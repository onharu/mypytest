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
        if t0.type.defn.name == "At":
            roleName = set(str([t0.args[1]])) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception
    else:
        raise Exception
        
# rolesOf(type) -> str
def rolesOf_t(n:mypy.types.Type | None, typeChecker:mypy.checker.TypeChecker) -> set[str]:
    print(n)
    if isinstance(n,mypy.types.Instance):
        if n.type.defn.name == "At":
            roleName = set(str([n.args[1]])) # At[int,A]でいうところのA
            return roleName
        else:
            raise Exception
    else:
        raise Exception

# 構文木の情報から値だけを取り出す関数nameExpr
def nameExpr(e:mypy.nodes.Expression) -> str:
    if isinstance(e,mypy.nodes.NameExpr):
        return e.name
    else:
        raise Exception
    
def isNone(n:mypy.nodes.Node):
    if n is None:
        raise Exception
    else:
        pass

# listの[]を省略する関数 (list -> string)
def list_to_str(list:list) -> str:
    str_list = ''.join(str(x) for x in list)
    return str_list
