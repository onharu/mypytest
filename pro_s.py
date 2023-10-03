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
# 構文木
class Stmt:
    pass

class Pass(Stmt):
    pass

class Return(Stmt):
    def __init__(self, exp:str):
        self.expr = exp

class Seq(Stmt): # e1; s
    def __init__(self, exp:mypy.nodes.ExpressionStmt, stmt:Stmt):
        self.expr = exp
        self.stmt = stmt

class Asg(Stmt): # id:TE = e; s
    def __init__(
            self, 
            lv:mypy.nodes.AssignmentStmt, 
            rv:mypy.nodes.AssignmentStmt, 
            type:mypy.nodes.AssignmentStmt, 
            stmt:Stmt
            ):
        self.lvalues = lv
        self.rvalue = rv
        self.type = type
        self.stmt = stmt

class OpAsg(Stmt): # e1 Asgop e2; s
    def __init__(
            self, 
            lv:mypy.nodes.OperatorAssignmentStmt, 
            rv:mypy.nodes.OperatorAssignmentStmt, 
            op:mypy.nodes.OperatorAssignmentStmt, 
            stmt:Stmt
            ):
        self.lvalue = lv
        self.rvalue = rv
        self.op = op
        self.stmt = stmt

class If(Stmt): # if e1:s1; else:s2; s
    def __init__(
            self, 
            exp:mypy.nodes.IfStmt, 
            body:mypy.nodes.IfStmt, 
            else_body:mypy.nodes.IfStmt, 
            stmt:Stmt
            ):
        self.expr = exp
        self.body = body
        self.else_body = else_body
        self.stmt = stmt

class Try(Stmt): # try:s; except e:s2; s 
    def __init__(
            self, 
            body:mypy.nodes.TryStmt, 
            vars:mypy.nodes.TryStmt, 
            types:mypy.nodes.TryStmt, 
            handlers:mypy.nodes.TryStmt, 
            stmt:Stmt
            ):
        self.body = body
        self.vars = vars
        self.types = types
        self.handlers = handlers
        self.stmt = stmt

class Match(Stmt):
    def __init__(
            self, 
            sub:mypy.nodes.MatchStmt, 
            pat:mypy.nodes.MatchStmt, 
            guards:mypy.nodes.MatchStmt, 
            bodies:mypy.nodes.MatchStmt, 
            stmt:Stmt
            ):
        self.subject = sub
        self.patterns = pat
        self.guards = guards
        self.bodies = bodies
        self.stmt = stmt

# problem
#・Expression　→　str を返すようになっており、射影後の構文木に存在する式が全て文字列である


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
        #if r in rolesOf(s.type,tc): # <- Typeからどうroleをとる？
        if r in rolesOf(s.rvalue,tc): # <- （代替案）右辺の型情報からとる
            return Asg(lv,rvs,t,s) # <- stmtはどうする？
        else:
            return Seq(rvs,s) 
    #OperatorAssignment
    if isinstance(s,mypy.nodes.OperatorAssignmentStmt):
        rv = pro_e.projection_exp(s.rvalue,r,tc)
        return OpAsg(s.lvalue,rv,s.op,s)
    #if
    if isinstance(s,mypy.nodes.IfStmt):
        exp = pro_e.projection_exp(s.expr,r,tc)
        stm1 = projection_stm(s.body,r,tc)
        stm2 = projection_stm(s.else_body,r,tc)
        if r in rolesOf(s.expr,tc):
            return If(exp,stm1,stm2,s)
        else:
            return Seq(exp,stm1,stm2,s) # <- merge踏まえても何になる？
    #Try
    if isinstance(s,mypy.nodes.TryStmt):
        if r in rolesOf(s.types,tc):
            body = projection_stm(s.body,r,tc)
            te = pro_e.projection_exp(s.types,r,tc)
            vars = s.vars
            exbody = projection_stm(s.handlers,r,tc)
            return Try(body,te,vars,exbody,s)
        
    #Seq
    #if isinstance(s,mypy.nodes.ExpressionStmt):
    #    t = s.expr.accept(tc.expr_checker)
    #    if isinstance(t,mypy.types.Instance):
    #        if t.type.defn.name == "Enum":
    #            if isinstance(s.expr,mypy.nodes.CallExpr):
    #                call = s.expr.callee
    #                if isinstance(call,mypy.nodes.MemberExpr):
    #                    if call.name == "select":
    #                        #roleが合っているのかの確認もいる
    #                        assert False
            #match文へのprojection???
    

def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = set([t0.args[1]]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception


#normalizing
def normalize(s:Stmt) -> Stmt: 
    if isinstance(s, Pass):
        return s
    elif isinstance(s, Return):
        return s
    elif isinstance(s, Seq):
        # ここでは stmt.expr が削る対象だったら s.stmt を return する
        assert False # TODO
    # elif...
    assert False

# merging
def merge(s1:Stmt, s2:Stmt) -> Stmt: 
    assert False # TODO
