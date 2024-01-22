from multiprocessing import Process, Queue, Pipe
import multiprocessing as mp
import os
from typing import Generic,TypeVar

_T1 = TypeVar("_T1")
_R1 = TypeVar("_R1")
_R2 = TypeVar("_R2")

class Unit:
    def id(self):
        pass

parent_pipeA = None # 誰かからAにつながっているpipe
parent_pipeB = None # 誰かからBにつながっているpipe
parent_pipeC = None # 誰かからCにつながっているpipe

roledict = {"A":parent_pipeA,"B":parent_pipeB,"C":parent_pipeC}

class Channel(Generic[_T1,_R1,_R2]):
    def __init__(self,from_r:str,to_r:str): #from_r：送信者、to_r：受信者
        self.pipe = None
        self.from_r = from_r
        self.to_r = to_r

    def com(self,msg:_T1=None) -> _T1:
        if msg is None: # msgがない　→ 受信側 
            print("received pipe")
            if self.from_r in roledict.keys():
                return roledict[self.from_r].recv()
            else:
                raise Exception("no role")
        else: # msgがある　→ 送信側 → 受信側にparent_pipeを使ってpipeを送る
            if self.to_r in roledict.keys():
                roledict[self.to_r].send(msg)
                print("send msg to " + self.to_r)
                return None
            else:
                raise Exception("no role")


def start_processes(f_A, f_B, f_C):
    pipe_AtoB, pipe_BtoA = Pipe()
    pipe_BtoC, pipe_CtoB = Pipe()
    pipe_CtoA, pipe_AtoC = Pipe()
    pa = Process(target=connectA, args=(f_A,pipe_AtoB,pipe_AtoC,)) 
    pb = Process(target=connectB, args=(f_B,pipe_BtoC,pipe_BtoA,)) 
    pc = Process(target=connectC, args=(f_C,pipe_CtoA,pipe_CtoB,)) 
    pa.start()#pychoral3 を実行(role A)
    pb.start()#pychoral3 を実行(role B)
    pc.start()#pychoral3 を実行(role C)
    pa.join() 
    pb.join()
    pc.join()

def connectA(f,pipe_AtoB,pipe_AtoC):
    global parent_pipeA
    global roledict 
    roledict = {"A":None,"B":pipe_AtoB,"C":pipe_AtoC}
    print("pipe_AtoB,pipe_AtoC are connected")
    f()

def connectB(f,pipe_BtoC,pipe_BtoA):
    global parent_pipeB
    global roledict 
    roledict = {"A":pipe_BtoA,"B":None,"C":pipe_BtoC}
    print("pipe_BtoC,pipe_BtoA are connected")
    f()

def connectC(f,pipe_CtoA,pipe_CtoB):
    global parent_pipeC
    global roledict 
    roledict = {"A":pipe_CtoA,"B":pipe_CtoB,"C":None}
    print("pipe_CtoA,pipe_CtoB are connected")
    f()