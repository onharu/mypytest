# 色々確認用ファイル
#from typing import TypeVar, Generic
#from enum import Enum
#import mypy
#import builtins
#
#T = TypeVar("T")
#U = TypeVar("U")
#V = TypeVar("V")

#A = TypeVar("A")
#B = TypeVar("B")
#C = TypeVar("C")
#x: At[int, type[A]] = 123 @ A
#class B(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#    pass
#
#class C(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#    pass
#
#class R2(Generic[U,V]):
#    pass
#
##class Bchannel(Generic[T,V]):
##    builtins.At[object,R2[T,V]]
#
#class Choice(Enum):
#    OK = 1
#    KO = 2

#from role import *
#class HelloRoles(Ch2[A,B]):
#  def f(self):
#    a:At[str,A] = "Hello from A"@A()
#    b:At[str,B] = "Hello from B"@B()
#    print(a@A())
#    print(b@B())
from role import *
class Conv(Ch2[A,B]):
  def __init__(self):
    self.chAB : Channel[int,A,B] = Channel[int,A,B]()

  def f(self,a:At[int,A]) -> At[int,B]:#,b:At[str,B]):
    a = 100@A()
    if a < 123@A():
      return self.chAB.com(123@A())
    else:
      return self.chAB.com(a)
      #return self.chAB.com(100@A())
