from functools import wraps
from nose.tools import make_decorator as make_dec, istest

from wumpus.events import *

from wumpus.server import Server
from wumpus.tests.mock import FakeServer, FakeClient
from wumpus.core import Player

def server_and_client(function):
    @wraps(function)
    def wrapper(self):
        for listener in [self.server] + self.clients:
            function(self, listener)
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
        listener.players = []
        if listener.is_server:
            listener.clients = {}
        return True
        event = Join_Event(self.player)
        
        old_player_count = len(listener.players)
        old_client_count = len(listener.clients) if hasattr(listener, "clients") else 0
        event.handle(listener)
        assert old_player_count + 1 == len(listener.players), (old_player_count, len(listener.players))
        if listener.is_server:
            assert len(listener.clients) == old_client_count + 1, (len(listener.clients), old_client_count + 1)

    def test_event_broadcasting(self):
        self.client.players = []
        self.server.players = []
        self.client2.players = []
        self.server.clients = {}
        self.server.broadcast = Server.broadcast
        event = Join_Event(self.player)
        event.handle(self.server)
        assert len(self.server.clients) == 1, self.server.clients
        event2 = Join_Event(self.player2)
        event.handle(self.server)
        assert len(self.server.clients) == 2
        assert len(self.client.players) == 2, """Client1 players: {client1_players}.
                                                Server players: {server_players}. 
                                                Client2 players: {client2_players}
                                                """.format(client1_players=self.client.players,
                                                           client2_players=self.client2.players,
                                                           server_players=self.server.players)
