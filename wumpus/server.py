import circuits
from . import events
from circuits.node import Node
import itertools

class Server(circuits.core.Component):
    def __init__(self, host="0.0.0.0", port=50551):
        super().__init__()
        #This maps user_id to client
        self.clients = {}
        self.host = host
        self.port = port
        self.id_generator = itertools.count()
        Node((host, port)).register(self)

    def connect(*args):
        pass

    def read(self, socket, data):
        event = events.parse(data)
        old_events = new_events = event.handle()
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
                new_events.extend(event.handle())
                self.broadcast(event)

    
