import sys
from time import sleep
### library ###
import time
import threading
import ctrl_socket
import utils


serverPort = 10080
# global variables

def check_timeout():
    global table_lock, client_table, termserver
    while True:
        del_key = {}
        table_lock.acquire()
        for key in client_table:
            client_table[key][1] = client_table[key][1] + 1
            if client_table[key][1] > 30:
                del_key[key] = 1
                
        for key in del_key:
            client_table.del(key)
            print(key, ' is disconnected')  ## client connection is dead by 30s timeout
            
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
    ## set global variables
    global table_lock, termserver, client_table
    print('server started...')
    
    ## set variables
    client_table = {} ### dataform : {client_ID : [client_address, time]}
    table_lock = threading.lock(); termserver = 0
     
    ## create socket    
    server_socket = ctrl_socket.ctrl_socket(('', serverPort))
    
    ## start check_timeout thread
    tcheck = threading.Thread(target=check_timeout)
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


