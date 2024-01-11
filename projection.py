import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from data import *
import help_func
import mypy.patterns
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern

#Projection
def projection_all(n:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker) -> list[Stmt]:
    result:list[Stmt] = []
    for node in n:
        if isinstance(node,mypy.nodes.Import) or isinstance(node,mypy.nodes.ImportFrom) or isinstance(node,mypy.nodes.ImportAll):
            result += [projection_md(node)]
        elif isinstance(node,mypy.nodes.ClassDef):
            result += [projection_class(node,r,tc)]
        elif isinstance(node,mypy.nodes.FuncDef):
            result += [projection_func(node,r,tc)]
        elif isinstance(node,mypy.nodes.Block):
            result += projection_block(node.body,r,tc)
        else:
            result += [projection_stm(node,r,tc)]
    return result



# Import 
def projection_md(n:mypy.nodes.Statement) -> Stmt:
    if isinstance(n,mypy.nodes.Import):
        return Import(help_func.get(n.ids))
    elif isinstance(n,mypy.nodes.ImportFrom):
        return ImportFrom(n.id,n.relative,help_func.get(n.names))
    elif isinstance(n,mypy.nodes.ImportAll):
        return ImportAll(n.id,n.relative)
    else:
        raise Exception("unexpected syntax",n)
    

# クラス定義
def projection_class(n:mypy.nodes.ClassDef,r:str,tc:mypy.checker.TypeChecker) -> ClassDef:
    if "Ch1" not in str(n.base_type_exprs[0]) and "Ch2" not in str(n.base_type_exprs[0]) and "Ch3" not in str(n.base_type_exprs[0]):
        raise Exception
    if r not in str(n.base_type_exprs[0]):
        raise Exception
    exprs:list[str] = []
    for exp in n.base_type_exprs[1:]:
        exprs += [(projection_exp(exp,r,tc))]
    s_list:list[Stmt] = []
    for stm in n.defs.body:
        if isinstance(stm,mypy.nodes.FuncDef):
            s_list.append(projection_func(stm,r,tc))
        else:
            raise Exception("not funcdef",stm)
    return ClassDef(n.name,r,exprs,Block(s_list,4))

# 関数定義
def projection_func(n:mypy.nodes.FuncDef,r:str,tc:mypy.checker.TypeChecker) -> FuncDef:
    args:list[str] = []
    if len(n.arguments) != 0:
        for arg in n.arguments:
            if arg.type_annotation is not None and r in help_func.rolesOf_t(arg.type_annotation,tc):
                args.append(arg.variable.name)
            elif arg.type_annotation is not None and r not in help_func.rolesOf_t(arg.type_annotation,tc):
                args
            elif arg.type_annotation is None:
                args.append(arg.variable.name)
            else:
                raise Exception("pattern missmatching",n.arguments)
        return FuncDef(n.name,args,Block(projection_block(n.body.body,r,tc),4))
    else:
        return FuncDef(n.name,[],Block(projection_block(n.body.body,r,tc),4))

#Block
def projection_block(s_list:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker)-> list[Stmt]:
    if s_list == []:
        return []
    else:
        s = s_list[0]
        # 分岐あり(e;s -> match)
        if isinstance(s,mypy.nodes.ExpressionStmt):
            t = help_func.get_type(tc, s.expr)
            if isinstance(t,mypy.types.Instance) and \
                "enum" in t.type.defn.name and \
                    r in help_func.rolesOf(s.expr,tc) and \
                        isinstance(s.expr,mypy.nodes.CallExpr) and \
                            isinstance(s.expr.callee,mypy.nodes.MemberExpr) and \
                                s.expr.callee.name == "select":# enum型かつロールが合っているかつメソッド名がselectのとき
                if len(s.expr.args) == 1:# args:list[expression] <- このリストの要素は一つしかあり得ない
                    pro_args = projection_exp(s.expr.args[0],r,tc)
                    return [Match(projection_exp(s.expr,r,tc),[pro_args],[Block(projection_block(s_list[1:],r,tc),4)])]
                else:
                    raise Exception("length is not 1",s.expr.args)
            else:
                return [projection_stm(s,r,tc)] + projection_block(s_list[1:],r,tc)
        else:# 分岐がない単一の文
            #print(s)
            return [projection_stm(s,r,tc)] + projection_block(s_list[1:],r,tc) # それぞれの文をプロジェクションする


