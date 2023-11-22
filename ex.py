# 色々確認用ファイル
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

x = 123 @ A()

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