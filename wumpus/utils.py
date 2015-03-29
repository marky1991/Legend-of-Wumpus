class Lazy_Coord(float):

    """Implements a lazily_evaluated value. Effectively implements a blob
    of lazy getattrs that can be done arithmetic on. Not actually used at this
    point. (But it works too well to rip out without me feeling sad. : ( )
    
    TODO: Does this really need to be  a float subclass? It should work
    regardless of what the type that self.function returns. I think I
    can generalize to Lazy_Object if I implement the magic methods needed
    for non-numerics."""
    
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)#*args, **kwargs)
    #Note : To implement thuis, just make sure to calculate the current value
    #when doing __mul__, __add__, etc.
    def __init__(self, obj, field_name):
        super().__init__()
        self.object = obj
        self.field_name = field_name
        self.function = lambda: getattr(self.object, self.field_name) 

    def __add__(self, other):
        sum = Lazy_Coord(self.object, self.field_name)
        sum.function = lambda: self.function() + (other.function() if hasattr(other, "function") else other)
        return sum
    __radd__ = __add__

    def __sub__(self, other):
        difference = Lazy_Coord(self.object, self.field_name)
        difference.function = lambda: self.function() - (other.function() if hasattr(other, "function") else other) 
        return difference

    def __mul__(self, other):
        product = Lazy_Coord(self.object, self.field_name)
        product.function = lambda: self.function() * (other.function() if hasattr(other, "function") else other)
        return product

    def __truediv__(self, other):
        quotient = Lazy_Coord(self.object, self.field_name)
        quotient.function = lambda: self.function() / (other.function() if hasattr(other, "function") else other)
        return quotient

    def __floordiv__(self, other):
        quotient = Lazy_Coord(self.object, self.field_name)
        quotient.function = lambda: self.function() // (other.function() if hasattr(other, "function") else other)
        return quotient

    def __pow__(self, other, mod=None):
        #Not exactly the technical term...
        raised_thing = Lazy_Coord(self.object, self.field_name)
        if mod is None:
            raised_thing.function = lambda: self.function() ** (other.function() if hasattr(other, "function") else other)
        else:
            raised_thing.function = lambda: self.function() ** (other.function() if hasattr(other, "function") else other) % mod
        return raised_thing



    def __float__(self):
        #Haha. I can't believe I forgot to add the mechanism for a lazy number to be converted to a real number.
        return float(self.function())

    def __int__(self):
        return int(self.function())



def get_git_password():
    f = open("../password.txt")
    line = f.readline().strip()
    return line
