from typing import TypeVar, Generic

T = TypeVar("T")
#U = TypeVar("U")
#V = TypeVar("V")

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

def g0(y:At[str,A]):
    return y

def check(e1,e2):
    return e1

def g(x:str):
    # A() @ ""
    y = x @ A()
    check(C[A](),A)
    g0(y)
    # A() @ 123
    return x
