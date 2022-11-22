def n(str):
  names:list[str] = ['太郎', '次郎', '三郎']
  for name in names:
      print(name)
  return name


def fun(a:int):
  return a + 1


def f():
  list:list[int] = [x,y,z]
  x:int = 1
  y:int = 1
  for i in list:
    z:int = 3
  return x,y,z

def even_odd():
  list1:list[int] = [3, 5, 4567, 8, 56, 10, 234, 99,16, 13, 5, 86, 999, 1234]
  list2:list[int] = []
  list3:list[int] = []
  i:int
  for i in list1:
      if i % 2 == 0:
         list2.append(i)
      else:
         list3.append(i)
  return list2