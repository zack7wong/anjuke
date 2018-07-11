# -*- coding: utf-8 -*-
import time, threading
# 创建多线程两种方法
# 1.把一个函数传入并创建Thread实例，然后调用start()开始执行

def thread_run(urls):
    print('22 current %s is running...' % threading.current_thread().name)
    for url in urls:
        print('%s ---> %s' %(threading.current_thread().name,url))
        time.sleep(1)
    print('%s ended. ' % threading.current_thread().name)

print('11 %s is running...' % threading.current_thread().name)
t1 = threading.Thread(target=thread_run,name='thread-1',args=(['url1','url2','url3'],))
t2 = threading.Thread(target=thread_run,name='thread-2',args=(['url4','url5','url6'],))
t1.start()
t2.start()
t1.join()
t2.join()
print('%s ended.' % threading.current_thread().name)

