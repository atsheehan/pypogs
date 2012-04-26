#!/usr/bin/env python

from pypogs import server

ADDRESS = ''
PORT = 4485

s = server.ConnectionServer((ADDRESS, PORT), server.ConnectionHandler)
s.serve_forever()
