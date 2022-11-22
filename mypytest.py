import sys
import mypycustom
import mypy
# import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
from mypy.plugin import CheckerPluginInterface
from typing import Optional
import mypy.type_visitor

result : mypy.build.BuildResult = mypycustom.main(["--show-traceback", "--verbose", "ex1.py"])

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
        print(s.expr.accept(self.type_checker.expr_checker))
        print()
        pass

    #addition
    def visit_for_stmt(self, f: mypy.nodes.ForStmt) -> None:
        print("visit for")
        f.body.accept(self)

    def visit_if_stmt(self, i: mypy.nodes.IfStmt) -> None:
        print("visit if")
        i.else_body.accept(self)
        

#class RoreOfVisitor(mypy.visitor.NodeVisitor[None], CheckerPluginInterface) -> List[str]:
    


src = result.graph["ex1"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
