import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro_s import *
import mypy.patterns
import help_func
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern


class Node:
    pass

class Stmt:
    pass

class Block(Stmt): # list[stm]
    def __init__(self, body:list[Stmt]):
        self.body = body
    def __repr__(self):
        return f"{self.body}"
    
class Var(Node):
    pass
    #def __init__(self,name:str):
    #    self.name = name
    #def __repr__(self):
    #    return f"{self.name}"
    
class Argument(Node):
    def __init__(self,
                 var:Var,
                 type_annotation:mypy.types.Type | None
                 ):
        self.var = var
        self.type_annotation = type_annotation
    def __repr__(self):
        return f"{self.var}"

class FuncDef(Stmt):
    def __init__(self,
                 name:str,
                 arguments:list[mypy.nodes.Var] | None, 
                 body:Block | None,
                 #typ:mypy.types.FunctionLike | None
                 ):
        self.name = name
        self.arguments = arguments
        self.body = body
        #self.typ = typ
    def __repr__(self):
        return f"def {self.name}({list_to_str(self.arguments)}): \n      {list_to_str(self.body)}"

def projection_func(n:mypy.nodes.FuncDef,r:str,tc:mypy.checker.TypeChecker) -> FuncDef:
    args:list[mypy.nodes.Var] = []
    if len(n.arguments) != 0:
        for arg in n.arguments:
            if arg.type_annotation is not None and r in str(arg.type_annotation):#help_func.rolesOf_t(arg.type_annotation,tc):
                print(arg.type_annotation)
                print(arg.variable)
                args.append(arg.variable)
            elif arg.type_annotation is not None and r not in str(arg.type_annotation):#help_func.rolesOf_t(arg.type_annotation,tc):
                args.append(None)
            elif arg.type_annotation is None:
                args.append(arg.variable)
            else:
                raise Exception
        return FuncDef(n.name,args,projection_block(n.body.body,r,tc))
    else:
        return FuncDef(n.name,[],projection_block(n.body.body,r,tc))
    
            
    # list[Argument]じゃなくてlist[Expression]にしたい　→　どうすればいいか？
    #　xの型推論の結果からroleをとる