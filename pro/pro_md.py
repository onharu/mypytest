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

def get(tlist:list[tuple[str,str|None]]) -> list[str]:
    str_list:list[str] = []
    for tuple in tlist:
        str_list.append(tuple[0])
    return str_list
    
def projection_md(n:mypy.nodes.Statement) -> Stmt:
    print("module!")
    if isinstance(n,mypy.nodes.Import):
        return Import(get(n.ids))
    elif isinstance(n,mypy.nodes.ImportFrom):
        return ImportFrom(n.id,n.relative,get(n.names))
    elif isinstance(n,mypy.nodes.ImportAll):
        return ImportAll(n.id,n.relative)
    else:
        raise Exception("unexpected syntax",n)