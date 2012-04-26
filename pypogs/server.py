import time
import SocketServer

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render
from pypogs import world

# Don't bother with DatagramRequestHandler, we do not necessarily
# want to respond to each packet that is processed, e.g. an input
# packet might change the state of the server without an ACK sent
# back to the client.

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self._connected_users = {}
        SocketServer.BaseRequestHandler.__init__(self,
                                                 request,
                                                 client_address,
                                                 server)


    def handle(self):
        data = self.request[0].decode('ascii')

        if data == 'SYN':
            self._store_user_and_respond_to_syn(self.client_address)
        elif data == 'ACK':
            pass

    def _store_user_and_respond_to_syn(self, address):
        if address in self._connected_users:
            print "Received another SYN from", address
            return

        print "Received a SYN from", address

class GameServer(world.World):

    def __init__(self):
        world.World.__init__(self)

    def run(self):
        while not self._quit:
            self._tick()
            self._handle_events()
            self._wait_til_next_tick()
