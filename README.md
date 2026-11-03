# Load Balancer Monitor

A small Python tool that checks whether the machines in a load balancing setup are up and running.

You tell it which machine is the **master** and which machines are the **slaves**, and with one command it pings them all and prints a simple summary.

*OPS435 Assignment 2 by Melanie Chu*

## Quick start

**1. Make sure you have what you need**

- Python 3
- The `ping` command. If it's missing, install it with:
  ```
  sudo apt-get update && sudo apt-get install -y iputils-ping
  ```

**2. Use it in Python**

```python
from load_balancer_monitor_ckhna import Node, LoadBalancerMonitor

# Create the master and the monitor
master = Node("1.1.1.1")
monitor = LoadBalancerMonitor("1.1.1.0", 24, master)

# Add some slaves
monitor.addSlave(Node("127.0.0.1"))
monitor.addSlave(Node("127.0.0.2"))
monitor.addSlave(Node("127.0.0.3"))

# Check everything
monitor.getStatus()
```

**3. Read the result**

```
Checking....

Load Balancer Status
====================
Master: ONLINE
Slaves: 3 ONLINE, 0 OFFLINE
```

Each dot after "Checking" is one machine being checked (the master plus every slave).

## How to run the file

```
python3 load_balancer_monitor_ckhna.py
```

Use `python3` to run it. Typing `./load_balancer_monitor_ckhna.py` won't work, because the terminal would try to read the Python code as shell commands.

## What you can do

| I want to... | Use |
|---|---|
| Add a slave | `monitor.addSlave(Node("10.0.0.5"))` |
| Remove a slave | `monitor.removeSlave(Node("10.0.0.5"))` |
| See the status of everything | `monitor.getStatus()` |
| Check if an IP address is valid | `Node("10.0.0.5").canExist()` |
| Check if one machine answers a ping | `Node("10.0.0.5").isRunning()` |

A few things worth knowing:

- Adding a slave with an invalid IP address (like `127.0.0.0`) doesn't add it. You'll see an error message instead.
- Removing a slave that was never added does nothing and doesn't cause an error.
- The master counts as ONLINE only when its IP address is valid **and** it answers a ping.

## What counts as a valid IP address?

An address like `192.168.0.1` is valid when:

- it has exactly four numbers separated by dots
- the first number is not 0
- the last number is not 0
- every number is between 0 and 254

| Address | Valid? | Why |
|---|---|---|
| `10.4.45.100` | Yes | Follows all the rules |
| `0.168.0.1` | No | First number is 0 |
| `192.168.0.0` | No | Last number is 0 |
| `192.168.1` | No | Only three numbers |
| `192.268.0.1` | No | 268 is too big |

## Troubleshooting

**Everything shows OFFLINE, even `127.0.0.1`.**
`ping` is probably not installed or is blocked in your environment. Test it with:
```
which ping
ping -W 2 -c 1 127.0.0.1
```
If `which ping` prints nothing, install it with the command in the quick start. Some online environments, like Codespaces, may also block pings to the internet, so the master (`1.1.1.1`) can still show OFFLINE even when local addresses work.

**`IndentationError` when running the file.**
Check that everything inside the classes and inside `if __name__ == "__main__":` is indented, and that no `if` block is left empty.

**`import: command not found` or similar shell errors.**
You ran the file with `./`. Run it with `python3` instead.

## Files

- `load_balancer_monitor_ckhna.py` - the program (both classes live in this one file)
- `README.md` - this guide

## Reference

- [OPS435 Assignment 2](http://wiki.littlesvr.ca/wiki/OPS435_Assignment_2) - the assignment specification
