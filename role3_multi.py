from role import *
#from multiprocessing import Process, Queue , Pipe
import role3_A, role3_B, role3_C
import pychoral3


def run_A():
    conv_a = role3_A.Conv_A()
    #conv_a.f()
    v = conv_a.f(100)
    print(v)

def run_B():
    conv_b = role3_B.Conv_B()
    conv_b.f()
    #v = conv_b.f()
    #print(v)

def run_C():
    conv_c = role3_C.Conv_C()
    conv_c.f()
    #v = conv_c.f()   
    #print(v)

if __name__ == "__main__":
    pychoral3.start_processes(run_A, run_B, run_C)