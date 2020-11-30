import sys
from time import sleep
### library ###
import time
import threading
### user library ###
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

def saveCID(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    client_table[CID] = [address, 0]
    table_lock.release()
    print(CID, address)

def reslist(s_socket, address, CID):
    global table_lock, client_table
    table = []
    table_lock.acquire()
    for key in client_table:
        table.append([key,client_table[key][0]])
    table_lock.release()
    
    data = utils. make_data(5, table)
    s_socket.send_data(address, data)
    
def reset_time(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    client_table[CID][1] = 0
    table_lock.release()
    
def rm_timer(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    if CID in client_table:
        client_table.del(CID)
    table_lock.release()
    print(CID, ' is unregistered')
    
def recv_data(s_socket):
    global termserver
    # mode
    # 0 : recv CID
    # 1 : recv req list
    # 2 : recv chat
    # 3 : recv keep alive
    # 4 : recv exit
    # 5 : recv res list
    mode2cmd = { 0 : saveCID, \
                 1 : reslist, \
                 3 : reset_time, \
                 4 : rm_timer \
               }
    
    while True:
        data, addr = s_socket.recv_data()  ## 아마도 이 부분 수정해야할지도
        
        if termserver:
            return        
        
        if data != 0:
            pass
        
        mode, unpacked = utils.unpackdata(data.decode())
        
        mode2cmd[mode](s_socket, addr, unpacked)
        
        

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


