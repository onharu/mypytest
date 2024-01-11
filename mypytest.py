import sys
import mypycustom
import mypy.build
import mypy.visitor
import mypy.nodes
import mypy.checker
import mypy.types
import mypy.type_visitor
import projection

# result <- ASTが保存されている
result : mypy.build.BuildResult | None = mypycustom.main([
    "--show-traceback", "--custom-typeshed", "./typeshed", "ex.py"])

if result is None: # Noneを省く
    sys.exit(1)

src = result.graph["ex"] #木構造
typechecker = src.type_checker()

if src.tree is None: # Noneを省く
    sys.exit(1)

filename = "ex.py"
roles = ["A","B"]
for r in roles:
    pro_filename = filename.replace(".","_"+r+".")
    print(pro_filename)
    f = open(pro_filename,"w")
    print(pro_filename)
    for stm in projection.projection_all(src.tree.defs,r,typechecker):
        print(r)
        f.write((projection.stmt_to_string(stm,0)))
#f = open("ex_A.py","w")
#for stm in projection.projection_all(src.tree.defs,"A",typechecker):
#    f.write((projection.stmt_to_string(stm,0)))