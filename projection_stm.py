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
import projection_exp

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

# normalizing
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

# projection (Statement)
def projection_stm(s:mypy.nodes.Statement,r:str,tc:mypy.checker.TypeChecker) -> Stmt:
    #Pass
    if isinstance(s,mypy.nodes.PassStmt):
        return Pass()
    #Return
    if isinstance(s,mypy.nodes.ReturnStmt):
        exp = projection_exp.projection_exp(s.expr,r,tc)
        return Return(exp) 
    #Seq
    if isinstance(s,mypy.nodes.ExpressionStmt):
        t = s.expr.accept(tc.expr_checker)
        if isinstance(t,mypy.types.Instance):
            if t.type.defn.name == "Enum":
                assert False

            #enum型の区別　→　メソッド名がselect
            #match文へのprojection???
    #Assignment
    #if isinstance(s,Asg):
    #    if r in rolesOf(s.type,tc):



#def projection_stm(s:mypy.nodes.Statement, r:str, tc:mypy.checker.TypeChecker) -> Stmt: 
#    # Pass
#    if isinstance(s,mypy.nodes.PassStmt):
#        return s
#    # Return
#    if isinstance(s,mypy.nodes.ReturnStmt):
#        s1 = projection_exp.projection_exp(s.expr,r,tc)
#        return s1
#    # Seq
#    if isinstance(s,mypy.nodes.ExpressionStmt):
#        # もしexpがEnum＠A型だったら
#        if isinstance(s.expr,mypy.nodes.MemberExpr):
#            if s.expr.name == "select":
#                # match文にprojection
#                assert False
#        else:
#            return projection_exp.projection_exp(s.expr,r,tc) + Seq.stmt
        



def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = set([t0.args[1]]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception