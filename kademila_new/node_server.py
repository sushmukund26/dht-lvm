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
        self.mySocket.listen(20)  
        print('Node server is listening on: ', (self.ip, self.port), '\n')

        while True:

            conn, addr = self.mySocket.accept()
            self.clients[addr] = conn
            print ('Client Connected: ', addr, '\n')
            threading.Thread(target=onConnection, args=(conn, addr)).start()

class NodeClient:

    def __init__(self, ip, port, node):

        self.ip = ip
        self.host = tuple()
        self.port = port
        self.node = node
        self.mySocket = socket.socket()
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
                elif key == '1':
                    data = pickle.loads(mySocket.recv(512))
                    print (data)
                elif key == '2':
                    fileName = input("Enter file name: ")
                    mySocket.send(fileName.encode())
                    recvFile(mySocket, fileName)
                elif key == '3':
                    filePath = input("Enter file path: ")
                    fileName = filePath.split("/")[-1]
                    mySocket.send(fileName.encode())
                    clientSend(mySocket, filePath)

            mySocket.close()


def onConnection(clientSocket, clientAddr):

    #do something on connection

    lv = clientSocket.recv(512)
    userLv = os.getcwd() + "/" + lv.decode()
    recvFolder = userLv + "/received" 
    # print (userLv)

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
            fileName = clientSocket.recv(512).decode()
            sendFile(clientSocket, fileName, userLv)
        elif mode == '3':
            #put a file in the logical volume
            print ("mode 3")
            fileName = clientSocket.recv(512).decode()
            serverRecv(clientSocket, fileName, recvFolder)

def sendFile(socket, fileName, filePath):

    f = open(filePath+"/"+fileName, 'rb')
    print('Sending ...')
    l = f.read(1024)

    while (l):
        print('Sending ...')
        socket.send(l)
        l = f.read(1024)
    
    f.close()
    print ('Done Sending')


def recvFile(socket, fileName):

    f = open(fileName, 'wb')
    print('Receiving ...')

    l = socket.recv(1024)
    while (l):
        print ('Receiving ... ')
        f.write(l)
        if len(l) < 1024:
            break
        l = socket.recv(1024)

    f.close()
    print ('Done Receiving')

def serverRecv(socket, fileName, folder):

    f = open(folder+"/"+fileName, 'wb')
    print('Receiving ...')

    l = socket.recv(1024)
    while (l):
        print ('Receiving ... ')
        f.write(l)
        if len(l) < 1024:
            break
        l = socket.recv(1024)

    f.close()
    print ('Done Receiving')

def clientSend(socket, filePath):

    f = open(filePath, 'rb')
    print('Sending ...')
    l = f.read(1024)

    while (l):
        print('Sending ...')
        socket.send(l)
        l = f.read(1024)
    
    f.close()
    print ('Done Sending')
