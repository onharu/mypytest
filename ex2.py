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
#print(list2)
#print(list3)
