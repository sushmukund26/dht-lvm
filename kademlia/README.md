**Documentation for Kademlia can be found at [kademlia.readthedocs.org](http://kademlia.readthedocs.org/).**

This library is an asynchronous Python implementation of the [Kademlia distributed hash table](http://en.wikipedia.org/wiki/Kademlia).  It uses the [asyncio library](https://docs.python.org/3/library/asyncio.html) in Python 3 to provide asynchronous communication.  The nodes communicate using [RPC over UDP](https://github.com/bmuller/rpcudp) to communiate, meaning that it is capable of working behind a [NAT](http://en.wikipedia.org/wiki/Network_address_translation).

This library aims to be as close to a reference implementation of the [Kademlia paper](http://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) as possible.


All of the following must be executed inside the kademlia folder
## Installation

make sure you have python3 and pip3 installed on your pc

run the following commands:
```
pip3 install -r requirements.txt
pip3 install -r dev-requirements.txt
```

## Usage

The following commands creates one node in the DHT
```
python3 dht_node.py <bootstrap-ip> <bootstrap-port> <own port>
```
The following commands can be used to set keys and their values on the DHT
```
python3 set.py <bootstrap-ip> <bootstrap-port> <key> <value>
```
The following commands can be used to get the value of a key from the DHT
```
python3 get.py <bootstrap-ip> <bootstrap-port> <key> 
```

