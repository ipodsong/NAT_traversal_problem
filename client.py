### library ###
import sys
import signal
import socket
import threading
import time
import re
### user library ###
import ctrl_socket
import utils

# global variables
serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081

# mode
# 0 : send CID
# 1 : send rm CID
# 2 : send chat
# 3 : send keep alive
# 4 : send exit

###### thread 함수 ######
# send keep alive to server
def send_alive(c_socket, server_address):
    global exit_flag
    data = utils.make_data(3, clientID)
    while True:
        # wait for 10s
        for i in range(10):
            if exit_flag == 1:
                break
            time.sleep(1)
        if exit_flag == 1:
            break
        # send client is alive
        c_socket.send_data(server_address, data)
    print("send_alive thread terminated")

# receive data    
def recv_data(c_socket):
    #print("recv_data_init")
    # mode
    # 0 : recv add CID
    # 1 : recv rm CID
    # 2 : recv chat
    mode2cmd = { 0 : add_CID, \
                 1 : rm_CID, \
                 2 : print_chat \
               }
    while True:
        if exit_flag == 1:
            break
        data, addr = c_socket.return_data() 
        if len(data) == 0:
            continue
        time.sleep(0.01)
        # unpack data to mode and message
        mode, msg = utils.unpack_data(data.decode())
        
        # execute function
        mode2cmd[mode](msg)
    print("recv_data thread terminated")
###### thread 함수 ######

###### client_table ######
# add CID in CID table
def add_CID(msg):
    global client_table
    CID, Addr = msg
    
    if CID not in client_table:
        client_table[CID] = Addr
        
# remove CID in CID table    
def rm_CID(msg):
    global client_table
    CID, _ = msg
    if CID in client_table:
        client_table.pop(CID)
###### client_table ######

###### print 함수 ######
# reveive message from other client
def print_chat(msg):
    # 채팅 메세지 console에 표시
    # ex) From client [msg]
    chat = ''.join(msg[1])
    print('from', msg[0], '[{}]'.format(chat))
    
    
# receive all clinet list from server
def print_list(socket, address, cid, msg):
    global client_table

    for key in client_table:
        print(key, client_table[key][0],':', client_table[key][1])
        
        
###### print 함수 ######


###### send function ######      
# send message to other client
def send_msg(socket, address, cid, msg):
    #print('addr',address[0],address[1])
    msg = ''.join(msg)
    #print('msg', msg)
    data = utils.make_data(2, [cid, msg])
    socket.send_data(address, data)

# send exit message to server    
def send_exit(socket, address, cid, msg):
    data = utils.make_data(4, cid) 
    socket.send_data(address, data)    
###### send function ######

# split commend to mode and data    
def splitcmd(cmd, address):
    global client_table
    # cmd : '@commend' or '@chat [otherclient] [message]'
    splited = (cmd+' ').split(' ')
    mode = splited[0]; CID = splited[1]; msg = splited[2:-1]
    msg = ' '.join(msg)
    if CID in client_table:
        address = client_table[CID]
    if len(CID.split('.')) == 4:
        address = (CID, clientPort)
    return mode, address, msg

def client(serverIP, serverPort, clientID):
    # client init
    # print("Init client")
    global client_table, exit_flag
    exit_flag = 0
    client_table = {} ## client_table dataform : { clientID : client_address} 
    
    # 함수 dic
    cmd2mode = {'@show_list':print_list, \
                 '@chat':send_msg, \
                 '@exit':send_exit \
                }
    
    #소켓 생성
    try:
    #    print("Make socket...")
        server_address = (serverIP, serverPort)
        client_socket = ctrl_socket.ctrl_socket(('', clientPort), 'client')
    #    print("Make socket completed")
    except:
        print("Make socket failed")
        exit(0)

    # data 받는 thread 생성
    th_recv_data = threading.Thread(target=recv_data, args=(client_socket, ))
    th_recv_data.start()
    time.sleep(0.1)
    # 서버에 CID 전송
    try:
    #    print("Send CID to server...")
        data = utils.make_data(0, [clientID, server_address])
        client_socket.send_data(server_address, data)
    #    print("Send CID to server completed")
    except:
        print("Send CID to server failed")
        exit(0)

    # sending alive thread 생성
    th_send_alive = threading.Thread(target=send_alive, args=(client_socket, server_address),)
    th_send_alive.start()

    print("Init client completed")
    print("Start Shell...")
    while True:
        cmd = input(">> ")
        sys.stdout.flush()
        # 입력받은 command parsing
        mode, address, msg = splitcmd(cmd, server_address)
        
        # command 예외처리
        if mode not in cmd2mode:
            continue
        
        # command에 맞는 함수 
        cmd2mode[mode](client_socket, address, clientID, msg)
        
        if mode == '@exit':
            # client was terminated
            exit_flag = 1
            del client_socket
            th_recv_data.join()
            th_send_alive.join()
            break
    print(clientID, "terminates")
    sys.exit()

"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


