from role import *
from enum import Enum
import math

class MChoice(Enum):
  L = "L"
  R = "R"

class Mergesort(Ch3[A,B,C]):
  #def __init__(self,ch_AB:Channel[object,A,B],ch_BC:Channel[object,B,C],ch_CA:Channel[object,C,A]):
  #  self.ch_AB = ch_AB
  #  self.ch_BC = ch_BC
  #  self.ch_CA = ch_CA
  #  ch_AB = Channel[object,A,B]("A","B")
  #  ch_BC = Channel[object,B,C]("B","C")
  #  ch_CA = Channel[object,C,A]("C","A")

  def __init__(self):
      self.ch_AB:Channel[object,A,B] = Channel[object,A,B]("A","B")
      self.ch_BC:Channel[object,B,C] = Channel[object,B,C]("B","C")
      self.ch_CA:Channel[object,C,A] = Channel[object,C,A]("C","A")

  def sort(self,a:At[list[int],A]):
    if len(a) > 1@A():
      self.ch_AB.select(MChoice.L@A())
      self.ch_CA.select(MChoice.L@A())
      pivot:At[float,A] = float(math.floor(len(a)/2@A())@A())@A()
      mb:Mergesort(Ch3[B,C,A]) = Mergesort(Ch3[B,C,A])
      mc:Mergesort(Ch3[C,A,B]) = Mergesort(Ch3[C,A,B])
      lhs:At[list[int],B] = mb.sort(self.ch_AB.com(a[0@A():int(pivot)]))
      rhs:At[list[int],C] = mc.sort(self.ch_CA.com(a[int(pivot):len(a)]))
      return merge(self.ch_AB.com(lhs),self.ch_AB.com(rhs))
    else:
      self.ch_AB.select(MChoice.R@A())
      self.ch_CA.select(MChoice.R@A())
      return a
    
  def merge(self,lhs:At[list[int],B],rhs:At[list[int],C]) -> At[list[int],A]:
    if len(lhs) > 0@B():
      self.ch_CA.select(MChoice.L@B())
      self.ch_BC.select(MChoice.L@B())
      result:At[list[int],A] = []
      if lhs[0]@B() <= self.ch_BC.com(rhs[0]@C()):
        self.ch_AB.select(MChoice.L@B())
        self.ch_BC.select(MChoice.L@B())
        result += self.ch_AB.com(lhs[0]@B())
        result += (merge(lhs[1@B():len(lhs)],rhs))
        return result
      else:
        pass
