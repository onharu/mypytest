from role import *
from enum import Enum
from typing import Iterator

#ConsumeChoice = Enum('ConsumeChoice',['AGAIN','STOP'])
class ConsumeChoice(Ch1[A],Enum):
    AGAIN = 'AGAIN'
    STOP = 'STOP'

# 型注釈としての ConsumeChoice
again: ConsumeChoice = ConsumeChoice.AGAIN
stop: ConsumeChoice = ConsumeChoice.STOP

class ConsumeItems(Ch2[A,B]):
  def __init__(self) -> None:
    self.chAB : Channel[int,A,B] = Channel[int,A,B]()

  def accept(self, name):
        print(name)

  def consumeItems(self,item:At[Iterator,A],consumer:At[int,B]) -> None:
    if item > Iterator@A():
      self.chAB.select(again@A())
    else:
      self.chAB.select(stop@A())