from role import *
from builtins import *
class Conv_A():
    def __init__(self):
        self.chAB = Channel[int,A,B]()
    def f(self,x):
        x = 100
        return Unit.id(self.chAB.com(123))