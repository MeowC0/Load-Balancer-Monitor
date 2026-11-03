Load Balancer Monitor

OPS435 Assignment 2 by Melanie Chu.

A small Python program that models a load balancing setup on a single subnet and reports whether its nodes are online. It is the beginning of what could one day become a real monitoring system.

What it does
Represents each device (computer, virtual machine, etc.) as a Node with an IP address.
Checks whether an IP address is valid and whether the node answers a ping.
Keeps one master node and a list of slave nodes in a LoadBalancerMonitor.
Adds and removes slaves, and prints a status summary for the whole setup.
Files
File	Description
load_balancer_monitor_ckhna.py	The single source file containing both classes
README.md	This file
Requirements
Python 3
The ping command (on Debian/Ubuntu: sudo apt-get install iputils-ping)

The program uses ping -W 2 -c 1, which waits at most two seconds for one reply. If ping is missing or blocked, every node will be reported as OFFLINE.

Classes
Node
Member	Description
ip	The node's IP address, stored as a string
__init__(ip)	Builds a node from an IP address string
canExist()	Returns True if the IP has exactly four dot-separated octets, each a number from 0 to 254, with the first and last octets not zero. Otherwise returns False
isRunning()	Pings the node once (maximum two seconds) and returns True if it replies, False otherwise
LoadBalancerMonitor
Member	Description
networkAddress	The subnet's network address, as a string
bitmask	The network bitmask, as an int
master	The master Node
slaves	A list of slave Node objects
__init__(networkAddress, bitmask, master)	Builds the monitor with an empty slave list
addSlave(node)	Adds the node to slaves if canExist() is true, otherwise prints an error message
removeSlave(slave)	Removes the slave from slaves if present, matching by IP address
getStatus()	Prints the status summary (see below)
Usage
python
from load_balancer_monitor_ckhna import Node, LoadBalancerMonitor

master = Node("1.1.1.1")
monitor = LoadBalancerMonitor("1.1.1.0", 24, master)

monitor.addSlave(Node("127.0.0.1"))
monitor.addSlave(Node("127.0.0.2"))
monitor.addSlave(Node("127.0.0.3"))

monitor.removeSlave(Node("127.0.0.2"))

monitor.getStatus()

getStatus() prints one dot after "Checking" for each node checked (the master plus every slave), then the summary:

Checking...

Load Balancer Status
====================
Master: ONLINE
Slaves: 2 ONLINE, 0 OFFLINE

The master is ONLINE only when its IP is valid and it answers a ping. Slaves are counted as ONLINE when they answer a ping.

Running and testing

Run the file with Python (not directly with ./, unless the file has a shebang line):

python3 load_balancer_monitor_ckhna.py

The test code that checks the classes can be placed at the bottom of the file under if __name__ == "__main__":. Some useful checks:

Node("0.168.0.1").canExist() is False (first octet is 0)
Node("192.168.0.0").canExist() is False (last octet is 0)
Node("192.168.1").canExist() is False (only three octets)
Node("192.268.0.1").canExist() is False (octet over 254)
Node("10.4.45.100").canExist() is True
Adding Node("127.0.0.0") as a slave prints an error message and does not add it
Reference
OPS435 Assignment 2 - assignment specification
