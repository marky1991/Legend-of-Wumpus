import circuits

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
