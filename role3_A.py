from pychoral3 import *
from role import *
class Conv_A():
    def __init__(self):
        self.chAB = Channel[str,A,B]('A','B')
        
        self.chCA = Channel[str,C,A]('C','A')
    def f(self):
        Unit.id(self.chAB.com("Hello"))
        
        return self.chCA.com()