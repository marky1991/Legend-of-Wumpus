import circuits
from circuits import node
#from wumpus import events
import itertools

class Server(circuits.Component):
    def __init__(self, host="127.0.0.1", port=9001):
        super().__init__()
        #This maps user_id to client
        self.clients = {}
        self.id_generator = itertools.count()
        node.Node((host, port)).register(self)
        
    def connect(*args):
        pass

    def read(self, socket, data):
        event = events.parse(data)
        old_events = new_events = event.handle()
        #old = new = [BBevent]
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
