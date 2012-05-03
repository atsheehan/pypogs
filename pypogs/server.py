import datetime

from twisted.application import internet
from twisted.application import service
from twisted.internet import protocol
from twisted.protocols import basic
from twisted.python import log

class PyPogsProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        log.msg("received line: %s" % line)

    def connectionMade(self):
        client_address = self.transport.getPeer()
        self.factory.add_user((client_address.host, client_address.port))

    def connectionLost(self, reason):
        client_address = self.transport.getPeer()
        self.factory.drop_user((client_address.host, client_address.port))


class PyPogsService(service.Service):
    def __init__(self):
        self._users = {}
        self._instances = []

    def add_user(self, address):
        self._users[address] = { 'connected_at': datetime.datetime.now(),
                                 'status': 'waiting' }
        players = self._find_players_to_start_game()
        if players is not None:
            self._start_new_game(players)

        log.msg("added user: %s" % self._users)

    def _find_players_to_start_game(self):
        available_players = []
        for k, v in self._users.iteritems():
            if v['status'] == 'waiting':
                available_players.append(k)
                if len(available_players) >= 2:
                    break

        if len(available_players) >= 2:
            return available_players
        else:
            return None

    def _start_new_game(self, players):
        self._instances.append(players)
        for p in players:
            self._users[p]['status'] = 'in-game'

    def drop_user(self, address):
        del self._users[address]
        log.msg("removed user: %s" % self._users)

    def get_pypogs_factory(self):
        f = protocol.ServerFactory()
        f.protocol = PyPogsProtocol
        f.add_user = self.add_user
        f.drop_user = self.drop_user
        return f

application = service.Application('pypogs')
f = PyPogsService()
service_collection = service.IServiceCollection(application)
f.setServiceParent(service_collection)

internet.TCPServer(4485, f.get_pypogs_factory()).setServiceParent(service_collection)
