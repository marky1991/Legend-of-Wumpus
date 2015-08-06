import json
from .utils import Grid

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
    def __hash__(self):
        return hash(self.name)
    __repr__ = __str__


class Game:
    def __init__(self):
        self.players = set()
        #Ha. I haven't even implemented maps yet...
        self.map = None

    def update(self):
        pass
class Unit:
    def __init__(self):
        #Represents the max growth per level. Multipied by a random number between 0 and 1,
        #then rounded to the nearest integer 
        self.growth_rates = {"resistance": 0,
                        "strength": 0,
                    "speed": 0,
                    "skill": 0,
                    "magic": 0,
                    "luck": 0,
                    "defense": 0,
                    "hp": 0
                    }

        self.resistance = 0
        self.strength = 0
        self.speed = 0
        self.skill = 0
        self.magic = 0
        self.luck = 0
        self.defense = 0
        self.hp = 10
        #Weight is between 0 and 10
        self.weight = 5
        self.movement = 4
        #weapon_skill is on a geade scale of F-Ss
        self.weapon_skill = {"axe": None,
                    "bow": None,
                    "sword": None,
                    #Heal, buff, etc.
                    "staff": None,
                    #Used for heron-style buffs
                    "song": None,
                    "lance": None,
                    "knife": None,
                    #Also includes dragon breath, claws, etc.
                    "hand": None,
                    "fire": None,
                    "wind": None,
                    "lightning": None,
                    "light": None,
                    "dark": None,
                    #For summoning
                    "wand": None
                }        

    def level_up(self):
        increased_none = True    
        while increased_none:
            for attribute_name, growth_rate in self.growth_rates.items():
                guaranteed_levels, growth_rate  = divmod(growth_rate, 100)
                increased_level = random.random() > growth_rate/100
                increased_none = guaranteed_levels + increased_level == 0 
                setattr(self, attribute_name, getattr(self, attribute_name) + guaranteed_levels + increased_level)
    
    @classmethod
    def create(cls):
        default = cls()
        for arg in vars(default):
            try:
                setattr(default, arg, getattr(default, arg)*random.random())
            except TypeError:
                pass
        return default
    def __str__(self):
        return "{0}({1})".format(type(self), self.name)

class Map:
    def __init__(self, grid=None, columns=50, rows=50):
        self.grid = grid or Grid(columns, rows)
        for node in self.grid:
            node.data = Cell()

    def jsonify(self):
        return {"grid": self.grid.jsonify()}
    @classmethod
    def debytify(cls, json_string):
        print(json_string)
        json_dict = json.loads(json_string)
        grid = Grid.debytify(json_dict["grid"]) 
        map = cls(grid=grid)
        return map
class Cell:
    """Represents a square in a map."""
    def __init__(self):
        #Grass is a required terrain type, no matter what
        #(You're free to customize it, but it must exist!)
        from .terrain_types import Grass
        #Mountain, grass, river, etc.
        self.terrain = Grass()
        #Anything located here (other than a player), e.g. a chest
        #Obviously there can only be one thing at a location, other than a player
        #This is intentional.
        self.object = None
    
class Terrain:
    def __init__(self):
        #How many steps it takes to traverse the terrain
        #For unpassable things like mountains, make infinity
        self.movement_cost = 1
        #At 0, you are invulnerable in this location
        #At 1, you take normal damage.
        #At 2, you take double damage, 3, 3x, etc
        
        #Might want to make this more sophisticated
        #than a simple constant. (Ex: perhaps on a river, submarine fighters
        #take no damage but everyone else takes normal damage)
        #For now, this is good enough
        self.defense_multiplier = 1.0
        #Same thing, except for attack
        self.attack_multiplier = 1.0
