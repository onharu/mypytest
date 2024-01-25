from pychoral2 import *
from role import *
from enum import Enum
class Check_S():
    def __init__(self):
        self.ch_CS = Channel[int,C,S]()
        self.ch_SC = Channel[str,S,C]()
    def check(self,price):
        payment = self.ch_CS.com()
        if payment>price:
            return Unit.id(self.ch_SC.com("thanks"))
        else:
            return Unit.id(self.ch_SC.com("not enough"))