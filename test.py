from role import *
import mypy
from enum import Enum
#from typing import Literal
#
#def f() -> Literal["a"]:
#    return "a"
#
#hints = get_type_hints(f)
#
#return_type = hints["return"]
#literal_value = return_type.__args__[0]
#print(type(literal_value))

#def lit_to_str() -> str:
#    string = str(Literal["a"])
#    return string

Choice = Enum('Choice',['L','R'])

#class Choice(Enum):
#    L = "left"
#    R = "right"
print(Choice)
a = Choice.L.name
print(a)
print(type(a))
#reveal_type(a)
#reveal_type(Choice.L.name)
#reveal_type(Choice.value)
#reveal_type(Choice.name)
#reveal_type(Choice)
###a = "A"
##reveal_type(a)
#
#
#x1 = 1
#y1 = 2
#z1 = (x1 < y1)
##reveal_type(z1)
##reveal_type(x1)
#x = 1@A()
##reveal_type(x)
#y = 2@A()
##reveal_type(y)