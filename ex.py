# 色々確認用ファイル

#list = [1,2,3]
#list2 = []
#for i in range(len(list)):
#  
#    x = list[i] + 1
#    list2 += [x]
#
##print(list2)
#
#from typing import TypeVar, Generic
#from enum import Enum
#
#
#class Color(Enum):
#    RED = 1
#    GREEN = 2
#    BLUE = 3
#
#
#def print_color(color):
#    if color == Color.RED:
#        print('Color is red')
#    elif color == Color.GREEN:
#        print('Color is green')
#    elif color == Color.BLUE:
#        print('Color is blue')
#    else:
#        print('not Color enum')
#
#
#if __name__ == '__main__':
#    print_color(Color.BLUE)  # Color is blue
#    print_color(1)  # not Color enum
#    print(type(Color.GREEN))
#    #print(Color)  # <enum 'Color'>
#    print(Color(1))  # Color.RED
#    print(Color.RED == Color.RED)  # True
#    print(Color.RED == Color.GREEN)  # False
#    for color in Color:
#       print(color)

from typing import TypeVar, Generic
from enum import Enum
import mypy

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

class E(Enum):
    OK = 1
    KO = 2





x = E.OK@A()
print(type(x))

#def pri(a):
#    if a == E.OK:
#        print('OK')
#    elif a == E.KO:
#        print('KO')
#    else:
#        print('NO!')
#
#if __name__ == '__main__':
#    print(type(E.OK@A()))
#    pri(E.OK)
#    pri(E(2))
#    pri(1)