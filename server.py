import sys
from time import sleep
### library ###
import time
import threading
import ctrl_socket
import utils


serverPort = 10080
def timecheck():
    global table_lock
    while True:
        termkey = {}
        table_lock.acquire()
        for key in IPTABLE:
            key[1] = key[1] + 1
            if key[1] > 30:
                termkey[key] = 1
        for key in termkey:
            IPTABLE.del(key)
            print(key, ' is disconnected')
        table_lock.release()
        sleep(1)
        if termserver:
            return
        
def server():
    """
    Write your code!!!
    """
    global table_lock, termserver
    print('server started...')
    IPTABLE = {}
    table_lock = threading.lock(); termserver = 0
    timecheck()
    server_socket = ctrl_socket.ctrl_socket(('', serverPort))
    
    while True:
        
    


"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()


