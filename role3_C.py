from pychoral3 import *
from role import *
class Conv_C():
    def __init__(self):
        
        self.chBC = Channel[str,B,C]('B','C')
        self.chCA = Channel[str,C,A]('C','A')
    def f(self):
        
        b = self.chBC.com()
        return Unit.id(self.chCA.com(b))