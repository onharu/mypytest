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
from pro_all import *
import help_func
import mypy.patterns
import ast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy.patterns import Pattern

def projection_class(n:mypy.nodes.ClassDef,r:str,tc:mypy.checker.TypeChecker) -> ClassDef:
    print("class!!")
    if "Ch1" in str(n.base_type_exprs[0]) or "Ch2" in str(n.base_type_exprs[0]) or "Ch3" in str(n.base_type_exprs[0]) and r in str(n.base_type_exprs[0]):
        exprs:list[str] = []
        for exp in n.base_type_exprs[1:]:
            exprs += [(projection_exp(exp,r,tc))]
        if type(n.defs.body[0]) == mypy.nodes.FuncDef: # definite function
            return ClassDef(n.name,r,exprs,Block([projection_func(n.defs.body[0],r,tc)]+[projection_all(n.defs.body[1:],r,tc)],4))
        else: # class定義のなかで式、文が初めに来るとき
            return ClassDef(n.name,r,exprs,Block(projection_block(n.defs.body,r,tc),4))
    else:
        raise Exception
    # クラス定義