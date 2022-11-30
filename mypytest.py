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


class MyVisitor(mypy.visitor.NodeVisitor[None], CheckerPluginInterface):
    type_checker : mypy.checker.TypeChecker

    def __init__(self, checker:mypy.checker.TypeChecker):
        print("init success")
        self.type_checker = checker
    
    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
        print("visit def")
        defn.body.accept(self)

    def visit_block(self, b: mypy.nodes.Block) -> None:
        print("visit block")
        for s in b.body:
            s.accept(self)

    def visit_return_stmt(self, s :mypy.nodes.ReturnStmt) -> None:
        print("visit return stmt")
        #s.expr.accept(self)
        if s.expr is not None:
            print(type(s.expr.accept(self.type_checker.expr_checker)))
        pass

    #addition
    #for文
    def visit_for_stmt(self, f: mypy.nodes.ForStmt) -> None:
        print("visit for")
        f.body.accept(self)
    #if文
    def visit_if_stmt(self, i: mypy.nodes.IfStmt) -> None:
        print("visit if")
        for i0 in i.body:
            i0.accept(self)
        if i.else_body is not None:
            i.else_body.accept(self)
    #代入文
    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> None:
        print("visit assign")
        t = a.rvalue.accept(self.type_checker.expr_checker)
        #print(t)
        if isinstance(t,mypy.types.Instance):
            print(t.args[0])
            #print(t.args[0].typ)
    #これでロールの名前は取り出せた
    #ロールがクラスから取ってきているのでTypeInfoからなんかやる

    def roleof(self, e:mypy.nodes.Expression) -> str:
        t = e.accept(self.type_checker.expr_checker)
        if isinstance(t,mypy.types.Instance):
            t0 = str(t.args[0])
            return t0
        else:
            raise Exception("error")

        







        

'''
class RolesOfExpVisitor(mypy.visitor.ExpressionVisitor[set[str]]):
    type_checker : mypy.checker.TypeChecker

    def visit_call_expr(self, c: mypy.nodes.CallExpr) -> set[str]:
        print("visit call")
        c.accept(self.type_checker.expr_checker)
       ''' 


    

result : mypy.build.BuildResult = mypycustom.main(["--show-traceback", "--verbose", "ex1.py"])

src = result.graph["ex1"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
