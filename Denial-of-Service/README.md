# ddos_simulation and dos_prevention

Originally forked from https://github.com/ricardojoserf/ddos_simulation. 

Includes features such as 4 attacks running in parallel to attack a target IP. Moreover, there is an option to extract all the available IPs and MACs on a network using Fing CLI and then attack while being spoofed as those IPs.

Server.py file has a methodoloy implemented using AMS algorithm to calculate surprise number to check for DoS attack and block any suspicious IPs.

DDoS simulation written in Python using "scapy" and "multiprocessing" libraries. Used for educational purposes


## Options:

There are 4 different DDoS attacks:

- SYN Flood 

- Teardrop 

- Black nurse

- Ether Flood




## Requirements

Python 2.x:

```
pip install scapy
```

Python 3.x:

```
pip3 install scapy
```

You should also have Fing CLI installed. Can be installed at https://www.fing.com/products/development-toolkit.

## Note

Tested both in Python2.x (2.7.15rc1) and Python 3.x (3.6.7)
