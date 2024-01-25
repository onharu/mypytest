import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro.pro_all import *
import mypy.patterns
import ast
from typing import TypeVar
import help_func

# Import 
def projection_md(n:mypy.nodes.Statement) -> Stmt:
    if isinstance(n,mypy.nodes.Import):
        return Import(help_func.get(n.ids))
    elif isinstance(n,mypy.nodes.ImportFrom):
        return ImportFrom(n.id,n.relative,help_func.get(n.names))
    elif isinstance(n,mypy.nodes.ImportAll):
        return ImportAll(n.id,n.relative)
    else:
        raise Exception("unexpected syntax",n)