import os
import socket
import asyncio
import threading
from kademlia.network import Server

class NodeServer:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.mySocket = socket.socket()
        self.clients = dict()



    def listen(self):

        self.mySocket.bind((self.ip, self.port))
        self.mySocket.listen(5)  
        print('Node server is listening on: ', (self.ip, self.port), '\n')

        while True:

            conn, addr = self.mySocket.accept()
            print ('Client Connected: ', addr, '\n')
            threading.Thread(target=onConnection, args=(conn, addr)).start()
        



class NodeClient:

    def __init__(self, ip, port, node, backup):

        self.ip = ip
        self.host = tuple()
        self.port = port
        self.node = node
        self.mySocket = socket.socket()
        self.backup = backup

        self.mySocket.bind((self.ip, self.port))


    def get(self):

        loop = asyncio.new_event_loop()
        while 1:

            mySocket = socket.socket()

            key = input("Enter the key you want to retrieve: \n")
            result = loop.run_until_complete(self.node.get(key))
            print("This logical volume belongs to: ", result)
            mySocket.connect(('0.0.0.0', result))
            mySocket.send(key.encode())

            while 1:

                key = input("Input 0 to exit \n Input 1 to see all files in a volume \n Input 2 to Rretrieve a file \n Input 3 to put a file")
                mySocket.send(key.encode())



            mySocket.close()


def onConnection(clientSocket, clientAddr):

    #do something on connection

    lv = clientSocket.recv(512)
    print ('Entered Different thread')
    print (os.getcwd() + "/"  +lv.decode())

    while 1:

        mode = clientSocket.recv(512).decode()

        if mode == '1':
            print ("mode 1")
        elif mode == '2':
            print ("mode 2")
        elif mode == '3':
            print ("mode 3")

        exit(0)

        # print (os.listdir(os.getcwd()))

                
            
