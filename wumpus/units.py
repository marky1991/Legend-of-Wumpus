import random

#Still not sure if we're going to keep all of the subclasses or not
#They don't have unique behavior (so far), so we should probably rip them
#out. It just doesn't feel right right now, so they'll stay for now. 
#(Recording in case we forget)

#Still todo: 
#   -Set up weight
#   -Extrapolate backwards for all of the classes to convert them to level 1
#   characters
#   -Skills
#   -Add non-FE-based classes
#   -?

from .core import Unit

magic_triangle_types = {"fire", "wind", "lighting"}
magic_types = magic_triangle_types | {"light", "dark"}

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

        #TODO: Discuss whether we want to give level E hand to everyone or not.
        #TODO: Also, discuss if we really want to seperate horsemen by weapon
        #type. I think we probably do (We don't want to give them both bows and
        #swords for example), but we need to discuss how to imlpement it.
        #I think creating (programmatic) class-level subtypes is a bad decision.
        #I think we have two choices: We can either give the user the choice on
        #generating his character or we can randomly choose for him. For now,
        #I'm implementing the random choice approach.
    
        preferred_weapon = random.choice(["axe", "sword", "bow", "lance"])
        self.weapon_skill[preferred_weapon] = "E"

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

        self.weapon_skill["sword"] = "E"

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

        self.weapon_skill["lance"] = "E"

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

        self.weapon_skill["axe"] = "E"

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

        self.weapon_skill["bow"] = "E"

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

        self.weapon_skill["lance"] = "E"

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

        self.weapon_skill["knife"] = "E"

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
        for magic_type in magic_triangle_types:
            self.weapon_type[magic_type] = "E"

class Dark_Mage(Unit):
    """Pelleas, level 12. (I've never played with him. No idea
if he's any good at all. Compare with soren to see.)"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 25,
                            "strength": 25,
                            "magic": 55,
                            "skill": 45,
                            "speed": 60,
                            "luck": 40,
                            "defense": 30,
                            "resistance": 45}

        self.hp = 33
        self.strength = 13
        self.magic = 24
        self.skill = 20
        self.speed = 21
        self.luck = 14
        self.defense = 14
        self.resistance = 19

        self.movement = 6
        self.weight = 9
        ##TODO: Discuss.
        #Pelleas has thunder and dark. Sephiran, the other dark mage of the
        #first two, starts as an archsage it looks like and has
        #light+dark(+staff). Maybe give dark + one random choice from the rest of
        #the magic types? It's kind of unfair though. With this way, dark mages
        #beat two of the three points of the triangle, while normal mages (and
        #bishops) can only beat one. I guess the counter is to make them
        #slightly worse than normal mages.
        self.weapon_skill["dark"] = "E"
        other_known_magic = random.choice(magic_types - {"dark"})
        self.weapon_type[other_known_magic] = "E"

class Priest(Unit):
    """Rhys, level 4"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 40,
                            "strength": 5,
                            "magic": 60,
                            "skill": 50,
                            "speed": 40,
                            "luck": 50,
                            "defense": 25,
                            "resistance": 55}

        self.hp = 20
        self.strength = 0
        self.magic = 10
        self.skill = 7
        self.speed = 4
        self.luck = 6
        self.defense = 0
        self.resistance = 14

        self.movement = 5
    
        self.weapon_type["staff"] = "E"

#Not sure if keeping or not.
#We can always simply not instantiate it

#TODO: Discuss
#We can probably have a class that is for the classes that transform
#Might instead group by semantic meaning (E.g. animals).
#Need to consider
class Cat(Unit):
    """Currently using lethe (lvl 3) from PoR. Might use ranulf instead. Need
to test."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 130,
                            "strength": 50,
                            "magic": 5,
                            "skill": 65,
                            "speed": 70,
                            "luck": 50,
                            "defense": 40,
                            "resistance": 25}

        #Using untransformed stats
        #TODO: Discuss how to implement this properly.
        self.hp = 34
        self.strength = 12
        self.magic = 4
        self.skill = 10
        self.speed = 12
        self.luck = 15
        self.defense = 9
        self.resistance = 10

        self.movement = 7
        self.weapon_type["hand"] = "E"

class Tiger(Unit):
    """Maurim, level 9. (He's less broken than Mordecai)"""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 145,
                            "strength": 70,
                            "magic": 5,
                            "skill": 70,
                            "speed": 55,
                            "luck": 35,
                            "defense": 35,
                            "resistance": 45}

        self.hp = 45
        self.strength = 16
        self.magic = 4
        self.skill = 13
        self.speed = 15
        self.luck = 11
        self.defense = 12
        self.resistance = 12

        self.movement = 7
        self.weapon_type["hand"] = "E"

class Raven(Unit):
    """Vika, level 13. (RD) She might be awful. Not sure."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 60,
                            "strength": 25,
                            "magic": 50,
                            "skill": 60,
                            "speed": 60,
                            "luck": 65,
                            "defense": 15,
                            "resistance": 65}

        self.hp = 38
        self.strength = 9
        self.magic = 5
        self.skill = 13
        self.speed = 15
        self.luck = 14
        self.defense = 7
        self.resistance = 7

        self.movement = 6
        self.weapon_type["hand"] = "E"

class Hawk(Unit):
    """Janaff, level 8."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 130,
                            "strength": 55,
                            "magic": 10,
                            "skill": 70,
                            "speed": 65,
                            "luck": 40,
                            "defense": 30,
                            "resistance": 25}

        self.hp = 39
        self.strength = 13
        self.magic = 5
        self.skill = 15
        self.speed = 17
        self.luck = 16
        self.defense = 11
        self.resistance = 10

        self.movement = 6
        self.weapon_type["hand"] = "E"

class Heron(Unit):
    """Reyson, level 3."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 65,
                            "strength": 5,
                            "magic": 40,
                            "skill": 50,
                            "speed": 50,
                            "luck": 60,
                            "defense": 15,
                            "resistance": 50}

        self.hp = 22
        self.strength = 1
        self.magic = 10
        self.skill = 11
        self.speed = 14
        self.luck = 15
        self.defense = 2
        self.resistance = 20

        self.movement = 5
        #TODO: Discuss. Do we want to give them a weapon of some kind?
        self.weapon_type["song"] = "E"

class Red_Dragon(Unit):
    """Ena, level 10."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 145,
                            "strength": 35,
                            "magic": 5,
                            "skill": 50,
                            "speed": 60,
                            "luck": 40,
                            "defense": 40,
                            "resistance": 30}

        self.hp = 52
        self.strength = 20
        self.magic = 9
        self.skill = 17
        self.speed = 15
        self.luck = 14
        self.defense = 23
        self.resistance = 21

        self.movement = 5
        #TODO: Do we want to make this fire instead of hand?
        #I think so.
        self.weapon_type["hand"] = "E"

class White_Dragon(Unit):
    """Nasir, level 18."""
    def __init__(self):
        super().__init__()
        self.growth_rates = {"hp": 150,
                            "strength": 50,
                            "magic": 10,
                            "skill": 55,
                            "speed": 45,
                            "luck": 60,
                            "defense": 25,
                            "resistance": 35}

        self.hp = 56
        self.strength = 20
        self.magic = 11
        self.skill = 123
        self.speed = 22
        self.luck = 17
        self.defense = 24
        self.resistance = 27

        self.movement = 5
        self.weapon_type["hand"] = "E"
