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

# 構文木
class Stmt:
    pass

class Block(Stmt): # list[stm]
    def __init__(
            self,
            body:list[Stmt],
            indent:int
    ):
        super().__init__() 
        #    サブクラスで__init__を定義すると、親クラスの__init__が上書きされる
        # -> super().__init__()で親クラスの__init__と同様の処理が可能
        # -> 今回は親クラスのStmtに__init__がないためなくても良い
        self.body = body
        self.indent = indent

class Pass(Stmt):
    pass

class Return(Stmt):
    def __init__(self, exp:str):
        self.expr = exp

class Raise(Stmt): # raise
    def __init__(self, expr:str):#, from_expr:str | None):
        self.expr = expr
        #self.from_expr = from_expr

class Assert(Stmt): # assert
    expr:str
    def __init__(self,expr:str):
        self.expr = expr
    

class Es(Stmt): # e1; s
    def __init__(self, exp:str):
        self.expr = exp

class Asg(Stmt): # id:TE = e; s
    def __init__(
            self, 
            #lv:list[str], assignment変更前
            lv:str,
            rv:str,
            type:mypy.types.Type | None, 
            ):
        self.lvalues = lv
        self.rvalue = rv
        self.type = type
        
class OpAsg(Stmt): # e1 Asgop e2; s
    def __init__(
            self, 
            lv:str, 
            rv:str, 
            op:str, 
            ):
        self.lvalue = lv
        self.rvalue = rv
        self.op = op
        
class If(Stmt): # if e1:s1; else:s2; s
    def __init__(
            self, 
            exp:list[str], 
            body:list[Block], 
            else_body:Block, 
            
            ):
        self.expr = exp
        self.body = body
        self.else_body = else_body

class Match(Stmt): # match
    def __init__(
            self, 
            sub:str, 
            pat:list[str],#list[mypy.patterns.ValuePattern.expr], 
            #guards:list[str | None], 
            bodies:list[Block], 
            
            ):
        self.subject = sub
        self.patterns = pat
        #self.guards = guards
        self.bodies = bodies
    
class FuncDef(Stmt):
    def __init__(self,
                 name:str,
                 arguments:list[str] | None, 
                 body:Block,
                 #typ:mypy.types.FunctionLike | None
                 ):
        self.name = name
        self.arguments = arguments
        self.body = body
        #self.typ = typ
    
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

class Import(Stmt):
    def __init__(self,ids:list[tuple[str, str | None]]):
        self.ids = ids

class ImportFrom(Stmt):
    def __init__(self,id:str,relative:int,names:list[tuple[str, str | None]]):
        self.id = id
        self.relative = relative
        self.names = names

class ImportAll(Stmt):
    def __init__(self,id:str,relative:int):
        super().__init__()
        self.id = id
        self.relative = relative

def stmt_to_string(s:Stmt,indent:int) -> str:
    if isinstance(s,Pass):
        return " "*indent + "pass"
    elif isinstance(s,Return):
        return " "*indent + "return " + s.expr
    elif isinstance(s,Raise):
        return " "*indent + "raise " + s.expr
    elif isinstance(s,Assert):
        return " "*indent + "return " + s.expr
    elif isinstance(s,Es):
        return " "*indent + s.expr
    elif isinstance(s,Asg):
        return " "*indent + s.lvalues + " = " + s.rvalue
    elif isinstance(s,OpAsg):
        return " "*indent + s.lvalue + " " +s.op + " " + s.rvalue
    elif isinstance(s,If):
        return " " * indent + "if " + s.expr + ":\n" + \
                stmt_to_string(s.body, indent+4) + \
                " " * indent + "else:\n" +\
                stmt_to_string(s.else_body, indent+4)
    elif isinstance(s,Match):
        return " "*indent + "match " + s.subject + ":\n" + \
                " "*(indent+4) + "case " + s.patterns + ":\n" + \
                stmt_to_string(s.bodies,indent+8)
    elif isinstance(s,FuncDef):
        return " "*indent + "def " + s.name + "("+s.arguments+"):\n" + stmt_to_string(s.body,indent+4)
    elif isinstance(s,ClassDef):
        return " "*indent + "class " + s.name + "_" + s.rolename + "(" + s.base_type_vars + "):\n" + s.defs
    elif isinstance(s,Import):
        return " "*indent + "import " + s.ids
    elif isinstance(s,ImportFrom):
        return " "*indent + "from " + s.id + " import " + s.names
    elif isinstance(s,ImportAll):
        return " "*indent + "from " + s.id + " *"
    else:
        assert False



def projection_all(n:list[mypy.nodes.Statement],r:str,tc:mypy.checker.TypeChecker) -> list[Stmt]:
    result:list[Stmt] = []
    for node in n:
        #print(node)
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