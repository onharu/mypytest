from role import *
from enum import Enum
import math

class Choice(Enum):
  L = "L"
  R = "R"

class Mergesort(Ch3[M,S1,S2]):
  def __init__(self,
               ch_MS1:Channel[object,M,S1],
               ch_MS2:Channel[object,M,S2],
               ch_S1S2:Channel[object,S1,S2]
               ):
    self.ch_MS1 = ch_MS1
    self.ch_MS2 = ch_MS2
    self.ch_S1S2 = ch_S1S2

    ch_MS1 = Channel[object,M,S1]("M","S1")
    ch_MS2 = Channel[object,M,S2]("M","S2")
    ch_S1S2 = Channel[object,S1,S2]("S1","S2")

  def sort(self,a:At[list[int],M]):
    if len(a) > 1@M():
      self.ch_MS1.select(Choice.L@M())
      self.ch_MS2.select(Choice.L@M())
      pivot:At[float,M] = float(math.floor(len(a)/2@M())@M())@M()
      mb:Mergesort(Ch3[S1,S2,M]) = Mergesort(Ch3[S1,S2,M])
      mc:Mergesort(Ch3[S2,M,S1]) = Mergesort(Ch3[S2,M,S1])
      lhs:At[list[int],S1] = mb.sort()
