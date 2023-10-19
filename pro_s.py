import sys
import mypycustom
import mypytest
import mypy
#import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
#from mypy.plugin import CheckerPluginInterface
#from typing import Optional, cast
import mypy.type_visitor
#from pro_e import projection_exp
import pro_e

# Lvalue = Union['NameExpr', 'MemberExpr', 'IndexExpr', 'SuperExpr', 'StarExpr','TupleExpr']; 
Lvalue: mypy.nodes._TypeAlias = mypy.nodes.Expression

# 構文木
class Stmt:
    pass

class Block(Stmt): # list[stm]
    def __init__(
            self,
            body:list[mypy.nodes.Statement]
    ):
        super().__init__() 
        #    サブクラスで__init__を定義すると、親クラスの__init__が上書きされる
        # -> super().__init__()で親クラスの__init__と同様の処理が可能
        # -> 今回は親クラスのStmtに__init__がないためなくても良い
        self.body = body

class Pass(Stmt):
    pass

class Return(Stmt):
    def __init__(self, exp:mypy.nodes.Expression):
        self.expr = exp

class Seq(Stmt): # e1; s
    def __init__(self, exp:mypy.nodes.Expression):
        self.expr = exp

class Asg(Stmt): # id:TE = e; s
    def __init__(
            self, 
            lv:list[Lvalue], 
            rv:mypy.nodes.Expression, 
            type:mypy.types.Type, 
            ):
        self.lvalues = lv
        self.rvalue = rv
        self.type = type
        
class OpAsg(Stmt): # e1 Asgop e2; s
    def __init__(
            self, 
            lv:Lvalue, 
            rv:mypy.nodes.Expression, 
            op:str, 
            ):
        self.lvalue = lv
        self.rvalue = rv
        self.op = op
        
class If(Stmt): # if e1:s1; else:s2; s
    def __init__(
            self, 
            exp:list[mypy.nodes.Expression], 
            body:list[mypy.nodes.Block], 
            else_body:mypy.nodes.Block | None, 
            
            ):
        self.expr = exp
        self.body = body
        self.else_body = else_body
        

class Try(Stmt): # try:s; except e:s2; s 
    def __init__(
            self, 
            body:mypy.nodes.Block, 
            vars:list[mypy.nodes.NameExpr | None], 
            types:list[mypy.nodes.Expression | None], 
            handlers:list[mypy.nodes.Block], 
            
            ):
        self.body = body
        self.vars = vars
        self.types = types
        self.handlers = handlers
        

class Match(Stmt): # match
    def __init__(
            self, 
            sub:mypy.nodes.Expression, 
            pat:list[mypy.nodes.Pattern], 
            guards:list[mypy.nodes.Expression | None], 
            bodies:list[mypy.nodes.Block], 
            
            ):
        self.subject = sub
        self.patterns = pat
        self.guards = guards
        self.bodies = bodies



# problem
#・Expression　→　str を返すようになっており、射影後の構文木に存在する式が全て文字列である

def projection_block(s_list:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker) -> list[Stmt]:
    prolist:list[Stmt] = []
    for i in range(len(s_list)):
        e_s = projection_stm(s_list[i],r,tc)
        prolist += [e_s]
    return prolist

    


