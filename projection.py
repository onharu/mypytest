import sys
import mypycustom
import mypy
#import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from mypy.plugin import CheckerPluginInterface
#from typing import Optional, cast
import mypy.type_visitor

result : mypy.build.BuildResult = mypycustom.main(["--show-traceback", 
                                                    #"--verbose",
                                                    "--custom-typeshed", "./typeshed",
                                                    "ex2.py"])

class MyVisitor(mypy.visitor.NodeVisitor[mypy.nodes.Statement], CheckerPluginInterface):
    type_checker : mypy.checker.TypeChecker
    
    def __init__(self, checker:mypy.checker.TypeChecker):
        print("init success")
        self.type_checker = checker

    def print(n: mypy.nodes.Node):
            if isinstance(n, mypy.nodes.IfStmt):
                return "if" + print(n.expr) + "\n" + "\t" + print(n.body) + "\n" + "else:" + "\n" + "\t" + print(n.else_body) + "\n" + print("aaa")
            elif isinstance(n, mypy.nodes.AssignmentStmt):
                #＠があるかないか
                

        

src = result.graph["ex2"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
    if isinstance(d,mypy.types.Instance):
        pass