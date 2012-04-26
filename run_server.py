#!/usr/bin/env python

import SocketServer

from pypogs import server

ADDRESS = ''
PORT = 4485

s = SocketServer.UDPServer((ADDRESS, PORT), server.ConnectionHandler)
s.serve_forever()
