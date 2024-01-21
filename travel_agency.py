from role import *
from enum import Enum

class Choice(Enum):
  Price = "Reserve"
  Cancel = "Cancel"


price:int = 100
billing:str = "price is"+str(price)

class Travel_Agency(Ch3[Customer,Agency,Hotel]):
  def __init__(self):
    self.chCA : Channel[str,Customer,Agency] = Channel[str,Customer,Agency]()
    self.chAH : Channel[int|str,Agency,Hotel] = Channel[int|str,Agency,Hotel]()
    self.chHC : Channel[str|None,Hotel,Customer] = Channel[str|None,Hotel,Customer]()

  def travel_agency(self,msg:At[str,Customer]):
    c_msg = self.chCA.com(msg)
    if c_msg == Choice.Reserve@Customer():
      self.chAH.select(price)
      return self.chHC.com
