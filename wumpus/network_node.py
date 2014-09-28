import circuits
from circuits.node import remote
from circuits.net.events import connect, write
from . import events
from .events import bytify

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
        print("Reading", self, self.is_server)
        event = events.debytify(data)
        print(event, event.broadcast)
        old_events = new_events = event.handle(self)
        if event.broadcast and self.is_server:
            print(self.broadcast, "BROADCASTING")
            self.broadcast(event)
        #old = new = [BBevent]
        #Hmm. This implementation assumes a finite event
        #set is returned. This might be hurtful. (But for any sane event, it isn't.
        #(And since the handler has to be on the server, any server manager that installs a server
        #handler that generates infinite events has shot himself in the foot))
        while new_events:
            #new = [bb] -> [blow, candle]
            #old = [BBEvent] -> [blow, candle]
            old_events = list(new_events)
            #old = bb -> [blow, candle]
            #new = []
            new_events = []
            for event in old_events:
                print("Event", event)
                #old = [bb] -> [blow, candle]
                #new = [blow_up, c=andle_on] -> []
                caused_events = event.handle()
                new_events.extend(caused_events)
                if event.broadcast and self.is_server:
                    self.broadcast(event)
                for listener in type(event).listeners:
                    #This API doesn't yet exist.
                    #Will define when we have a listener.
                    listener.handle(event)
                #I don't understand this logic.
                #if caused_events is None:
                #    self.shutdown()
                #    new_events = []
    def shutdown(self):
        self.stop()
    def broadcast(self, event):
        #I'm not even sure what this code was trying to do...
        #Surely it was a temporary ujnk piece cof code.

        #Actual broadcasting logic needs to be added.
        print("Broadcasting event")
        self.fire(write(bytify(event).encode("utf-8")))
        #raise NotImplementedError("Nope")
        
        #self.fire(remote(connect(("0.0.0.0", 50551)), "server"))
    
    @property
    def is_server(self):
        #This is a pretty defining feature for a server
        #Ought to think about this more.
        return hasattr(self, "clients")
