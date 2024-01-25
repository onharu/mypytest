from pychoral2 import *
from role import *
from enum import Enum
from typing import Iterator
class ConsumeChoice(Enum):
    AGAIN = 'AGAIN'
    STOP = 'STOP'
    
class ConsumeItems_A():
    def __init__(self):
        self.chAB = Channel[int,A,B]()