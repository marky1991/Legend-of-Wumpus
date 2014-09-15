import json

class Player:
    def __init__(self, name="default"):
        self.name = name
        #For now, team isn't a custom object.
        #Just a string (More like a label than a thing)
        self.team = None
    def jsonify(self):
        return {"name": self.name,
                "team": self.team}
    @classmethod
    def debytify(cls, json_string):
        print(json_string)
        json_dict = json.loads(json_string)
        player = cls(name=json_dict["name"])
        player.team = team
        return player
    def __eq__(self, other):
        #We do not care about team for purposes of equality
        return self.name == other.name
    def __str__(self):
        return "Player(name={name}, team={team})".format(name=self.name,
                                                        team=self.team)
    __repr__ = __str__
