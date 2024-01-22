from pychoral3 import *
from role import *
class Conv_B():
    def __init__(self):
        self.chAB = Channel[str,A,B]('A','B')
        self.chBC = Channel[str,B,C]('B','C')
        
    def f(self):
        x = self.chAB.com()
        Unit.id(self.chBC.com(x))
        pass