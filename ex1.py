from typing import TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")

class Roled1(Generic[T]):
    pass

class Roled2(Generic[T,U]):
    pass

#class rstr(str, Roled1[T]):
#    pass

class channel(Roled2[T,U]):
    pass

class Role:
    pass

class A(Role):
    def __matmul__(self, x): # @ を使えるようにする
        pass
    pass

#def at(x:T, role:Role) -> T:
#    return x

def g(x:str):
    # A() @ ""
    x @ A()
    # A() @ 123
    return x

'''
from typing import TYPE_CHECKING, Generic, TypeVar, cast

T = TypeVar("T")
#at関数の第二引数でroleの解析が起こる

class Role:
  pass

class A(Role):
  pass
class B(Role):
  pass

#class rstr(str,Generic[T]):
#  pass

def at(x:T,y:Role) -> T:
  return x

#a0 = at("Hello",A()) 
def sayHello():
  a = at("Hello from A",A()) # "Hello from A" @ A
  b = at("Hello from B",B())

#a = at("Hello","A") 
#b = at("Hello","B")

'''