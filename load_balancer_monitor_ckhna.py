#!/usr/bin/env python3
# OPS435 Assignment 2
# load_balancer_monitor_ckhna.py
# Author: Melanie Chu
import subprocess
#Create Node Class
class Node:
    """Represents one device (computer, VM, etc.) in the load balancer."""
    def __init__(self, ip):
        # Store the IP address as a string, e.g. "192.168.0.1"
        self.ip = str(ip)
     

    def canExist(self):
        """Return True if self.ip is a valid IP address, otherwise False."""
        # Split "192.168.0.1" into ["192", "168", "0", "1"]
        octets = self.ip.split(".") 

        # Check 1: there must be exactly four octets 
        if len(octets) != 4:
            return False

        # Check 2: every octet must be a whole number from 0 to 254
        numbers = []
        for octet in octets:
            # isdigit() rejects empty strings, letters and negative signs,
            # which would crash int() or slip through
            if not octet.isdigit():
                return False
            number = int(octet)
            if number < 0 or number >= 255:
                return False
            numbers.append(number)
 
        # Check 3: the first octet (index 0) cannot be zero
        # Check 4: the last octet (index 3) cannot be zero
        if numbers[0] == 0 or numbers[3] == 0:
            return False
 
        # Every check passed
        return True

    def isRunning(self):
        """Ping the node once, waiting at most 2 seconds. True if it replies."""
        # getstatusoutput() runs the shell command and returns a tuple:
        # (return code, output text). Return code 0 means the ping succeeded.
        status, output = subprocess.getstatusoutput("ping -W 2 -c 1 " + self.ip)
        if status == 0:
            return True
        else:
            return False




class LoadBalancerMonitor:
    """Monitors one master Node and a list of slave Nodes on a subnet."""

    def __init__(self, networkAddress, bitmask, master):
        # Network address as a string
        self.networkAddress = str(networkAddress)
        # Bitmask as an integer
        self.bitmask = int(bitmask)
        # The master is a Node object
        self.master = master
        # The slaves list must be created here in __init__ so that it
        # belongs to the object and keeps its contents between method calls.
        self.slaves = []

    def addSlave(self, node):
        """Add a Node to the slaves list if its IP address is valid."""
        if node.canExist():
            self.slaves.append(node)
        else:
            print("Error: " + node.ip + " is not a valid IP address, slave not added")

    def removeSlave(self, slave):
        """Remove the slave from the slaves list if it is in there."""
        for exist_slave in self.slaves:
            if exist_slave.ip == slave.ip:
                self.slaves.remove(exist_slave)
                break

    def getStatus(self):
        """Print the status of the master and all of the slaves."""
        # Print "Checking" and add one dot for each node checked.
        # end="" stops the newline and flush=True shows each dot immediately.
        print("Checking", end="", flush=True)

        # Check the master: it is online only if its IP is valid AND it pings
        if self.master.canExist() and self.master.isRunning():
            master_online = True
        else:
            master_online = False
        print(".", end="", flush=True) #one dot for the master

        # Check each slave and count how many are up and down
        count_online = 0
        count_offline = 0
        for slave in self.slaves:
            if slave.isRunning():
                count_online = count_online + 1
            else:
                count_offline = count_offline + 1
            print(".", end="", flush=True) #one dot per slave
        # Finish the "Checking....." line, then leave a blank line
        print()
        print()

        # Print the summary
        print("Load Balancer Status")
        print("====================")
        if master_online:
            print("Master: ONLINE")
        else:
            print("Master: OFFLINE")
        print("Slaves: " + str(count_online) + " ONLINE, " + str(count_offline) + " OFFLINE")
 
if __name__ == "__main__":

    print(Node("192.168.0.255").canExist())   # False: 255 is not allowed
    print(Node("10.a.0.1").canExist())        # False: non-numeric octet
    print(Node("10.0.0.1.5").canExist())      # False: five octets
    print(Node("1.0.0.254").canExist())       # True: lowest and highest allowed values

    # removeSlave on a node that was never added (should do nothing, no crash)
    monitor = LoadBalancerMonitor("1.1.1.0", 24, Node("127.0.0.1"))
    monitor.removeSlave(Node("127.0.0.9"))
    print(len(monitor.slaves))                # 0

    # add one slave, remove it, list should be empty again
    monitor.addSlave(Node("127.0.0.2"))
    monitor.removeSlave(Node("127.0.0.2"))
    print(len(monitor.slaves))                # 0

    # add three slaves for the status check
    monitor.addSlave(Node("127.0.0.1"))
    monitor.addSlave(Node("127.0.0.2"))
    monitor.addSlave(Node("127.0.0.3"))
    print(len(monitor.slaves))                # 3

    # getStatus with three slaves
    monitor.getStatus()                       # Slaves: 3 ONLINE, 0 OFFLINE (if ping works)