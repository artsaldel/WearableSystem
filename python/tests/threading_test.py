import threading
import time

def Function1(lock):
    while(True):
        with lock:
            print("Function 1")
        time.sleep(1)


def Function2(lock):
    while(True):
        with lock:
            print("Function 2")
        time.sleep(1)

lock = threading.Lock()
thread1 = threading.Thread(target = Function1, name = " 1", args=(lock,))
thread2 = threading.Thread(target = Function2, name = " 2", args=(lock,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()