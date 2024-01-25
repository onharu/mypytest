from role import *
from multiprocessing import Process, Queue , Pipe
import check_S, check_C
import pychoral2

def run_S():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = A
    conv_a = check_S.Check_S()
    conv_a.check(2000)

def run_C():# プロジェクション後のファイル(class)を呼び出す
    #pychoral.myrole = B
    conv_b = check_C.Check_C()
    v = conv_b.check(1000)
    print(v)

if __name__ == "__main__":
    pychoral2.start_processes(run_S, run_C)