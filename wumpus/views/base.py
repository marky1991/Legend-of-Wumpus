import itertools, os
import types

from ..log import debug, error, warning


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
        #Why does this exist in the base?
        self.window = None
        #The class of the view you want to start on (the more obvious design
        #would have been to just let the client set
        #gui.view = some_view_instance, but certain backends (curses) don't let
        #you instantiate views before the gui is actually running)
        #I don't think this is too awkward a workaround
        self.first_view_class = None

    def update(self):
        """Duh."""
        self.view.update()
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

    def register_view(self, view_type, kwargs=None):
        """Registers the view with the GUI, allowing it to be used. If you are instantiating
        instances of the type outside of register_view, this must be called first. If the subclass
        itself chooses to instantiate the type in this method, it must pass kwargs into the view as
        keyword arguments."""
        pass

class View:
    def __init__(self, gui):
        """Right now, this is pointless. Just indicates the interface.
        If it never becomes functional, to-be-removed."""
        debug("{cls}.init() triggered View.__init__".format(cls=type(self).__qualname__))
        super().__init__()
        self.screen = None
        self.gui = gui

    def add_widgets(self):
        """I give up. Accessing properties of other added widgets just doesn't
        logically work in __init__ (which ought not require that you 
        have a set-up gui.) This method is called after the gui is up and running."""
        pass

    def post_init(self):
        debug("About to add widgets to " + str(type(self)))
        try:
            self.add_widgets()
        except Exception as e:
            error("Some issue when adding widgets: {err}".format(err=str(e)))
        debug("Finished adding widgets")
    def set_next_screen(self, screen_class):
        """Lets the GUI know what window we're going to go to next. Sets up
        any information that next_screen will need to do its work. 
        
        It is currently required that there only be one set_next_screen call
        per screen_class (For the whole application). It is hoped that this
        restriction can be removed in the future."""
        debug("GOT the bacse class.")
    def next_screen(self):
        """Switches the current screen to the one set up by set_next_screen."""
        debug("Switching scrren")
        self.gui.view = self.next_screen
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
