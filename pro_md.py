import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro_all import *
import mypy.patterns
import ast
from typing import TypeVar
    
def projection_md(n:mypy.nodes.Statement) -> Stmt:
    print("module!")
    if isinstance(n,mypy.nodes.Import):
        return Import(n.ids)
    elif isinstance(n,mypy.nodes.ImportFrom):
        return ImportFrom(n.id,n.relative,n.names)
    elif isinstance(n,mypy.nodes.ImportAll):
        return ImportAll(n.id,n.relative)
    else:
        raise Exception("unexpected syntax",n)