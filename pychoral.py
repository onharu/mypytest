from multiprocessing import Process, Queue, Pipe
import subprocess
import role
##import multiprocessing as mp
import os
from typing import Generic,TypeVar

_T1 = TypeVar("_T1")
_R1 = TypeVar("_R1")
_R2 = TypeVar("_R2")

class Unit:
    def id(self):
        pass

#myrole = None
parent_q = None# Channel宣言時に作られるPipe(親queue?)

class Channel(Generic[_T1,_R1,_R2]):
    def __init__(self):
        self.queue = None
            
    def com(self,msg:_T1=None) -> _T1:
        if self.queue is None: # queueがない　→　初めてcomを呼び出した時
            if msg is None: # msgがない　→ 受信側 
                self.queue = parent_q.recv() # pipeを使用してqueueを繋ぐ
                return self.queue.get() # queue.get()でqueueで送られてきたものを取得
            else: # msgがある　→ 送信側 → 受信側にparent_qを使ってqueue
                self.queue = Queue() # 新たにqueueを作る（送信側）
                self.queue.put(msg)
                return None
        else: # queueがある → queueがすでにつながっている
            if msg is None: # msgがない　→ 受信側 
                return self.queue.get()
            else: # msgがある　→ 送信側 
                self.queue.put(msg)
                return None
            
def start_processes(f_A, f_B):
    pipe_A, pipe_B = Pipe()
    pa = Process(target=connect, args=(f_A,pipe_A,))
    pb = Process(target=connect, args=(f_B,pipe_B,))
    pa.start()
    pb.start()
    pa.join() 
    pb.join()

def connect(f,pipe):
    parent_q = pipe
    print("pipe is connected")
    f()
            


#def f(filename):
#    subprocess.run(["python3",filename])
#
#if __name__ == "__main__":
#    f("ex_A.py")
#    pb = Process(target=f,args=("ex_B.py",))
#    pb.start()
#    pb.join()

#def f(q):
#    q.put([42, None, 'hello'])
#
#if __name__ == '__main__':
#    q = Queue()
#    p = Process(target=f, args=(q,))
#    p.start()
#    print(q.get())    # prints "[42, None, 'hello']"
#    p.join()
