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
from typing import TypeVar

class Stmt:
    pass

class Import(Stmt):
    def __init__(self,ids:list[tuple[str, str | None]]):
        self.ids = ids
    def __repr__(self):
        return f"Import {self.ids[[0]]}"

class ImportFrom(Stmt):
    def __init__(self,id:str,relative:int,names:list[tuple[str, str | None]]):
        self.id = id
        self.relative = relative
        self.names = names
    def __repr__(self):
        return f"from {self.id} import {self.names}"

class ImportAll(Stmt):
    def __init__(self,id:str,relative:int):
        super().__init__()
        self.id = id
        self.relative = relative
    def __repr__(self):
        return f"from {self.id} import *"
    
def projection_md(n:mypy.nodes.Statement) -> Stmt:
    if isinstance(n,mypy.nodes.Import):
        return Import(n.ids)
    elif isinstance(n,mypy.nodes.ImportFrom):
        return ImportFrom(n.id,n.relative,n.names)
    elif isinstance(n,mypy.nodes.ImportAll):
        return ImportAll(n.id,n.relative)
    else:
        raise Exception("unexpected syntax",n)