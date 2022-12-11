import http.server
import socketserver
import random
import numpy as np
from statistics import mode

def AMSestimate(seq, num_samples=100):
    inds = list(range(len(seq)))
    random.shuffle(inds)
    inds = sorted(inds[: num_samples])

    d = {}
    for i, c in enumerate(seq):
        if i in inds and c not in d:
            d[c] = 0
        if c in d:
            d[c] += 1
    return int(len(seq) / float(len(d)) * sum((2 * v - 1) for v in d.values()))


IPWindow = []
Blocked_IPs = []
count = 0


PORT = 8080
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # print("Client IP: ", self.address_string())
        f = open("BlockedIPs.txt")
        Blocked_IPs = [line.strip() for line in f.readlines()]
        if self.address_string() in Blocked_IPs:
            print("IP", self.address_string(), "is Blocked")
        else:
            f = open("IPWindow.txt")
            IPWindow = [line.strip() for line in f.readlines()]
            f.close()
            if len(IPWindow) < 1000:
                IPWindow.append(self.address_string())
            else:
                IPWindow.pop(1)
                IPWindow.append(self.address_string())
            f = open("Count.txt")
            try:
                count = int(f.read())
            except:
                count = 0
            f.close()
            Unique, indices, counts = np.unique(IPWindow, return_counts=True, return_index=True)
            print(count, Unique, indices, counts, AMSestimate(IPWindow) / len(IPWindow))    
            # print(count, IPWindow)
            if count == 3:
                count = 0
                if AMSestimate(IPWindow) / len(IPWindow) > 1:
                    # Unique, counts, indices = np.unique(IPWindow, return_counts=True, return_index=True)
                    Blocked_IPs.append(mode(IPWindow))
                    with open("BlockedIPs.txt", "w") as outfile:
                        for IP in Blocked_IPs:
                            outfile.write('%s\n' %IP)
            self.path = 'index.html'
            count += 1
            with open("Count.txt", "w") as outfile:
                outfile.write(str(count))
            with open("IPWindow.txt", "w") as outfile:
                for IP in IPWindow:
                    outfile.write('%s\n' %IP)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHttpRequestHandler
# f = open("BlockedIPs.txt")
# Blocked_IPs = f.readlines()
open('IPWindow.txt', 'w').close()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()