import socket
import threading

class ctrl_socket:
    def __init__(self, address):
        # Variables
        self.data = ''
        self.exit = 0

        # class 생성 시 argument로 받는 address(ip, port)
        # bind, listen
        self.recv_Socket = socket.socket()
        self.recv_Socket.bind(address)
        self.recv_Socket.listen()
        # data를 받는 thread 생성
        self.th_recv_data = threading.Thread(target=self.recv_data)
        self.th_recv_data.start()

    def __del__(self):
        # 소멸자
        self.exit = 1
        self.recv_Socket.close()
        self.th_recv_data.join()

    def recv_data(self):
        # data 받고 저장
        while True:
            # class 종료 시 loop 종료
            if self.exit == 1:
                break

            # 데이터 받음
            recver, addr = self.recv_Socket.accept()
            recv_data = recver.recv(400)

            if len(recv_data) == 0:
                continue

            

    def send_data(self, address, data):
        # send 위한 socket 생성
        sender = socket.socket()
        sender.connect(address)
        sender.send(data.encode())



            