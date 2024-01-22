from pychoral3 import *
from role import *
class Conv_A():
    def __init__(self):
        self.chAB = Channel[str,A,B]('A','B')
        
        self.chCA = Channel[str,C,A]('C','A')
    def f(self,a):
        if a==100:
            Unit.id(self.chAB.com(123))
            
            return self.chCA.com()
        else:
            Unit.id(self.chAB.com(a))
            
            return self.chCA.com()