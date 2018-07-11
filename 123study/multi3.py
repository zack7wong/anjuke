# -*- coding: utf-8 -*-
#coding=utf-8
import threading
from time import ctime,sleep


def music(func):
    for i in range(2):
        print( "I was listening to %s. %s" %(func,ctime()))
        sleep(1)

def move(func):
    for i in range(5):
        print ("I was at the %s! %s" %(func,ctime()))
        print('current %s is running...' % threading.current_thread().name)
        sleep(0.2)

threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
for i in range(5):
    t2 = threading.Thread(target=move,args=(u'阿凡达',))
    threads.append(t2)
# t3 = threading.Thread(target=move,args=(u'阿斯顿发生',))
# threads.append(t3)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print ("all over %s" %ctime())