import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro.pro_s import *
#import pro_s
from pro.pro_all import *
from data import *
#import pro_all
import mypy.patterns
import help_func
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern
    
#class Var(Node):
#    pass
#    #def __init__(self,name:str):
#    #    self.name = name
#    #def __repr__(self):
#    #    return f"{self.name}"
#    
#class Argument(Node):
#    def __init__(self,
#                 var:Var,
#                 type_annotation:mypy.types.Type | None
#                 ):
#        self.var = var
#        self.type_annotation = type_annotation
#    def __repr__(self):
#        return f"{self.var}"
    
def projection_func(n:mypy.nodes.FuncDef,r:str,tc:mypy.checker.TypeChecker) -> FuncDef:
    print("def!")
    args:list[str] = []
    if len(n.arguments) != 0:
        for arg in n.arguments:
            if arg.type_annotation is not None and r in help_func.rolesOf_t(arg.type_annotation,tc):
                print(type(help_func.rolesOf_t(arg.type_annotation,tc)))
                print("rolesOf_t = "+help_func.list_to_str(help_func.rolesOf_t(arg.type_annotation,tc)))
                #print(arg.type_annotation)
                #print(arg.variable.name)
                args.append(arg.variable.name)
            elif arg.type_annotation is not None and r not in help_func.rolesOf_t(arg.type_annotation,tc):
                print(type(help_func.rolesOf_t(arg.type_annotation,tc)))
                print("rolesOf_t = "+help_func.list_to_str(help_func.rolesOf_t(arg.type_annotation,tc)))
                args
            elif arg.type_annotation is None:
                args.append(arg.variable.name)
            else:
                raise Exception
        return FuncDef(n.name,args,Block(projection_block(n.body.body,r,tc),4))
    else:
        return FuncDef(n.name,[],Block(projection_block(n.body.body,r,tc),4))
    
            
    # list[Argument]じゃなくてlist[Expression]にしたい　→　どうすればいいか？
    #　xの型推論の結果からroleをとる