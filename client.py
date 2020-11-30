import sys
### library ###
import socket
import threading
### user library ###
import ctrl_socket
import utils

serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081

# global variables

# mode
# 0 : send CID
# 1 : request list
# 2 : send chat
# 3 : send keep alive
# 4 : send exit
# 5 : send res list


def recv_chat(msg):
    # 채팅 메세지 console에 표시
    # ex) From client [msg]
    print('from ', msg[0], '[{}]'.format(msg[1]))
    
def recv_list(msg):
    # 주석 필요
    global client_table
    client_table = {}
    for key in msg:
        print(key)
        # 주석 필요
        client_table[key[0]] = key[1]
    
    
def recv_data(c_socket):
    # mode
    # 2 : recv chat
    # 5 : recv res list
    mode2cmd = { 2 : recv_chat, \
                 5 : recv_list  \
               }
    while True:
        data, addr = c_socket.recv_data() 
        if data != 0:
            pass

        # 주석 필요
        mode, msg = utils.unpack_data(data.decode())
        
        mode2cmd[mode](msg)

        
### send func ###        
def request_list(socket, address, cid, msg):
    data = utils.make_data(1, cid)  
    socket.send_data(address, data)

def send_msg(socket, address, cid, msg):
    data = utils.make_data(2, [cid, msg])  
    socket.send_data(address, data)

def send_exit(socket, address, cid, msg):
    data = utils.make_data(4, cid)   
    socket.send_data(address, data)    
    
def splitcmd(cmd, address):
    global client_table
    splited = (cmd+' ').split(' ')
    mode = splited[0]; CID = splited[1]; msg = splited[-2]
        
    if CID in client_table:
        address = client_table[CID]
        
    return mode, address, msg

def client(serverIP, serverPort, clientID):
    # client init
    global client_table
    client_table = {} ## dataform : {another clientID : another client_address} 
    
    cmd2mode = {'@show_list':requst_list, \
                 '@chat':send_msg, \
                 '@exit':send_exit \
                }
    
    server_address = (serverIP, serverPort)
    client_socket = ctrl_socket.ctrl_socket(('', clientPort))

    # data 받는 thread 생성
    th_recv_data = threading.Thread(target=recv_data, args=(client_socket))
    th_recv_data.start()
    
    # 서버에 CID 전송
    data = utils.make_data(0, clientID)
    client_socket.send_data(server_address, data)

    while True:
        
        cmd = input("shell >> ")
        
        mode, address, msg = splitcmd(cmd, server_address)
        
        if mode not in cmd2mode:
            pass
            
        cmd2mode[mode](client_socket, address, clientID, msg)
        
        if mode == '@exit':
            break


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


