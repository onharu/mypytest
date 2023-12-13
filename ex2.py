import mypy
import ast

print(ast.dump(ast.parse("""\
class Foo(base1, base2, metaclass=meta):
    pass
"""), indent=4))