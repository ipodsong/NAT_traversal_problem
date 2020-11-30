import sys
### library ###
import socket
import threading
import time
### user library ###
import ctrl_socket
import utils

# global variables
serverIP = '127.0.0.1'
serverPort = 10080
clientPort = 10081

# mode
# 0 : send CID
# 1 : request list
# 2 : send chat
# 3 : send keep alive
# 4 : send exit
# 5 : send res list

###### thread 함수 ######
# send keep alive to server
def send_alive(c_socket, server_address):
    global cli_term
    data = utils.make_data(3, clientID)
    while True:
        # wait for 10s
        time.sleep(10)
        # send client is alive
        c_socket.send_data(server_address, data)
        if cli_term:
            # client is terminated
            return

# receive data    
def recv_data(c_socket):
    print("recv_data_init")
    # mode
    # 2 : recv chat
    # 5 : recv res list
    mode2cmd = { 2 : print_chat, \
                 5 : print_list  \
               }
    while True:
        data, addr = c_socket.return_data() 
        if len(data) == 0:
            continue

        # unpack data to mode and message
        mode, msg = utils.unpack_data(data.decode())
        
        # execute function
        mode2cmd[mode](msg)
###### thread 함수 ######

###### print 함수 ######
# reveive message from other client
def print_chat(msg):
    # 채팅 메세지 console에 표시
    # ex) From client [msg]
    print('from ', msg[0], '[{}]'.format(msg[1]))
    
    
# receive all clinet list from server
def print_list(msg):
    global client_table
    # reset client info table
    client_table = {}
    for key in msg:
        print(key)
        # add client info to client_table
        client_table[key[0]] = key[1]
###### print 함수 ######
        
###### send function ######      
# request all client list to server
def request_list(socket, address, cid, msg):
    data = utils.make_data(1, cid)  
    socket.send_data(address, data)

# send message to other client
def send_msg(socket, address, cid, msg):
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
    mode = splited[0]; CID = splited[1]; msg = splited[-2]
        
    if CID in client_table:
        address = client_table[CID]
        
    return mode, address, msg

def client(serverIP, serverPort, clientID):
    # client init
    print("Init client")
    global client_table, cli_term
    cli_term = 0
    client_table = {} ## client_table dataform : { clientID : client_address} 
    
    # 함수 dic
    cmd2mode = {'@show_list':request_list, \
                 '@chat':send_msg, \
                 '@exit':send_exit \
                }
    
    #소켓 생성
    try:
        print("Make socket...")
        server_address = (serverIP, serverPort)
        client_socket = ctrl_socket.ctrl_socket(('', clientPort))
        print("Make socket completed")
    except:
        print("Make socket failed")
        exit(0)

    # data 받는 thread 생성
    th_recv_data = threading.Thread(target=recv_data, args=(client_socket, ))
    th_recv_data.start()

    # 서버에 CID 전송
    try:
        print("Send CID to server...")
        data = utils.make_data(0, clientID)
        client_socket.send_data(server_address, data)
        print("Send CID to server completed")
    except:
        print("Send CID to server failed")
        exit(0)

    # sending alive thread 생성
    th_send_alive = threading.Thread(target=send_alive, args=(client_socket, server_address))
    th_send_alive.start()

    print("Init client completed")
    print("Start Shell...")
    while True:
        cmd = input("shell >> ")
        # 입력받은 command parsing
        mode, address, msg = splitcmd(cmd, server_address)
        
        # command 예외처리
        if mode not in cmd2mode:
            continue
        
        # command에 맞는 함수 
        cmd2mode[mode](client_socket, address, clientID, msg)
        
        if mode == '@exit':
            # client was terminated
            cli_term = 1
            break


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


