try:
    import npyscreen as curses
except ImportError:
    curses= None

from ..log import debug, warning, error

from .base import *#GUI, View

view_cache = {}
class Curses_Widget:
    def __init__(self, widget):
        self.widget = widget
    @property 
    def x(self):
        return self.widget.relx

    @property
    def y(self):
        return self.widget.rely
    def __getattr__(self, attr_name):
        try:
            attr= self.widget.__getattribute__(attr_name)
        except Exception as e:
            error("Error", e)
        return attr

class Curses_GUI(GUI, curses.NPSAppManaged):
    def __init__(self):
        from .views import Login_View, Menu_View
        super().__init__()
        #This is a function that when called (takes no arguments)
        #switches the screen
        self.next_screen_function = lambda: None
        #This ought to be made less hacky once I move the implementations out
        #of here
        self.views = [Login_View, Menu_View]
        debug(self.views, "VIEWS")

    def onStart(self):
        debug("Setting up gui")
        if self.view is None:
            for index in range(len(self.views)):
                debug(self.views)
                screen_class = self.views[index]
                if index == 0:# and False:
                    kwargs = {"form_name": "MAIN"}
                else:
                    kwargs = {}
                if screen_class not in view_cache:
                    debug(screen_class, kwargs)
                    view_cache[screen_class] = screen_class(self, **kwargs)

            debug("Calling next")
            self.next_screen()
            debug("Called it")
        debug("Setting up")
        self.view.post_init()
        debug("Adding widgets")
        self.view.add_widgets()
        debug("seting afterediting")
        self.view.afterEditing = lambda: (debug("edit") or self.next_screen())
        debug("Done start")
        
    def run(self):
        super().run()
    
    @property
    def width(self):
        return self.view.columns
    
    @property
    def height(self):
        return self.view.lines
    
    def set_next_screen(self, screen_class):
        debug("setting next", screen_class, self.view)
        first_screen = self.view is None

        #Due to the way npyscreen works, I can't do this in __init__
        def switch_screen(self):
            #So application is set only once we try to switch to another view
            #HAAACK
            debug(self.view, "previous view", screen_class)
            self.view = view_cache[screen_class]
            debug("switching")
            try:
                if not first_screen:
                    self.onStart()
            except Exception as e:
                error(e)
        self.next_screen_function = lambda: switch_screen(self)
        self.setNextForm(screen_class.__name__)

    def next_screen(self):
        debug("Actually doing the switch")
        self.next_screen_function()

    def register_view(self, view_type):
        self.views.add(view_type)

class Curses_View(View, curses.Form):
    def __init__(self, gui, form_name=None):
        super().__init__(gui)
        self.form_name = form_name or type(self).__name__

    def post_init(self):
        self.gui.registerForm(self.form_name, self)

    def text_box(self, label=None, x=None, y=None, secret=False):
        if not secret:
            cls = curses.TitleText
        else:
            cls = curses.TitlePassword
        args = (curses.TitleText,)
        kwargs = {}
        if label is not None:
            args = (cls,)
            kwargs = {"name": label}
        return Curses_Widget(self.add(*args, **kwargs))

