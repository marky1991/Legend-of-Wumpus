class Player:
    def __init__(self, name):
        self.name = name
        self.team = None
    def jsonify(self):
        return {"name": self.name,
                "team": self.team}
    @staticmethod
    def debytify(player):
        return Player(
    def __eq__(self, other):
        #We do not care about team for purposes of equality
        return self.name == other.name
