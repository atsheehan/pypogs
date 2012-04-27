#!/usr/bin/env python

import socket

if __name__ == "__main__":
    PORT = 4485
    MAX = 2000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print "Sending SYN packet to", ("localhost", PORT)

    sock.connect(("localhost", PORT))
    sock.send("SYN")

    data = sock.recv(MAX)
    tokens = data.split(':', 1)
    if tokens[0] == 'SYN-ACK':
        if len(tokens) == 2:
            message = "ACK:%s" % tokens[1]
            sock.send(message)

        data = sock.recv(MAX)
        tokens = data.split(':', 1)
        if tokens[0] == 'STARTED':
            print "game has started"


    print "closing socket"
    sock.close()

