import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
import pro_e,pro_s,pro_class,pro_func,pro_md
import mypy.patterns
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern

class Stmt:
    pass

def projection(n:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker) -> list[Stmt]:
    result:list[Stmt] = []
    for node in n:
        print(node)
        if isinstance(node,mypy.nodes.Import) or isinstance(node,mypy.nodes.ImportFrom) or isinstance(node,mypy.nodes.ImportAll):
            result += [pro_md.projection_md(node)]
        elif isinstance(node,mypy.nodes.ClassDef):
            result += [pro_class.projection_class(node,r,tc)]
        elif isinstance(node,mypy.nodes.FuncDef):
            result += [pro_func.projection_func(node,r,tc)]
        elif isinstance(node,mypy.nodes.Block):
            result += [pro_s.projection_block(node.body,r,tc)]
        else:
            result += [pro_s.projection_stm(node,r,tc)]
    return result