# Statement（単一の文）
def projection_stm(s:mypy.nodes.Statement,r:str,tc:mypy.checker.TypeChecker) -> Stmt:
    # Pass
    if isinstance(s,mypy.nodes.PassStmt):
        return Pass()
    # Return
    elif isinstance(s,mypy.nodes.ReturnStmt):
        if s.expr is None:
            raise Exception("None error",s.expr)
        exp = projection_exp(s.expr,r,tc)
        return Return(exp) 
    # Assignment
    elif isinstance(s,mypy.nodes.AssignmentStmt):
        lv = s.lvalues
        if len(lv) == 1:
            l = projection_exp(lv[0],r,tc)
            rvs = projection_exp(s.rvalue,r,tc)
            t = s.type
            if t is None and r in help_func.rolesOf(s.rvalue,tc):#型を明示していない場合（型推論で行う場合）
                return Asg(l,rvs,t)
            elif t is None and r not in help_func.rolesOf(s.rvalue,tc):
                return Es(rvs)
            else:#型明示
                if r in help_func.rolesOf_t(t,tc): 
                    return Asg(l,rvs,t) 
                else:
                    return Es(rvs) 
        else:
            raise Exception("pattern missmatching",s)
    # OperatorAssignment
    elif isinstance(s,mypy.nodes.OperatorAssignmentStmt):
        l = projection_exp(s.lvalue,r,tc)
        rv = projection_exp(s.rvalue,r,tc)
        return OpAsg(l,rv,s.op)
    # If 
    elif isinstance(s,mypy.nodes.IfStmt):
        exp = projection_exp(s.expr[0],r,tc)
        stm = projection_block(s.body[0].body,r,tc)
        if s.else_body is None:
          raise Exception("None error")
        else_projected = projection_block(s.else_body.body,r,tc)
        if "Unit.id" in exp:
            stm1 = help_func.normalize(Block(stm,4))
            stm2 = help_func.normalize(Block(else_projected,4))
            return Es2(exp,help_func.merge(stm1,stm2))
        else:
            return If(exp,Block(stm,4),Block(else_projected,4))
    # Es
    elif isinstance(s,mypy.nodes.ExpressionStmt):
        exp = projection_exp(s.expr,r,tc)
        return Es(exp)
    # Raise
    elif isinstance(s,mypy.nodes.RaiseStmt):
        if s.expr is None:
            raise Exception
        exp = projection_exp(s.expr,r,tc)
        return Raise(exp)
    # Assert
    elif isinstance(s,mypy.nodes.AssertStmt):
        exp = projection_exp(s.expr,r,tc)
        return Assert(exp)
    else:
        raise Exception("unexpected syntax",s)
    
