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
def recv_data(c_socket):
    while True:
        data = c_socket.recv_data()
        if data != 0:
            pass

def request_list(socket, address):
    data = utils.make_data(1, '')
    socket.send_data(address, data)

def send_msg(socket, address, msg):
    socket.send_data(address, msg)

def send_exit(socket, address):
    socket.send_data(address, 'exit')

def client(serverIP, serverPort, clientID):
    # client init
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
    


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


