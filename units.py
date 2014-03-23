class Unit:
	base_weapons = set()
	def __init__(self, cls_name):
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

	def __str__(self):
		return "{0}({1})".format(type(self), self.name) 
