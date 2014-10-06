from functools import wraps, partial
from nose.tools import make_decorator as make_dec, istest

from wumpus.events import *

from wumpus.server import Server
from wumpus.client import Client
from wumpus.tests.mock import FakeServer, FakeClient
from wumpus.core import Player
from wumpus.network_node import Network_Node

def server_and_client(function):
    @wraps(function)
    def wrapper(self):
        for listener in [self.server] + self.clients:
            function(self, listener)
    return wrapper

def requires_networking(function):
    @wraps(function)
    def wrapper(self):
        if not (self.server.running and self.client.running):
            return
        else:
            return function(self)
    return wrapper

class testEvents:
    def setup(self):
        self.server = FakeServer()
        self.client = self.client1 = FakeClient()
        self.client2 = FakeClient()
        self.clients = [self.client, self.client2]
        self.player = self.player1 = Player("IDC")
        self.player2 = Player("Still don't care")
 
    @server_and_client
    def test_join_event(self, listener):
        #Unmock the players attribute
        listener.game.players = []
        if listener.is_server:
            listener.clients = {}
        return True
        event = Join_Event(self.player)
        
        old_player_count = len(listener.game.players)
        event.handle(listener)
        assert old_player_count + 1 == len(listener.game.players), (old_player_count, len(listener.game.players))

    @requires_networking
    def test_event_broadcasting(self):
        #This test can be naturalized now. It was made awkward because I was
        #trying to make it not require networking. That requirement is not
        #possible.
        self.client.game.players = []
        self.server.game.players = []
        self.client2.game.players = []
        self.server.clients = {}
        self.server.broadcast = functools.partial(Server.broadcast, self.server)
        self.server.read = functools.partial(Server.read, self.server)
        self.server.is_server = True#functools.partial(Network_Node.is_server, self.server)
        self.client.is_server = False#functools.partial(Network_Node.is_server, self.client)
        self.client2.is_server = False#functools.partial(Network_Node.is_server, self.client2)
        event = Join_Event(self.player)
        print(self.server.read, "REAd")
        self.server.read(None, bytify(event).encode("utf-8"))
        assert len(self.server.game.players) == 1, self.server.clients
        event2 = Join_Event(self.player2)
        self.server.read(None, bytify(event2).encode("utf-8"))
        assert len(self.server.game.players) == 2, self.server.game.players
        assert len(self.client2.game.players) == 2, self.client2.game.players
