import sys
import mypycustom
import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor
import projection

filename = input("filename : ") # PyChoralでコーディングされたPythonファイル名を入力
pychoralfile = filename+".py"
roles = ["A","B","C"] # プログラム中に出てくるroleをあらかじめ挙げておく
# result <- ASTが保存されている
result : mypy.build.BuildResult | None = mypycustom.main([
    "--show-traceback", "--custom-typeshed", "./typeshed", pychoralfile])

if result is None: # Noneを省く
    sys.exit(1)

src = result.graph[filename] #木構造
typechecker = src.type_checker()

if src.tree is None: # Noneを省く
    sys.exit(1)

for r in roles:
    pro_filename = pychoralfile.replace(".","_"+r+".")
    print(pro_filename)
    f = open(pro_filename,"w")
    f.write("from pychoral3 import *\n") # 通信するroleによって名前変更が必要(pychoral2 or pychoral3)
    g = open(pro_filename,"a")
    for stm in projection.projection_all(src.tree.defs,r,typechecker):
        projection.stmt_to_string(stm,0)
        g.write(projection.stmt_to_string(stm,0))
        #f.write("from pychoral import *\n"+projection.stmt_to_string(stm,0))
#f = open("ex_A.py","w")
#for stm in projection.projection_all(src.tree.defs,"A",typechecker):
#    f.write((projection.stmt_to_string(stm,0)))