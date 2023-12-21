## 補助関数の集合ファイル

import sys
import mypycustom
import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor

# rolesOf(e) -> str
def rolesOf(n:mypy.nodes.Expression, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    t0 = n.accept(typeChecker.expr_checker) #nの型情報を取得する
    if isinstance(t0, mypy.types.Instance): #Expression → Instance
        if t0.type.defn.name == "At": #型クラスがAtである場合
            roleNames = set(str([t0.args[1]])) # At[int,A] -> {A}
            return roleNames
        if t0.type.defn.name == "Channel": #型クラスがChannnelである場合
            roleNames = set(str([t0.args[1]]),str([t0.args[2]])) #Channel[str,A,B] -> {A,B}
        else:
            raise Exception
    else:
        raise Exception
        
# rolesOf(type) -> str
def rolesOf_t(n:mypy.types.Type | None, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    print(n)
    if isinstance(n,mypy.types.Instance):
        if n.type.defn.name == "At":
            roleNames = set(str([n.args[1]])) 
            return roleNames
        if n.type.defn.name == "Channel":
            roleNames = set(str([n.args[1]]),str([n.args[2]]))
            return roleNames
        else:
            raise Exception
    else:
        raise Exception

# 構文木の情報から値だけを取り出す関数nameExpr
def nameExpr(e:mypy.nodes.Expression) -> str:
    if isinstance(e,mypy.nodes.NameExpr):
        return e.name
    elif isinstance(e,mypy.nodes.CallExpr):
        #print(e.callee)
        return str(e.callee)
    else:
        raise Exception
    
def isNone(n:mypy.nodes.Node):
    if n is None:
        raise Exception
    else:
        pass

# listの[]を省略する関数 (list -> string)
def list_to_str(list:list) -> str:
    str_list = ','.join(str(x) for x in list)
    return str_list
