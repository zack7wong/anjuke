# http://blog.csdn.net/jinping_shi/article/details/52433867

import multiprocessing
import time


def func(msg):
    print(multiprocessing.current_process().name + '--' + msg)
    # time.sleep(0.2)
    # print(multiprocessing.current_process().name + '-' + msg)

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=10) # 创建4个进程
    results = []
    for i in range(101):
        msg = "hello %d" %(i)
        pool.apply_async(func, (msg, ))
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()  # 等待进程池中的所有进程执行完毕
    print("Sub-process(es) done.")
    # for res in results:
    #     print (res.get())