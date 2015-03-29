import itertools, os
import types



#Percent of the screen (either height or width, depending) to put between each
#widget
WIDGET_SPACING = 5

class Thing:
    def __init__(self, x, y, height=None, width=None):
        self.x = x
        self.y = y
        self.height = height
        self.width = width


#Yeah, it turns out I needed a global context for the gui after all. : )
class GUI:
    def __init__(self):
        super().__init__()
        self.view = None
        self.window = None

    def update(self):
        """Duh."""
        self.view.update()
    def set_next_screen(self, screen_class):
        """Lets the GUI know what window we're going to go to next. Sets up
        any information that next_screen will need to do its work."""
        print("GOT the bacse class.")
        pass
    def next_screen(self):
        """Switches the current screen to the one set up by set_next_screen."""
        pass
    def run(self):
        try:
            super().run()
        except AttributeError:
            pass
    @property
    def height(self):
        return 0

    @property
    def width(self):
        return 0

    def register_view(self, view_type):
        """Registers the view with the GUI, allowing it to be used. Must be
        called BEFORE you try to instantiate an instance of the 
        particular view"""
        pass

class View:
    def __init__(self, gui):
        """Right now, this is pointless. Just indicates the interface.
        If it never becomes functional, to-be-removed."""
        print("INITING")
        super().__init__()
        self.screen = None
        self.gui = gui

    def add_widgets(self):
        """I give up. Accessing properties of other added widgets just doesn't
        logically work in __init__ (which ought not require that you 
        have a set-up gui.) This method is called after the gui is up and running."""
        pass

    def setup(self):
        pass
    def update(self):
        """Duh."""
        pass
    def text_box(self, x=None, y=None, label=None, secret=False):
        """This function attaches it to the screen, whether you assign it to
        self (e.g. self.blah = return_value) or not. So don't forget to bind
        it to self.
        
        If secret is true, the values are to be hidden. (Replaced with
        asterisks, for example)
        
        Whatever type of object this returns, it has to have height, width, x, and y attributes.
        All other information about the object is undefined."""
        pass
    def run(self):
        pass
