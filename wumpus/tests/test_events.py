from nose import with_setup

from wumpus.events import *

from wumpus.tests.mock import FakeServer, FakeClient
from wumpus.core import Player

class testEvents:
    def setup(self):
        self.server = FakeServer()
        self.client = FakeClient()
        self.player = Player()

    def test_join_serialization(self):
        event = Join_Event(self.player)
        print(event.bytify().encode("utf-8"))
        print("A", debytify(event.bytify().encode("utf-8")).kwargs, event.kwargs, "B")
        round_trip_event = debytify(event.bytify().encode("utf-8"))
        assert event == round_trip_event, (event.args, round_trip_event.args)

def blah():
    
    join = Join_Event(player)
    server_events = []
    for event_type in [Join_Event, Event, Restart_Event, Shutdown_Event, Update_Code_Event]:
        event = event_type()
