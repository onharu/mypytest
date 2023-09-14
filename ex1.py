from typing import TypeVar, Generic

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

class Role:
    pass

class A(Role):
    def __matmul__(self, x): # @ を使えるようにする
        pass
    pass

class B(Role):
    def __matmul__(self, x): # @ を使えるようにする
        pass
    pass

class C(Generic[T]):
    pass
class R2(Generic[U,V]):
    pass

def g0(y:At[str,A]):
    return y

def check(e1,e2):
    return e1

def g(x:str):
    # A() @ ""
    y = x @ A()
    check(123@A,A)
    g0(y)
    # A() @ 123
    return x

#class HelloRoles@[A,B]:
#    def sayHello():
#        a:str@A = "Hello from A"@A
#        b:str@B = "Hello from B"@B
#        print(a)
#        print(b)
#
#class HelloRoles_A:
#    def sayHello():
#        a = "Hello from A"
#        print(a)
#
#class HelloRoles_B:
#    def sayHello():
#        b = "Hello from B"
#        print(b)