# projection (Statement)
def projection_stm(s:mypy.nodes.Statement,r:str,tc:mypy.checker.TypeChecker) -> Stmt:
    #Pass
    if isinstance(s,mypy.nodes.PassStmt):
        return Pass()
    #Return
    if isinstance(s,mypy.nodes.ReturnStmt):
        exp = pro_e.projection_exp(s.expr,r,tc)
        return Return(exp) 
    #Assignment
    if isinstance(s,mypy.nodes.AssignmentStmt):
        lv = s.lvalues
        rvs = pro_e.projection_exp(s.rvalue,r,tc)
        t = s.type
        if r in rolesOf_t(s.type,tc): # <- Typeからどうroleをとる？
            return Asg(lv,rvs,t) 
        else:
            return Seq(rvs) 
    #OperatorAssignment
    if isinstance(s,mypy.nodes.OperatorAssignmentStmt):
        rv = pro_e.projection_exp(s.rvalue,r,tc)
        return OpAsg(s.lvalue,rv,s.op)
    #if
    if isinstance(s,mypy.nodes.IfStmt):
        exp = pro_e.projection_exp(s.expr,r,tc)
        stm1 = projection_stm(s.body,r,tc)
        stm2 = projection_stm(s.else_body,r,tc)
        if r in rolesOf(s.expr,tc):
            return If(exp,stm1,stm2)
        else:
            return Seq(exp,merge(stm1,stm2)) # <- merge踏まえても何になる？
    #Try
    if isinstance(s,mypy.nodes.TryStmt):
        if r in rolesOf(s.types,tc):
            body = projection_stm(s.body,r,tc)
            te = pro_e.projection_exp(s.types,r,tc)
            vars = s.vars
            exbody = projection_stm(s.handlers,r,tc)
            return Try(body,te,vars,exbody)
        
    #Seq
    if isinstance(s,mypy.nodes.ExpressionStmt):
        t = s.expr.accept(tc.expr_checker)
        if isinstance(t,mypy.types.Instance):
            if "enum" in t.type.defn.name and r in rolesOf(s.expr):
                if isinstance(s.expr,mypy.nodes.CallExpr):
                    call = s.expr.callee
                    if isinstance(call,mypy.nodes.MemberExpr):
                        if call.name == "select":
                            assert False # <- ここでMatch文へのProjection
        else:
            exp = pro_e.projection_exp(s.expr,r,tc)
            return Seq(exp)
            #match文へのprojection???
    
# rolesOf(e) -> str
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = set([t0.args[1]]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception
        
# rolesOf(type) -> str
def rolesOf_t(n:mypy.types.Type, typeChecker:mypy.checker.TypeChecker) -> str:
    if isinstance(n,mypy.types.Instance):
        if n.type.defn.name == "At":
            roleName = set([n.args[1]]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception



# merging
# 同じstm,expはそのまま残す
def merge(s1:Stmt, s2:Stmt) -> Stmt: 
    # Block (list[stm])
    if isinstance(s1,Block) and isinstance(s2,Block):
        # listの要素にマージの再帰を定義する
        # s=[s1, s2, s3 ...]  s'=[s1', s2', s3' ...]のとき
        # s ⊔ s' = [s1 ⊔ s1', s2 ⊔ s2', s3 ⊔ s3', ...]
        for i in s1.body:
            for j in s2.body:
                return merge(s1.body[i],s2.body[j])
        assert False
    # return
    if isinstance(s1,Return) and isinstance(s2,Return):
        if s1.expr == s2.expr:
            return s1
        else:
            raise Exception
    # AsgOp
    if isinstance(s1,OpAsg) and isinstance(s2,OpAsg):
        if s1.lvalue == s2.lvalue and s1.rvalue == s2.rvalue:
            return OpAsg(s1.lvalue,s1.rvalue,s1.op)
        else:
            return merge(s1.stmt,s2.stmt)
    # e;s
    if isinstance(s1,Seq) and isinstance(s2,Seq):
        if s1.expr == s2.expr:
            return s1
        else:
            return None
    # if
    if isinstance(s1,If) and isinstance(s2,If):
        if s1.expr == s2.expr:
            return If(s1.expr,merge(s1.body,s2.body),merge(s1.else_body,s2.else_body),merge(s1.stmt,s2.stmt))
        else:
            return None














# Noop
def noop(exp:str):# 射影後のExpression(String型)
    if "Unit.id" in exp:
        return ""
    else:
        return exp



#normalizing
def normalize(s:Stmt) -> Stmt: 
    if isinstance(s, Pass):
        return s
    elif isinstance(s, Return):
        return s
    elif isinstance(s, Seq):
        # ここでは stmt.expr が削る対象だったら s.stmt を return する
        assert False # TODO
    #elif isinstance(s,OpAsg):
    #    if noop(s.rvalue)
    # elif...
    assert False
