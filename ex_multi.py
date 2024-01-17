from pychoral import *
from role import *
from multiprocessing import Process, Queue , Pipe
import subprocess
import ex_A
import ex_B
import pychoral

def run_A():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = A
    return ex_A.Conv_A()

def run_B():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = B
    return ex_B.Conv_B()

if __name__ == "__main__":
    pychoral.start_processes(run_A, run_B)