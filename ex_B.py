from pychoral import *
from role import *
class Conv_B():
    def __init__(self):
        self.chAB = Channel[int,A,B]()
    def f(self,b):
        
        return self.chAB.com(Unit.id)