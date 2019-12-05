import os
import socket
import asyncio
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

            # code for server side functions goes here


class NodeClient:

    def __init__(self, ip, port, node, backup):

        self.ip = ip
        self.host = tuple()
        self.port = port
        self.node = node
        self.mySocket = socket.socket()
        self.backup = backup

    def get(self):

        loop = asyncio.new_event_loop()
        while 1:
           
            key = input("Enter the key you want to retrieve: \n")
            result = loop.run_until_complete(self.node.get(key))
            print("This logical volume belongs to: ", result)
            #self.mySocket.connect(('0.0.0.0', result))
            
