import sys
from time import sleep
### library ###
import time
import threading
### user library ###
import ctrl_socket
import utils

# global variables
serverPort = 10080

# send created or removed Client_ID to the other Client    
def send_CID(s_socket, mode, CID):
    # mode
    # 0 : created
    # 1 : removed
    global client_table
    data = utils.make_data(mode, CID)
    for key in client_table:
        s_socket.send_data(client_table[key][0], data)   # client_table[key] : [adress, timer]
 
def check_timeout(s_socket):
    global table_lock, client_table, termserver
    while True:
        del_key = {}
        table_lock.acquire()
        ## run time
        for key in client_table:
            client_table[key][1] = client_table[key][1] + 1
            if client_table[key][1] > 30:
                del_key[key] = 1
        ## delete key 
        for key in del_key:
            client_table.pop(key)           ## delete key
            print(key, 'is disappeared')  ## client connection is dead by 30s timeout
            # send removed CID to the other client
            send_CID(s_socket, 1, key)
            
        table_lock.release()
        ## time sleep 1s
        sleep(1)
        ## server is terminated
        if termserver:
            return

# save received Client_ID
def saveCID(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    client_table[CID] = [address, 0]  ## dic[key = client_ID] = [address, time]
    # send created CID to the other Client
    send_CID(s_socket, 0, CID)
    table_lock.release()
    print(CID, address)

        
        

# reset timer for Client_ID    
def reset_time(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    client_table[CID][1] = 0
    table_lock.release()

# remove info about Client_ID    
def rm_timer(s_socket, address, CID):
    global table_lock, client_table
    table_lock.acquire()
    if CID in client_table:
        client_table.pop(CID)
        # send created CID to the other client
        send_CID(s_socket, 0, CID)
        
    table_lock.release()
    
    print(CID, 'is unregistered')

# reveive data from client    
def recv_data(s_socket):
    global termserver
    # mode
    # 0 : recv CID
    # 1 : recv rm CID
    # 2 : recv chat
    # 3 : recv keep alive
    # 4 : recv exit
    # response mode
    mode2cmd = { 0 : saveCID,    \
                 3 : reset_time, \
                 4 : rm_timer    \
               }
    
    while True:
        data, addr = s_socket.return_data()
        
        # if server is terminated
        if termserver:
            return        
        # if data is none
        if len(data) == 0:
            continue

        # unpack data
        mode, unpacked = utils.unpack_data(data.decode())
        # response
        mode2cmd[mode](s_socket, addr, unpacked)
        
        

def server():
    ## set global variables
    global table_lock, termserver, client_table
    print('server started...')
    
    ## set variables
    client_table = {} ### dataform : {client_ID : [client_address, time]}
    table_lock = threading.Lock(); termserver = 0
     
    ## create socket    
    server_socket = ctrl_socket.ctrl_socket(('', serverPort), 'server')
    
    ## start check_timeout thread
    tcheck = threading.Thread(target=check_timeout, args=(server_socket,))
    tcheck.start()
    
    ## start receive data thread
    th_recv_data = threading.Thread(target=recv_data, args=(server_socket,))
    th_recv_data.start()
   
    
    while True:
        cmd = input("")
        if cmd == 'quit':
            # server was terminated
            termserver = 1
            break
    


"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()


