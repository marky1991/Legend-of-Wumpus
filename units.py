import random

class Unit:
	base_weapons = set()
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
/
	def level_up(self):
		increased_none = True	
		while increased_none:
			for attribute_name, growth_rate in self.growth_rates.items():
				guaranteed_levels, growth_rate  = divmod(growth_rate, 100)
				increased_level = random.random() > growth_rate/100
				increased_none = guaranteed_levels + increased_level == 0 
				setattr(self, attribute_name, getattr(self, attribute_name) + guaranteed_levels + increased_level)
	def __str__(self):
		return "{0}({1})".format(type(self), self.name)

class Horseman(Unit):
	"""Oscar, level ?"""
	def __init__(self):
        super().__init__()
		self.growth_rates = {"resistance": 30,
                                        "strength": 45,
                                        "speed": 45,
                                        "skill": 50,
                                        "magic": 20,
                                        "luck": 30,
                                        "defense": 35,
                                        "hp": 55
                                        }
		self.hp = 26
		self.resistance = 0
		self.magic = 1
		self.skill = 6
		self.speed = 7
		self.luck = 5
		self.defense = 8

class Myrmidon(Unit):
	"""Mia, level 6"""
	def __init__(self):
        super().__init__()
		self.growth_rates = {"resistance": 30,
                                        "strength": 45,
                                        "speed": 45,
                                        "skill": 50,
                                        "magic": 20,
                                        "luck": 30,
                                        "defense": 35,
                                        "hp": 55
                                        }
	
		self.hp = 21
        self.resistance = 0
        self.magic = 0
        self.skill = 6
        self.speed = 7
        self.luck = 5
        self.defense = 8

class Soldier(Unit):
    """Nephenee, level 7"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 55,
                            "strength": 40,
                            "magic": 20,
                            "skill": 55,
                            "speed": 55,
                            "luck": 25,
                            "defense": 35,
                            "resistance": 30}
    
        self.hp = 22
        self.strength = 8
        self.magic = 2
        self.skill = 10
        self.speed = 11
        self.luck = 6
        self.defense = 9
        self.resistance = 3

        self.movement = 6

class Fighter(Unit):
    """Boyd, level 2"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 75,
                            "strength": 60,
                            "magic": 5,
                            "skill": 50,
                            "speed": 45,
                            "luck": 35,
                            "defense": 25,
                            "resistance": 25}

        self.hp = 30
        self.strength = 7
        self.magic = 0
        self.skill = 4
        self.speed = 6
        self.luck = 4
        self.defense = 5
        self.resistance = 0

        self.movement = 6

class Archer(Unit):
    """Leonardo, level 4"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 60,
                            "strength": 40,
                            "magic": 15,
                            "skill": 75,
                            "speed": 35,
                            "luck": 65,
                            "defense": 35,
                            "resistance": 55}

        self.hp = 17
        self.strength = 8
        self.magic = 0
        self.skill = 12
        self.speed = 10
        self.luck = 6
        self.defense = 5
        self.resistance = 4

        self.movement = 6

#Come up with better name for this class. FE calls them "knights", but I think
#that that is extremely confusing. Feel free to rename to whatever you like
class Tank(Unit):
    """Gatrie, level 9"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 80,
                            "strength": 55,
                            "magic": 5,
                            "skill": 55,
                            "speed": 25,
                            "luck": 25,
                            "defense": 60,
                            "resistance": 30}

        self.hp = 31
        self.strength = 12
        self.magic = 0
        self.skill = 6
        self.speed = 5
        self.luck = 5
        self.defense = 14 
        self.resistance = 0

        self.movement = 5

class Thief(Unit):
    """Volke, level 10"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 65,
                            "strength": 50,
                            "magic": 5,
                            "skill": 55,
                            "speed": 65,
                            "luck": 35,
                            "defense": 20,
                            "resistance": 10}

        self.hp = 25
        self.strength = 12
        self.magic = 0
        self.skill = 13
        self.speed = 13
        self.luck = 7
        self.defense = 14
        self.resistance = 3

        self.movement = 7

class Mage(Unit):
    """Duh. (Soren, level 1)"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 45,
                            "strength": 5,
                            "magic": 60,
                            "skill": 55,
                            "speed": 40,
                            "luck": 30,
                            "defense": 15,
                            "resistance": 55}

        self.hp = 18
        self.strength = 0
        self.magic = 6
        self.skill = 8
        self.speed = 8
        self.luck = 5
        self.defense = 2
        self.resistance = 7

        self.movement = 7
