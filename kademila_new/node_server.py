import os
import socket
import asyncio
import threading
import pickle
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

                print("Enter 0 to exit")
                print("Enter 1 to list all files")
                print("Enter 2 to get a file")
                print("Enter 3 to put a file")
                key = input("Enter: ")

                mySocket.send(key.encode())

                if key == '0':
                    break

                data = pickle.loads(mySocket.recv(512))

                print(data)


            mySocket.close()


def onConnection(clientSocket, clientAddr):

    #do something on connection

    lv = clientSocket.recv(512)
    userLv = os.getcwd() + "/" + lv.decode()
    print (userLv)

    while 1:

        mode = clientSocket.recv(512).decode()

        if mode == '0':
            exit(0)
        elif mode == '1':
            #list all the contents of the logical volume
            print ("mode 1")
            data=pickle.dumps(os.listdir(userLv))
            clientSocket.send(data)
        elif mode == '2':
            #access a file from the logical volume
            print ("mode 2")
        elif mode == '3':
            #put a file in the logical volume
            print ("mode 3")
