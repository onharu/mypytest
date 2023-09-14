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
import help_func
import projection_exp

result : mypy.build.BuildResult = mypycustom.main(["--show-traceback", 
                                                    #"--verbose",
                                                    "--custom-typeshed", "./typeshed",
                                                    "ex1.py"])


class MyVisitor(mypy.visitor.NodeVisitor[None], CheckerPluginInterface):
    type_checker : mypy.checker.TypeChecker

    def __init__(self, checker:mypy.checker.TypeChecker):
        #print("init success")
        self.type_checker = checker
    
    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
        #print("visit def")
        defn.body.accept(self)

    def visit_block(self, b: mypy.nodes.Block) -> None:
        #print("visit block")
        for s in b.body:
            s.accept(self)

    def visit_return_stmt(self, s :mypy.nodes.ReturnStmt) -> None:
        #print("visit return stmt")
        s.expr.accept(self)
        #print(s.expr.accept(self.type_checker.expr_checker))
        t = s.expr.accept(self.type_checker.expr_checker) 
        #print("printing class of:" + str(t))
        #print(type(t))  # mypy.types.Instance
        if isinstance(t, mypy.types.Instance):
            print(t.type.defn.name)
            #print("printing class of t.args:" + str(t.args))
            #print(type(t.args))
        pass
        '''
        if s.expr is not None:
            print(type(s.expr.accept(self.type_checker.expr_checker)))
        pass
'''

    #addition
    #for文
    def visit_for_stmt(self, f: mypy.nodes.ForStmt) -> None:
        #print("visit for")
        f.body.accept(self)
    #if文
    def visit_if_stmt(self, i: mypy.nodes.IfStmt) -> None:
        #print("visit if")
        for i0 in i.body:
            i0.accept(self)
        if i.else_body is not None:
            i.else_body.accept(self)
    #代入文
    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> None:
        #print("visit assign")
        t = a.rvalue.accept(self.type_checker.expr_checker)
        #print("printing class of:" + str(t)) 
        #print(type(t))  # mypy.types.Instance
        if isinstance(t, mypy.types.Instance):
            t0 = t.type.defn.name
            #print(t0)
            #print("printing class of t.args:" + str(t.args[1]))
            print(type(t))



    def visit_expression_stmt(self, e: mypy.nodes.ExpressionStmt) -> None:
        print("visit expr_stmt")
        if isinstance(e.expr,mypy.nodes.CallExpr):
            callee = e.expr.callee
            if isinstance(callee, mypy.nodes.NameExpr):
                #print(str(callee.name))
                #print(type(e))
                if str(callee.name) == "check":
                    print("visit check")
                    role = help_func.nameExpr(e.expr.args[1])
                    p = projection_exp.projection(e.expr.args[0],role,self.type_checker)
                    print(type(e.expr.args[1]))
                    print("printing  "+str(p))
    




'''
    def roleof(self, e:mypy.nodes.Expression) -> str:
        t = e.accept(self.type_checker.expr_checker)
        if isinstance(t,mypy.types.Instance):
            t0 = str(t.args[0])
            return t0
        else:
            raise Exception("error")
'''
if result is None:
    sys.exit(1)

src = result.graph["ex1"]
typechecker = src.type_checker()

for d in src.tree.defs:
    v = MyVisitor(src.type_checker())
    d.accept(v)
    if isinstance(d,mypy.types.Instance):
        pass


    