import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro_e import *
from help_func import *
from pro_all import *
import mypy.patterns
from typing import TypeVar
# Lvalue = Union['NameExpr', 'MemberExpr', 'IndexExpr', 'SuperExpr', 'StarExpr','TupleExpr']; 
Lvalue: mypy.nodes._TypeAlias = mypy.nodes.Expression
Self = TypeVar("Self")


#block
def projection_block(s_list:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker)-> list[Stmt]:
    print("block!")
    #for i in range(len(s_list)):
    if s_list == []:
        return []
    else:
        #print(len(s_list))
        s = s_list[0]
        # 分岐あり(e;s -> match)
        if isinstance(s,mypy.nodes.ExpressionStmt):
            t = s.expr.accept(tc.expr_checker) # 型情報入手
            if isinstance(t,mypy.types.Instance) and \
                "enum" in t.type.defn.name and \
                    r in rolesOf(s.expr,tc) and \
                        isinstance(s.expr,mypy.nodes.CallExpr) and \
                            isinstance(s.expr.callee,mypy.nodes.MemberExpr) and \
                                s.expr.callee.name == "select":# enum型かつロールが合っているかつメソッド名がselectのとき
                if len(s.expr.args) == 1:# args:list[expression] <- このリストの要素は一つしかあり得ない
                    pro_args = projection_exp(s.expr.args[0],r,tc)
                    return [Match(projection_exp(s.expr,r,tc),[pro_args],[Block(projection_block(s_list[1:],r,tc),4)])]
                else:
                    raise Exception
            else:
                raise Exception
        else:# 分岐がない単一の文
            #print(s)
            return [projection_stm(s,r,tc)] + projection_block(s_list[1:],r,tc) # それぞれの文をプロジェクションする
    #assert False



# projection Statement（単一の文）
def projection_stm(s:mypy.nodes.Statement,r:str,tc:mypy.checker.TypeChecker) -> Stmt:
    print("stm!")
    #Pass
    if isinstance(s,mypy.nodes.PassStmt):
        return Pass()
    #Return
    elif isinstance(s,mypy.nodes.ReturnStmt):
        if s.expr is None:
            raise Exception
        exp = projection_exp(s.expr,r,tc)
        return Return(exp) 
    
    #Assinment
    elif isinstance(s,mypy.nodes.AssignmentStmt):
        print("assign!")
        lv = s.lvalues
        if len(lv) == 1:
            l = projection_exp(lv[0],r,tc)
            rvs = projection_exp(s.rvalue,r,tc)
            t = s.type
            if t is None and r in rolesOf(s.rvalue,tc):#型を明示していない場合（型推論で行う場合）
                return Asg(l,rvs,t)
            elif t is None and r not in rolesOf(s.rvalue,tc):
                return Es(rvs)
            else:#型明示
                if r in rolesOf_t(t,tc): 
                    return Asg(l,rvs,t) 
                else:
                    return Es(rvs) 
        else:
            raise Exception
        
    #OperatorAssignment
    elif isinstance(s,mypy.nodes.OperatorAssignmentStmt):
        l = projection_exp(s.lvalue,r,tc)
        rv = projection_exp(s.rvalue,r,tc)
        return OpAsg(l,rv,s.op)
    #if
    elif isinstance(s,mypy.nodes.IfStmt):
        assert len(s.expr)==len(s.body)
        exprs_projected:list[str] = []
        bodies_projected:list[Block] = []
        for i in range(len(s.expr)):
            exp = projection_exp(s.expr[i],r,tc)
            stm = projection_block(s.body[i].body,r,tc)
            exprs_projected += [exp]
            bodies_projected += [Block(stm,4)]
        if s.else_body is None:
            raise Exception
        else_projected = projection_block(s.else_body.body,r,tc)
        return If(exprs_projected,bodies_projected,Block(else_projected,4))
    #Es
    elif isinstance(s,mypy.nodes.ExpressionStmt):
        exp = projection_exp(s.expr,r,tc)
        return Es(exp)
    #raise
    elif isinstance(s,mypy.nodes.RaiseStmt):
        if s.expr is None:
            raise Exception
        exp = projection_exp(s.expr,r,tc)
        return Raise(exp)
    #assert
    elif isinstance(s,mypy.nodes.AssertStmt):
        exp = projection_exp(s.expr,r,tc)
        return Assert(exp)
    
    else:
        raise Exception("unexpected syntax",s)