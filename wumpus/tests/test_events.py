from functools import wraps
from nose.tools import make_decorator as make_dec, istest

from wumpus.events import *

from wumpus.tests.mock import FakeServer, FakeClient
from wumpus.core import Player
from wumpus.utils import debytify, bytify


def server_and_client(function):
    @wraps(function)
    def wrapper(self):
        for listener in [self.server, self.client]:
            function(self, listener)
    return wrapper

class testEvents:
    def setup(self):
        self.server = FakeServer()
        self.client = FakeClient()
        self.player = Player()
    
    def test_player_event_serialization(self):
        """Tests those events that take a player"""
        events = [Join_Event]
        for cls in events:
            event = cls(self.player)
            round_trip_event = debytify(bytify(event))
            assert event == round_trip_event, (vars(event), vars(round_trip_event))
    
    def test_server_event_serialization(self): 
        events = [Shutdown_Event, Restart_Event]
        for cls in events:
            event = cls()
            round_trip_event = debytify(bytify(event))
            assert event == round_trip_event, (vars(event), vars(round_trip_event))

    def test_update_code_event(self):
        #Testing this one is going to be painful
        pass
 
    @server_and_client
    def test_join_event(self, listener):
        #Unmock the players attribute
        event = Join_Event(self.player)
        old_player_count = len(listener.game.players)
        event.handle(listener)
        assert old_player_count + 1 == len(listener.game.players), (old_player_count, len(listener.game.players))
    
    @server_and_client
    def test_join_event_duplicate(self, listener):
        event = Join_Event(self.player)
        event.handle(listener)
        event.handle(listener)
        assert len(listener.game.players) == 1, listener.game.players
