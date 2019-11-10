import socket

class NodeServer:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.mySocket = socket.socket()
        self.clients = dict()

    def listen(self):

        self.mySocket.bind((self.ip, self.port))
        self.mySocket.listen(5)  
        print('Started listening on: ', (self.ip, self.port))

        while True:

            conn, addr = self.mySocket.accept()
            print ('Client Connected: ', addr)


class NodeClient:

    def __init__(self, ip, port, host):

        self.ip = name
        self.port = port
        self.host = host
        self.mySocket = socket.socket()

    def connect(self):

        self.connect(host)
