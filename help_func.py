import sys
import mypycustom
import mypy
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor

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
