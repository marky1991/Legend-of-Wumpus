import os
basepath = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(basepath, "..", "..", "settings.txt"))
settings = open(path, "r")

try:
    from .pyglet import Pyglet_GUI
    from .pyglet import Pyglet_View
except ImportError as e:
    import traceback
    for line in traceback.format_stack():
        print(line)
    print(e)
    Pyglet_GUI = Pyglet_View = None

try:
    from .curses import Curses_GUI, Curses_View
except ImportError as e:
    import traceback
    for line in traceback.format_stack():
        print(line)
    print(e)
    Curses_GUI = Curses_View = None

#Short term hack. Should be replaced with proper
#settings loading.
mode = next(settings).replace("\n", "").split("=")[1]
print(mode, "mode")
settings.close()


GUI = Curses_GUI
View = Curses_View

if mode == "pyglet":
    if Pyglet_GUI and Pyglet_View:
        GUI = Pyglet_GUI
        View = Pyglet_View

#from .views import *
