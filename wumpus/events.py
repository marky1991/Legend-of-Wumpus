import json

class Event:
    #Determines whether the server will forward the event on to other clients or
#not.
    broadcast = False
    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}
    def handle(self, listener):
        """Handles the event. Can return an arbitrary (Currently finite only)
number of events. Listener is the networking actor (i.e. either client or server) that
is handling the event."""
        return
    def __iter__(self):
        """Allows you to iterate over an event, allowing you to treat a single
event as
an event_tuple instead of being forced to explicitly put it in a tuple. I'm
pretty sure this is a good idea, but I could maybe be wrong.
(It's convenient, but a bit of a hack...Need to think about it further.)"""
        return iter((self,))
    @property
    def name(self):
        return str(type(self))
    def bytify(self):
        out = {"name": self.name,
                "args": self.args,
                "kwargs": self.kwargs}
        return json.dumps(out)
    @staticmethod
    def debytify(json_val):
        json_dict = json.loads(json_val)
        return Event(*json_dict["args"], **json_dict["kwargs"])

class Join_Event(Event):
    broadcast = True
    def __init__(self, client):
        super().__init__(client)
    def handle(self, listener):
        #TODO: You know, add the client to the client list.
         return
