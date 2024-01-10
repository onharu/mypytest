import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
from enum import Enum
import mypy.type_visitor
from pro.pro_e import *
from pro.pro_s import *
from pro.pro_func import *
from pro.pro_all import *
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
        #n.defs.body[0]からbodyの長さ分だけbodyの要素に対してそれぞれプロジェクションする　n.defs.body[i]に対してprojection_func
        #プロジェクション後のbodyをリストでまとめてClassDefの要素としてとる
        s_list:list[Stmt] = []
        for stm in n.defs.body:
            if isinstance(stm,mypy.nodes.FuncDef):
                s_list.append(projection_func(stm,r,tc))
            else:
                raise Exception
        return ClassDef(n.name,r,exprs,Block(s_list,4))
        #if type(n.defs.body[0]) == mypy.nodes.FuncDef: # definite function
        #    return ClassDef(n.name,r,exprs,Block([projection_func(n.defs.body[0],r,tc)]+[projection_all(n.defs.body[1:],r,tc)],4))
        #else: # class定義のなかで式、文が初めに来るとき
        #    return ClassDef(n.name,r,exprs,Block(projection_block(n.defs.body,r,tc),4))
    else:
        raise Exception
    # クラス定義