try:
    import npyscreen as curses
except ImportError:
    curses= None

from .base import *#GUI, View
from .views import Login_View, Lobby_View

def print(*args):
    f = open("a.txt", "a")
    f.write(",".join(map(str, args))+"\n")
    f.close()

print("curses")
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
            print("Error", e)
        return attr

class Curses_GUI(GUI, curses.NPSAppManaged):
    def __init__(self):
        super().__init__()
        #This is a function that when called (takes no arguments)
        #switches the screen
        self.next_screen_function = lambda: None
        #This ought to be made less hacky once I move the implementations out
        #of here
        self.views = [views.Login_View, views.Lobby_View]
        print(self.views, "VIEWS")

    def onStart(self):
        print("Setting up gui")
        if self.view is None:
            for index in range(len(self.views)):
                screen_class = self.views[index]
                if index == 0:# and False:
                    kwargs = {"form_name": "MAIN"}
                else:
                    kwargs = {}
                if screen_class not in view_cache:
                    print(screen_class, kwargs)
                    view_cache[screen_class] = screen_class(self, **kwargs)

            print("Calling next")
            self.next_screen()
            print("Called it")
        print("Setting up")
        self.view.setup()
        print("Adding widgets")
        self.view.add_widgets()
        print("seting afterediting")
        self.view.afterEditing = lambda: (print("edit") or self.next_screen())
        print("Done start")
        
    def run(self):
        super().run()
    
    @property
    def width(self):
        return self.view.columns
    
    @property
    def height(self):
        return self.view.lines
    
    def set_next_screen(self, screen_class):
        print("setting next", screen_class, self.view)
        first_screen = self.view is None

        #Due to the way npyscreen works, I can't do this in __init__
        def switch_screen(self):
            #So application is set only once we try to switch to another view
            #HAAACK
            print(self.view, "previous view", screen_class)
            self.view = view_cache[screen_class]
            print("switching")
            try:
                if not first_screen:
                    self.onStart()
            except Exception as e:
                print(e)
        self.next_screen_function = lambda: switch_screen(self)
        self.setNextForm("MAIN")#screen_class.__name__)

    def next_screen(self):
        print("Actually doing the switch")
        self.next_screen_function()

    def register_view(self, view_type):
        self.views.add(view_type)

class Curses_View(View, curses.Form):
    def __init__(self, gui, form_name=None):
        super().__init__(gui)
        self.form_name = form_name or type(self).__name__

    def setup(self):
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

