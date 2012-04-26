#!/usr/bin/env python

import socket

if __name__ == "__main__":
    PORT = 4485
    MAX = 2000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print "Sending SYN packet to", ("localhost", PORT)

    sock.connect(("localhost", PORT))
    sock.send("SYN")
    sock.close()

