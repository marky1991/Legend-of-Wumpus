import circuits
from . import events

class Server(circuits.node.server.Server):
    def __init__(self):
        #This maps user_id to client
        self.clients = {}
        self.id_generator = itertools.count()
        
    def connect(*args):
        pass

    def read(self, socket, data):
        event = events.parse(data)
        old_events = new_events = event.handle()
        #old = new = [BBevent]
        while new_events:
            new = [bb] -> [blow, candle]
            #old = [BBEvent] -> [blow, candle]
            old_events = list(new_events)
            #old = bb -> [blow, candle]
            #new = []
            new_events = []
            for event in old_events:
                #old = [bb] -> [blow, candle]
                #new = [blow_up, c=andle_on] -> [] 
                new_events.extend(event.handle())
                self.broadcase(event)

    