# Expression    
def projection_exp(n:mypy.nodes.Expression,r:str,tc:mypy.checker.TypeChecker) -> str:
    #literal(role付き)
    if isinstance(n, mypy.nodes.OpExpr):
        if n.op == "@":
            if isinstance(n.left,mypy.nodes.IntExpr) or \
                isinstance(n.left,mypy.nodes.FloatExpr) or \
                    isinstance(n.left,mypy.nodes.StrExpr): # 1@A
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.value)
                else:
                    return "Unit.id"
            # None,True,False
            elif isinstance(n.left, mypy.nodes.NameExpr):
                if help_func.nameExpr(n.right) == r:
                    return str(n.left.name)
                else:
                    return "Unit.id"
            elif isinstance(n.left,mypy.nodes.OpExpr):
                return projection_exp(n.left,r,tc)
            else:
                raise Exception
        else:#二項演算 (+ - * / %)
            if r in help_func.rolesOf(n.left,tc) and r in help_func.rolesOf(n.right,tc):
                return projection_exp(n.left,r,tc) + str(n.op) + projection_exp(n.right,r,tc)
            else:
                return "Unit.id("  + projection_exp(n.left,r,tc)+","+ projection_exp(n.right,r,tc) +" )" 
    #比較演算子 (二つの式の比較限定)
    elif isinstance(n,mypy.nodes.ComparisonExpr):
        assert len(n.operators)==1
        assert len(n.operands)==2
        if n.operators[0] == ">" or ">=" or "==" or "<" or "<=" or "!=" or "and":
            left = projection_exp(n.operands[0],r,tc)
            right = projection_exp(n.operands[1],r,tc)
            return left+n.operators[0]+right
        else:
            raise Exception
    #field
    elif isinstance(n,mypy.nodes.MemberExpr):
        return projection_exp(n.expr,r,tc)+"."+n.name
    #関数呼び出し、メソッド呼び出し、クラス定義
    elif isinstance(n, mypy.nodes.CallExpr):
        #関数 f = variable
        if isinstance(n.callee, mypy.nodes.NameExpr): 
            exp_list:list[str] = []
            if r in help_func.rolesOf(n,tc): #f(Exp)のroleとprojection_expのroleが一致する時
                for exp_i in n.args:
                    exp_list.append(projection_exp(exp_i,r,tc))
                exp_var = ','.join(exp_list)
                return str(n.callee) + exp_var
            else:#f(Exp)のroleとprojection_expのroleが一致しない時
                for exp_i in n.args:
                    if r in help_func.rolesOf(exp_i,tc):
                        exp_list.append(projection_exp(exp_i,r,tc))
                    else:
                        n.args.remove(exp_i)
                exp_var = ','.join(exp_list)
                return "Unit.id(" + str(n.callee) + exp_var + ")"
        #method呼び出し f = memberexpr
        elif isinstance(n.callee, mypy.nodes.MemberExpr):
            exp_list_i = []
            if r in help_func.rolesOf(n,tc): # R in e.f(e')
                for exp_i in n.args:
                    exp_list_i.append(projection_exp(exp_i ,r,tc))
                exp_var_i = ','.join(exp_list_i)
                return projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + ")"
            else: # R not in e.f(e')
                if r in help_func.rolesOf(n.callee.expr,tc): # R in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    return "Unit.id(" + projection_exp(n.callee.expr,r,tc) + "." + n.callee.name + "(" + exp_var_i + "))"
                else: # R not in e
                    for exp_i in n.args:
                        exp_list_i.append(projection_exp(exp_i ,r,tc))
                    exp_var_i = ','.join(exp_list_i)
                    return "Unit.id(" + projection_exp(n.callee.expr,r,tc) + "," + exp_var_i + ")"
        # クラス定義
        elif isinstance(n.callee, mypy.nodes.IndexExpr):
            exp_list = []
            id_list = []
            if isinstance(n.callee.index,mypy.nodes.TupleExpr):
                for id in n.callee.index.items:
                    id1 = projection_exp(id,r,tc)
                    id_list += [id1]
                ids = ",".join(id_list)
                if r in ids: # R in Roles
                    for exp_i in n.args:
                        exp_list.append(projection_exp(exp_i ,r,tc))
                    exp_var = ','.join(exp_list)
                    return help_func.nameExpr(n.callee.base) + "[" + ids + "](" + exp_var + ")"
                else: # R not in Roles
                    for exp_i in n.args:
                        exp_list.append(projection_exp(exp_i ,r,tc))
                    exp_var = ','.join(exp_list)
                    return "Unit.id(" + exp_var + ")" 
            else:
                raise Exception
        else:
            raise Exception
    elif isinstance(n,mypy.nodes.NameExpr):
        return n.name
    elif isinstance(n,mypy.nodes.IntExpr):
        return str(n.value)
    else:
        raise Exception("unexcepted syntax",n)