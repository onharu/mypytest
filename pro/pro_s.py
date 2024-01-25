import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro.pro_e import *
from help_func import *
from pro.pro_all import *
import mypy.patterns
from typing import TypeVar
# Lvalue = Union['NameExpr', 'MemberExpr', 'IndexExpr', 'SuperExpr', 'StarExpr','TupleExpr']; 
Lvalue: mypy.nodes._TypeAlias = mypy.nodes.Expression
Self = TypeVar("Self")


#Block
def projection_block(s_list:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker)-> list[Stmt]:
    if s_list == []:
        return []
    else:
        s = s_list[0]
        # 分岐あり(e;s -> match)
        if isinstance(s,mypy.nodes.ExpressionStmt):
            #t = help_func.get_type(tc, s.expr)
            #if isinstance(t,mypy.types.Instance) and \
            #    "enum" in t.type.defn.name and \
            if r in help_func.rolesOf(s.expr,tc) and \
                isinstance(s.expr,mypy.nodes.CallExpr) and \
                    isinstance(s.expr.callee,mypy.nodes.MemberExpr) and \
                        s.expr.callee.name == "select":# enum型かつロールが合っているかつメソッド名がselectのとき
                if len(s.expr.args) == 1 and isinstance(s.expr.args[0],mypy.nodes.OpExpr):# args:list[expression] <- このリストの要素は一つしかあり得ない
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
        if isinstance(s.rvalue,mypy.nodes.CallExpr) and \
            isinstance(s.rvalue.callee, mypy.nodes.IndexExpr) and \
                isinstance(s.rvalue.callee.index,mypy.nodes.TupleExpr):#コンストラクタ生成
            lv = s.lvalues
            if len(lv) == 1:
                l = projection_exp(lv[0],r,tc)
                rvs = projection_exp(s.rvalue,r,tc)
                t = s.type
                if (t is None) and (r in help_func.rolesOf(s.rvalue,tc)):#型を明示していない場合（型推論で行う場合）
                    return Asg(l,rvs,t)
                elif (t is None) and (r not in help_func.rolesOf(s.rvalue,tc)):
                    return Asg("","",t)
                else:#型明示
                    if r in help_func.rolesOf_t(t,tc): 
                        return Asg(l,rvs,t) 
                    else:
                        return Asg("","",t)
            else:
                raise Exception("pattern missmatching",s)
        else:#その他の代入文
            lv = s.lvalues
            if len(lv) == 1:
                l = projection_exp(lv[0],r,tc)
                rvs = projection_exp(s.rvalue,r,tc)
                t = s.type
                if (t is None) and (r in help_func.rolesOf(s.rvalue,tc)):#型を明示していない場合（型推論で行う場合）
                    return Asg(l,rvs,t)
                elif (t is None) and (r not in help_func.rolesOf(s.rvalue,tc)):
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
        stm = projection_block(s.body[0].body,r,tc)
        if s.else_body is None:
          raise Exception("None error")
        else_projected = projection_block(s.else_body.body,r,tc)
        if isinstance(s.expr[0],mypy.nodes.ComparisonExpr):
            if (r in help_func.rolesOf(s.expr[0].operands[0],tc)) and\
                  (r in help_func.rolesOf(s.expr[0].operands[1],tc)):
                exp1 = projection_exp(s.expr[0].operands[0],r,tc)
                exp2 = projection_exp(s.expr[0].operands[1],r,tc)
                return If(exp1+s.expr[0].operators[0]+exp2,Block(stm,4),Block(else_projected,4))
            else:
                stm1 = help_func.normalize_block(stm)
                stm2 = help_func.normalize_block(else_projected)
                return Es2("",help_func.merge_block(stm1,stm2))
        else:
            if r not in help_func.rolesOf(s.expr[0],tc):
                stm1 = help_func.normalize_block(stm)
                stm2 = help_func.normalize_block(else_projected)
                #for i in range(len(stm1)):
                #    print("Stm1."+str(i)+" = " +help_func.stmt_to_string(stm1[i],0))
                #for j in range(len(stm2)):
                #    print("Stm1."+str(j)+" = " +help_func.stmt_to_string(stm2[i],0))
                return Es2(projection_exp(s.expr[0],r,tc),help_func.merge_block(stm1,stm2))
            else:
                return If(projection_exp(s.expr[0],r,tc),Block(stm,4),Block(else_projected,4))
    # Es
    elif isinstance(s,mypy.nodes.ExpressionStmt):
        #print(s.expr)
        exp = projection_exp(s.expr,r,tc)
        return help_func.normalize(Es(exp))
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