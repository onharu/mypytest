from pychoral2 import *
from role import *
from enum import Enum
class Check_C():
    def __init__(self):
        self.ch_CS = Channel[int,C,S]()
        self.ch_SC = Channel[str,S,C]()
    def check(self,money):
        Unit.id(self.ch_CS.com(money))
        
        return self.ch_SC.com()