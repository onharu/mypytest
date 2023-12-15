import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro_e import *
from pro_s import *
from pro_func import *
import help_func
import mypy.patterns
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern

class Stmt:
    pass

class Block(Stmt): # list[stm]
    def __init__(self, body:list[Stmt]):
        self.body = body
    def __repr__(self):
        return f"{self.body}"

class ClassDef(Stmt):
    def __init__(
            self,
            name:str,
            rolename:str,
            base_type_vars:list[str],
            #type_vars:Ch1 | Ch2 | Ch3 | None,
            defs: Block
    ):
        self.name = name
        self.rolename = rolename
        self.base_type_vars = base_type_vars
        self.defs = defs
    def __repr__(self):
        return f"class {self.name}_{self.rolename}({help_func.list_to_str(self.base_type_vars)}): \n   {self.defs}"
    #def __repr__(self):


def projection_class(n:mypy.nodes.ClassDef,r:str,tc:mypy.checker.TypeChecker) -> ClassDef:
    if "Ch1" in str(n.base_type_exprs[0]) or "Ch2" in str(n.base_type_exprs[0]) or "Ch3" in str(n.base_type_exprs[0]) and r in str(n.base_type_exprs[0]):
        exprs:list[str] = []
        for exp in n.base_type_exprs[1:]:
            exprs += [(projection_exp(exp,r,tc))]
        if type(n.defs.body[0]) == mypy.nodes.FuncDef: # definite function
            return ClassDef(n.name,r,exprs,projection_func(n.defs.body[0],r,tc))
        else: # class定義のなかで式、文が初めに来るとき
            return ClassDef(n.name,r,exprs,projection_block(n.defs.body,r,tc))
    else:
        raise Exception
    # クラス定義