'''
def fun(a:int):
  return a + 1

def even_odd():
  list1:list[int] = [3, 5, 4567, 8, 56, 10, 234, 99,16, 13, 5, 86, 999, 1234]
  list2:list[int] = []
  list3:list[int] = []
  for i in list1:
      if i % 2 == 0:
         list2.append(i)
      else:
      #if i % 2 != 0:
         list3.append(i)
  return list2

'''
#java
'''
class HelloRoles@(A, B) {
   public static void sayHello() {
      String@A a = "Hello from A"@A; 
      String@B b = "Hello from B"@B; 
      System@A.out.println(a); 
      System@B.out.println(b); 
   }
}

'''

from typing import TYPE_CHECKING, Generic, TypeVar, cast

T = TypeVar("T")
#at関数の第二引数でroleの解析が起こる

class Role:
  pass

class A(Role):
  pass
class B(Role):
  pass

class rstr(str,Generic[T]):
  pass

def at(x:str,y:T) -> rstr[T]:
  return cast(rstr[T],x)

#a0 = at("Hello",A()) 

a:rstr[A] = at("Hello from A",A()) 
b:rstr[B] = at("Hello from B",B())

#a = at("Hello","A") 
#b = at("Hello","B")

