import sys
### library ###
import socket

### user library ###
import ctrl_socket
import utils

serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081

# mode
# 0 : send CID
# 1 : request list
# 2 : send chat
# 3 : send keep alive
def client(serverIP, serverPort, clientID):
    client_socket = ctrl_socket.ctrl_socket(('', clientPort))

    # 서버에 CID 전송
    data = utils.make_data(0, clientID)
    client_socket.send_data((serverIP, serverPort), data)
    
    
    pass


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("")
    client(serverIP, serverPort, clientID)


