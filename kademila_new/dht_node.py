import random
import asyncio
import logging
import argparse
import threading

from node_server import NodeServer
from node_server import NodeClient

from kademlia.network import Server

numNodes = 0

# Commandline arguments
parser = argparse.ArgumentParser()
# parser.add_argument('ip', type=str, help='ip address of the node you want to connect to')
parser.add_argument('port', type=int, help='port number of the node you want to connec to')
parser.add_argument('host', type=int, help='your own port number')
parser.add_argument('key', type=str, help='comma separated list of logical volumes/folders to share')
# parser.add_argument('value', type=str, help='Value to be associated with that key')

# Get commandline args
args = parser.parse_args()

myLogicalVolumes = list(args.key.split(",")) 

# Set up screen logger
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log = logging.getLogger('kademlia')
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)
    
# Get Async event loop
loop = asyncio.get_event_loop()

# Set logging to TRUE
# loop.set_debug(True)

# Create NODE in our DHT
node = Server()
numNodes = numNodes + 1

# Set up a "backup" machine for newly added node
# backup = random.randint(1,numNodes)
# print('Backup machine for machine',numNodes,'is machine',backup)

# Start listening on the given PORT
loop.run_until_complete(node.listen(args.host))

# Bootstrap the node by connecting to other known nodes, in this case
# replace 123.123.123.123 with the IP of another node and optionally
# give as many ip/port combos as you can for other nodes.
loop.run_until_complete(node.bootstrap([('0.0.0.0', args.port)]))
print ('DHT node running on ', ('0.0.0.0', args.host))

# set a value for the key "my-key" on the network

for lv in myLogicalVolumes:
    loop.run_until_complete(node.set(lv, args.host+1))

# get the value associated with "my-key" from the network
#result = loop.run_until_complete(node.get("my-key"))
#print(result)

client_server = NodeServer("0.0.0.0", args.host+1)
client = NodeClient("0.0.0.0", args.host+2, node, 0)
thread1 = threading.Thread(target=client_server.listen)
thread2 = threading.Thread(target=client.get)
print ('Node client running on ', ('0.0.0.0', args.port+2))

thread1.start()
thread2.start()

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    node.stop()
    loop.close()
