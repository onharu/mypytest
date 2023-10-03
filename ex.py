#def greeting(name: str) -> str:
#    return 'Hello ' + name
#
#greeting(3)         # Argument 1 to "greeting" has incompatible type "int"; expected "str"
##greeting(b'Alice')  # Argument 1 to "greeting" has incompatible type "bytes"; expected "str"
#greeting("World!")  # No error

from enum import Enum

# class syntax
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# functional syntax
Color = Enum('Color', ['RED', 'GREEN', 'BLUE'])
print(type(Color))

