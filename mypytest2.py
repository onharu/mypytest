import sys
import mypycustom
import mypy
import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from mypy.plugin import CheckerPluginInterface
from typing import Optional, cast
import mypy.type_visitor

class MyVisitor(mypy.visitor.NodeVisitor[mypy.nodes.Statement], CheckerPluginInterface):
    type_checker : mypy.checker.TypeChecker

    def __init__(self, checker:mypy.checker.TypeChecker, role):
        print("init success")
        self.type_checker = checker
        self.role = role
        

    def roleof(self, e:mypy.nodes.Expression) -> str:
        t = e.accept(self.type_checker.expr_checker)
        if isinstance(t,mypy.types.Instance):
            t0 = str(t.args[0])
            return t0
        else:
            raise Exception("error")

    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> mypy.nodes.Statement:
        print("visit assign")
        if self.roleof(a.rvalue) == self.role:#指定したroleと代入文の右辺の式のroleが同じとき
          print(a)
          return a#statementは残す
        else:#指定したroleと代入文の右辺の式のroleが一致しないとき
          return mypy.nodes.PassStmt()#その文を取り除く

