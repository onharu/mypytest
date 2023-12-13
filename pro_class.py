import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
import pro_e
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

def projection_class(n:mypy.nodes.ClassDef,r:str,tc:mypy.checker.TypeChecker) -> ClassDef:
    if "Ch1" or "Ch2" or "Ch3" in str(n.base_type_exprs[0]) and r in str(n.base_type_exprs[0]):
        exprs:list[str] = []
        for exp in n.base_type_exprs[1:]:
            exprs += [pro_e.projection_exp(exp,r,tc)]
        return ClassDef(n.name,r,exprs,n.defs)
    else:
        raise Exception
    # クラス定義