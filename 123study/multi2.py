# -*- coding: utf-8 -*-
import time, threading
# 创建多线程两种方法
# 2.从 threading.Thread继承创建线程类,然后重写__init__方法和 run方法

class myThread(threading.Thread):
    def __init__(self,name,urls):
        threading.Thread.__init__(self,name=name)
        self.urls = urls

    def run(self):
        print('22 current %s is running...' % threading.current_thread().name)
        for url in self.urls:
            print('%s ---> %s' % (threading.current_thread().name, url))
            time.sleep(1)
        print('%s ended. ' % threading.current_thread().name)

print('11 %s is running...' % threading.current_thread().name)

t1 = myThread(name='thread-1',urls=['url1','url2','url3'])
t2 = myThread(name='thread-2',urls=['url4','url5','url6'])
t1.start()
t2.start()
t1.join()
t2.join()
print('%s ended.' % threading.current_thread().name)

