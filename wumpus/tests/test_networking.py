from functools import wraps
from nose.tools import make_decorator as make_dec, istest

from wumpus.events import *

from wumpus.tests.mock import FakeServer, FakeClient
from wumpus.core import Player



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
            round_trip_event = debytify(event.bytify().encode("utf-8"))
            assert event == round_trip_event, (vars(event), vars(round_trip_event))
    
    def test_server_event_serialization(self): 
        events = [Shutdown_Event, Restart_Event]
        for cls in events:
            event = cls()
            round_trip_event = debytify(event.bytify().encode("utf-8"))
            assert event == round_trip_event, (vars(event), vars(round_trip_event))

    def test_update_code_event(self):
        #Testing this one is going to be painful
        pass
 
    @server_and_client
    def test_join_event(self, listener):
        #Unmock the players attribute
        listener.players = []
        event = Join_Event(self.player)
        
        old_player_count = len(listener.players)
        old_client_count = len(listener.clients) if hasattr(listener, "clients") else 0
        event.handle(listener)
        assert old_player_count + 1 == len(listener.players), (old_player_count, len(listener.players))
        if listener.is_server:
            assert len(listener.clients) == old_client_count + 1, (len(listener.clients), old_client_count + 1)


    @server_and_client
    def test_join_event_duplicate(self, listener):
        listener.players = []
        event = Join_Event(self.player)
        event.handle(listener)
        event.handle(listener)
        assert len(listener.players) == 1, listener.players
