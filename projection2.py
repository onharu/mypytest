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

def projection(n:mypy.nodes.Node,r:str):
    if isinstance(n,mypy.nodes.Expression):
        #literal
        if isinstance(n, mypy.nodes.OpExpr):
            if n.op == "@":
                if isinstance(n.left,mypy.nodes.IntExpr) or isinstance(n.left,mypy.nodes.FloatExpr) or isinstance(n.left,mypy.nodes.StrExpr): # 1@A
                    if str(n.right) == r:
                        print(n.left)
                    else:
                        print("Unit.id")
                #if isinstance(n.left,mypy.nodes.FloatExpr): # 0.01@A
                #    if str(n.right) == r:
                #        print(n.left)
                #    else:
                #        print("Unit.id")
                #if isinstance(n.left,mypy.nodes.StrExpr): # "abc"@A
                #    if str(n.right) == r:
                #        print(n.left)
                #    else:
                #        print("Unit.id")
                #None,True,Falseは？
            else:#literalで＠がないのは例外扱いする
                raise Exception
        #関数呼び出し
        if isinstance(n, mypy.nodes.CallExpr):
            if rolesOf(n) == r: #f(Exp)のroleとprojectionのroleが一致する時
                for i in len(n.args):
                    if rolesOf(n.args[i]) == r:
                        return n.args[i]
                    else:
                        return "Unit.id"
                print(n)
            else:
                print ("Unit.id")
            
        
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker):
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At":
            roleName = str(t0.args[1]) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception

        
        
    #if isinstance(n,mypy.nodes.MemberExpr):
    #    rolesOf(n.expr,t)

            
    
    