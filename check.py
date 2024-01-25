from role import *
from enum import Enum
#from enum import Enum
#class Choice(Ch1[S],Enum):
#    T = "Thanks"
#    E = "The money is not enough"

#class Check(Ch2[S,C]):
#  def __init__(self) -> None:
#    self.ch_S_C : Channel[str,S,C] = Channel[str,S,C]()
#
#  def check(self,paied_money:At[int,S]) -> At[str,C]:
#      price:At[int,S] = 1000@S()
#      if (paied_money > price):
#          return self.ch_S_C.select(Choice.T.value@S())
#      else:
#          return self.ch_S_C.select(Choice.E.value@S())

#Choice = Enum('Choice',['L', 'R'])

class Check(Ch2[S,C]):
  def __init__(self):
    self.ch_CS : Channel[int,C,S] = Channel[int,C,S]()
    self.ch_SC : Channel[str,S,C] = Channel[str,S,C]()

  def check(self,price:At[int,S],money:At[int,C]) -> At[str,C]:
      payment = self.ch_CS.com(money)
      if (payment > price):
          return self.ch_SC.com("thanks"@S())
      else:
          return self.ch_SC.com("not enough"@S())
    