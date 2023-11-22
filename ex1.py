from typing import TypeVar, Generic
from enum import Enum
import mypy
import builtins

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

#A = TypeVar("A")
#B = TypeVar("B")
#C = TypeVar("C")

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

class Choice(Enum):
    OK = 1
    KO = 2

x = Choice.OK@A()

class C(Generic[T]):
    pass
class R2(Generic[U,V]):
    pass

def g0(y:builtins.At[str,A]):
    return y

def check(e1,e2):
    return e1


def g(x:str):
    # A() @ ""
    y = x @ A()
    check(Choice.OK@A(),A)
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


#class Choice(Enum):
#    HELLO = 1
#    BYE = 2
#
#class Bchannel(Generic[T,V]):
#    At[object,R2[T,V]]
#

#class Conv(Generic[A,B,C])
#
#    def __init__(self,ch_AB:Bchannel[A,B],ch_BC:Bchannel[B,C],ch_CA:Bchannel[C,A]):
#        self.ch_AB = ch_AB
#        self.ch_BC = ch_BC
#        self.ch_CA = ch_CA
#
#    def communicaton(msg):
#        ch_AB.comm(msg@A)
#        if msg == "Hello":
#            ch_BC.select(Choice@A(1))
#            ch_CA.select(Choice@A(1))
#            


    
    # a -> b:msg. b -> c:msg. c -> a:msg.  or   a -> b:bye. b -> c:bye. ends
