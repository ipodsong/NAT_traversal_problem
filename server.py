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
        
def recv_data(c_socket):
    while True:
        data, addr = c_socket.recv_data()
        if data != 0:
            pass

def server():
    """
    Write your code!!!
    """
    global table_lock, termserver
    print('server started...')
    
    ## set parameter
    IPTABLE = {}
    table_lock = threading.lock(); termserver = 0
     
    ## create socket    
    server_socket = ctrl_socket.ctrl_socket(('', serverPort))
    
    ## start timecheck thread
    tcheck = threading.Thread(target=timecheck)
    tcheck.start()
    
    ## start receive data thread
    th_recv_data = threading.Thread(target=recv_data, args=(server_socket))
    th_recv_data.start()
   
    
    while True:
        cmd = input("")
        if cmd == 'quit':
            termserver = 1
            break
    


"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()


