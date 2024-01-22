from role import *
class Conv(Ch3[A,B,C]):
  def __init__(self):
    self.chAB : Channel[str,A,B] = Channel[str,A,B]("A","B")
    self.chBC : Channel[str,B,C] = Channel[str,B,C]("B","C")
    self.chCA : Channel[str,C,A] = Channel[str,C,A]("C","A")

  def f(self,a:At[int,A]) -> At[int,A]:
    if a == 100@A():
      x = self.chAB.com(123@A())
      y = self.chBC.com(x)
      return self.chCA.com(y)
    else:
      x = self.chAB.com(a)
      y = self.chBC.com(x)
      return self.chCA.com(y)

  #def f(self) -> At[str,A]:
  #  a = self.chAB.com("Hello"@A())
  #  b = self.chBC.com(a)
  #  return self.chCA.com(b)