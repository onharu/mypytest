from role import *
class Conv(Ch3[A,B,C]):
  def __init__(self):
    self.chAB : Channel[str,A,B] = Channel[str,A,B]("A","B")
    self.chBC : Channel[str,B,C] = Channel[str,B,C]("B","C")
    self.chCA : Channel[str,C,A] = Channel[str,C,A]("C","A")

  def f(self) -> At[str,A]:
    a = self.chAB.com("Hello"@A())
    b = self.chBC.com(a)
    return self.chCA.com(b)