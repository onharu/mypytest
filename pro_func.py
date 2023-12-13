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

def pro_func(n:mypy.nodes.FuncDef,r:str,tc:mypy.checker.TypeChecker):
    pass