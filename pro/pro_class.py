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
    
# クラス定義
def projection_class(n:mypy.nodes.ClassDef,r:str,tc:mypy.checker.TypeChecker) -> ClassDef:
    if isinstance(n.base_type_exprs[0],mypy.nodes.IndexExpr): #クラスの第一引数は必ずChクラスを継承する
    #print(projection_exp(n.base_type_exprs[0],r,tc))
        if not any(ch in str(n.base_type_exprs[0].base) for ch in ["Ch1", "Ch2", "Ch3"]):#第一引数にChがない場合
        #if "Ch1" not in str(n.base_type_exprs[0]) and "Ch2" not in str(n.base_type_exprs[0]) and "Ch3" not in str(n.base_type_exprs[0]):
            raise Exception
        else:
            if isinstance(n.base_type_exprs[0].index,mypy.nodes.TupleExpr):
                role_list:list[str] = [ ]
                for role in n.base_type_exprs[0].index.items:
                    role_list.append(help_func.nameExpr(role))
                roles = ','.join(role_list)
                print("roles = "+roles)
                #roles = projection_exp(n.base_type_exprs[0].index)
                if r not in roles:#Ch1の[S,C]をどうとるか
                    raise Exception
                exprs:list[str] = []
                for exp in n.base_type_exprs[1:]:
                    exprs += [(projection_exp(exp,r,tc))]
                s_list:list[Stmt] = []
                for stm in n.defs.body:
                    if isinstance(stm,mypy.nodes.FuncDef):
                        s_list.append(projection_func(stm,r,tc))
                    else:
                        raise Exception("not funcdef",stm)
                return ClassDef(n.name,r,exprs,Block(s_list,4))
            else:
                raise Exception("not role")
    else: # Chクラスを継承していない場合
        raise Exception("not exist Ch",n)