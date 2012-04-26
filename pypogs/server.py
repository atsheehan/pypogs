import datetime
import time
import SocketServer

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render
from pypogs import world

def handle_syn(server, data, sock, address):
    if server.add_pending_connection(address):
        sock.sendto("SYN-ACK", address)

def handle_ack(server, data, sock, address):
    if server.check_for_pending_confirmation(address):
        sock.sendto("JOINED", address)

class ConnectionServer(SocketServer.UDPServer):

    def __init__(self, server_address, request_handler):
        self._pending_users = {}
        self._connected_users = {}
        SocketServer.UDPServer.__init__(self, server_address, request_handler)

    def add_pending_connection(self, address):
        self._pending_users[address] = datetime.today()

        print "syn received from", address
        print "pending users:", self._pending_users
        print "connected users:", self._connected_users

        return True

    def check_for_pending_confirmation(self, address):
        if address in self._pending_users:
            del self._pending_users[address]
            self._connected_users[address] = 1

        print "ack received from", address
        print "pending users:", self._pending_users
        print "connected users:", self._connected_users

        return True

# Don't bother with DatagramRequestHandler, we do not necessarily
# want to respond to each packet that is processed, e.g. an input
# packet might change the state of the server without an ACK sent
# back to the client. Inherit from BaseRequestHandler instead.

class ConnectionHandler(SocketServer.BaseRequestHandler):

    handlers = {
        'SYN': handle_syn,
        'ACK': handle_ack
        }

    def handle(self):
        packet_type = self.request[0].decode('ascii')

        handler = self.handlers.get(packet_type)

        if handler is not None:
            handler(self.server, self.request[0],
                    self.request[1], self.client_address)

class GameServer(world.World):

    def __init__(self):
        world.World.__init__(self)

    def run(self):
        while not self._quit:
            self._tick()
            self._handle_events()
            self._wait_til_next_tick()
