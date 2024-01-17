from pychoral import *
from role import *
class Conv_A():
    def __init__(self):
        self.chAB = Channel[int,A,B]()
    def f(self,a):
        a = 100
        if a<123:
            return Unit.id(self.chAB.com(123))
        else:
            return Unit.id(self.chAB.com(a))