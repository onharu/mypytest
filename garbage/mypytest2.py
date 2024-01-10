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
                                                  "ex1.py"])

class MyVisitor(mypy.visitor.NodeVisitor[mypy.nodes.Statement], CheckerPluginInterface):
    #type_checker : mypy.checker.TypeChecker

    def __init__(self, checker:mypy.checker.TypeChecker, role:str):
        print("init success")
        self.type_checker = checker
        self.role = role

    def visit_func_def(self, defn: mypy.nodes.FuncDef) -> None:
        print("visit def")
        defn.body.accept(self)

    def visit_block(self, b: mypy.nodes.Block) -> None:
        print("visit block")
        for s in b.body:
            s.accept(self)
    

    #def roleof(self, e:mypy.nodes.Expression) -> str:
    #    t = e.accept(self.type_checker.expr_checker)
    #    if isinstance(t,mypy.types.Instance):
    #        t0 = str(t.args[0])
    #        return t0
    #    else:
    #        raise Exception("error")


    def roleof(self, e:mypy.nodes.Expression) -> str:
        t = e.accept(self.type_checker.expr_checker)
        if isinstance(t, mypy.types.Instance):
            t0 = t.type.defn.name
            if(t0 == "At"):
                t1 = str(t.args[1])
                return t1
            else:
                raise Exception("error")
            
    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> mypy.nodes.Statement:
        print("visit assign")
        t = a.rvalue.accept(self.type_checker.expr_checker) #右辺の式の方を調べる
        if isinstance(t,mypy.types.Instance):#右辺のexpr->instanceへダウンキャスト
            #t1 = t.type.defn.name #t1に右辺に存在する関数名を代入
            #print(t1)
            #if(t1 == "At"): #関数名がAtの場合
            #    t2 = str(t.args[1]) #role名を取り出す
            #else:
            #    pass
          if self.roleof(a.rvalue) == self.role:
            #指定したroleと代入文の右辺の式のroleが同じとき
            return a
            #statementは残す
          if self.roleof(a.rvalue) != self.role:
            #指定したroleと代入文の右辺の式のroleが一致しないとき
            return mypy.nodes.PassStmt()
            #その文を取り除く
          else:
            return a
          

    def print(n: mypy.nodes.Node):
       if isinstance(n, mypy.nodes.IfStmt):
          return "if" + print(n.expr) + "\n" + "\t" + print(n.body) + "\n" + "else:" + "\n" + "\t" + print(n.else_body) + "\n"
       
          

class MyExpVisitor(mypy.visitor.ExpressionVisitor,CheckerPluginInterface):
  def __init__(self, checker:mypy.checker.TypeChecker):
        print("init success")
        self.type_checker = checker
      
  def visit_op_expr(self, e: mypy.nodes.OpExpr) -> None:
      t = e.accept(self.type_checker.expr_checker) 

      pass

'''
    def visit_assignment_stmt(self, a: mypy.nodes.AssignmentStmt) -> mypy.nodes.Statement:
        print("visit assign")
        if self.roleof(a.rvalue) == self.role:
          #指定したroleと代入文の右辺の式のroleが同じとき
          return a
          #statementは残す
        else:
          #指定したroleと代入文の右辺の式のroleが一致しないとき
          return mypy.nodes.PassStmt()
          #その文を取り除く
'''




src = result.graph["ex1"]

for d in src.tree.defs:
    v = MyVisitor(src.type_checker(),"ex1.A")
    d.accept(v)

