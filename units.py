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
