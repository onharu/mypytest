#import mypy
#import ast
#
#print(ast.dump(ast.parse("""\
#class Role:
#    pass
#class A(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#class B(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#class Conv(Ch2[A,B]):
#  pass
#"""), indent=4))

def greeting(name:str) -> str:
  return "hello"+name

greeting(123)
greeting(b"alice")