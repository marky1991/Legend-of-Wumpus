import circuits
from circuits.node import remote
from . import events

class Network_Node:
    """Represents a node (In the graph-theory sense) in the network. 
A node can be either a server or a client. Note: This object is 
game-specific. (So feel free to put in wumpus-related information.)
Maybe one day the design will justify splitting this out from the game-related
information, but that day isn't today."""
    def __init__(self, host="0.0.0.0", port=0):
        #We likely want to iterate over the player list in a stable order
        self.players = []
        self.host = host
        self.port = port
        #Object can't handle host and port, so don't pass them.
        super().__init__()
    @circuits.handler("read")
    def read(self, socket, data):
        event = events.debytify(data)
        old_events = new_events = event.handle(self)
        #old = new = [BBevent]
        #Hmm. This implementation assumes a finite event
        #set is returned. This might be hurtful.
        while new_events:
            #new = [bb] -> [blow, candle]
            #old = [BBEvent] -> [blow, candle]
            old_events = list(new_events)
            #old = bb -> [blow, candle]
            #new = []
            new_events = []
            for event in old_events:
                #old = [bb] -> [blow, candle]
                #new = [blow_up, c=andle_on] -> []
                caused_events = event.handle()
                new_events.extend(caused_events)
                if event.broadcast:
                    self.broadcast(event)
                if caused_events is None:
                    self.shutdown()
                    new_events = []
    def shutdown(self):
        self.stop()
    def broadcast(self):
        self.fire(remote(connect(("0.0.0.0", 50551)), "server"))
    
    @property
    def is_server(self):
        #This is a pretty defining feature for a server
        #Ought to think about this more.
        return hasattr(self, "clients")
