import sys
import os
import mypycustom
import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor
import projection
import help_func

filename = input("filename : ") # PyChoralでコーディングされたPythonファイル名を入力
pychoralfile = filename+".py"
#roles = list(map(str,input("Roles : ").split())) #PyChoralプログラム中に出現する参加者名を入力
#print(type(roles),type(roles[0]),roles)
# result <- ASTが保存されている
result : mypy.build.BuildResult | None = mypycustom.main([
    "--show-traceback", "--custom-typeshed", "./typeshed", pychoralfile])

if result is None: # Noneを省く
    sys.exit(1)

src = result.graph[filename] #木構造
typechecker = src.type_checker()

if src.tree is None: # Noneを省く
    sys.exit(1)
#roleはプログラム中の最初のクラス定義から取得する
def get_roles(stm_list:list[mypy.nodes.Statement]) -> str:
    for stm in stm_list:
        if isinstance(stm,mypy.nodes.ClassDef) and \
            isinstance(stm.base_type_exprs[0],mypy.nodes.IndexExpr) and\
                isinstance(stm.base_type_exprs[0].index,mypy.nodes.TupleExpr):
                    role_list:list[str] = [ ]
                    for role in stm.base_type_exprs[0].index.items:
                        role_list.append(help_func.nameExpr(role))
                    print(role_list)
                    roles = ''.join(role_list)
        else:
            pass
    return roles

roles = get_roles(src.tree.defs)
#print(roles)

for r in roles:
    pro_filename = pychoralfile.replace(".","_"+r+".")
    print(pro_filename)
    f = open(pro_filename,"w")
    f.write("from pychoral"+str(len(roles))+" import *\n") 
    g = open(pro_filename,"a")
    for stm in projection.projection_all(src.tree.defs,r,typechecker):
        projection.stmt_to_string(stm,0)
        g.write(projection.stmt_to_string(stm,0))
        #f.write("from pychoral import *\n"+projection.stmt_to_string(stm,0))
#f = open("ex_A.py","w")
#for stm in projection.projection_all(src.tree.defs,"A",typechecker):
#    f.write((projection.stmt_to_string(stm,0)))