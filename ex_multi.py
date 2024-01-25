from role import *
from multiprocessing import Process, Queue , Pipe
import subprocess
import ex_A,ex_B
import role3_A, role3_B, role3_C
import pychoral2

def run_A():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = A
    conv_a = ex_A.Conv_A()
    conv_a.f(100)

def run_B():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = B
    conv_b = ex_B.Conv_B()
    v = conv_b.f()
    print(v)

if __name__ == "__main__":
    pychoral2.start_processes(run_A, run_B)