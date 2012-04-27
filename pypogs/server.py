import os
import datetime
import time
import SocketServer
import string

import pygame

from pypogs import game_container
from pypogs import menu
from pypogs import render
from pypogs import world

def handle_syn(server, data, sock, address):
    challenge = _generate_random_challenge()

    if server.add_pending_connection(address, challenge):
        message = "SYN-ACK:%s" % challenge
        sock.sendto(message, address)

def handle_ack(server, data, sock, address):
    tokens = data.split(':', 1)
    if len(tokens) == 1:
        print "ACK did not contain challenge response, ignoring."
        return

    challenge_response = tokens[1]

    if server.check_for_pending_confirmation(address, challenge_response):
        sock.sendto("JOINED", address)
        server.check_for_new_game()

CHALLENGE_CHARS = string.ascii_uppercase + string.digits
CHALLENGE_LENGTH = 16

def _generate_random_challenge():
    return os.urandom(CHALLENGE_LENGTH).encode('hex')

class ConnectionServer(SocketServer.UDPServer):

    def __init__(self, server_address, request_handler):
        self._pending_users = {}
        self._connected_users = {}
        SocketServer.UDPServer.__init__(self, server_address, request_handler)

    def add_pending_connection(self, address, challenge):
        self._pending_users[address] = { 'time': datetime.datetime.now(),
                                         'challenge': challenge }

        print "syn received from", address
        print "pending users:", self._pending_users
        print "connected users:", self._connected_users

        return True

    def check_for_new_game(self):
        pass

    def check_for_pending_confirmation(self, address, challenge_response):
        if (address in self._pending_users and
            self._pending_users[address]['challenge'] == challenge_response):
            del self._pending_users[address]
            self._connected_users[address] = { 'time': datetime.datetime.now() }
        else:
            print "challenge failed or address prev. did not send SYN.", challenge_response

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
        packet_data = self.request[0].decode('ascii')
        packet_type = packet_data.split(':', 1)[0]

        handler = self.handlers.get(packet_type)

        if handler is not None:
            handler(self.server, packet_data,
                    self.request[1], self.client_address)

class GameServer(world.World):

    def __init__(self):
        world.World.__init__(self)

    def run(self):
        while not self._quit:
            self._tick()
            self._handle_events()
            self._wait_til_next_tick()
