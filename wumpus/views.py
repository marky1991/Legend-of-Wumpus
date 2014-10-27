import itertools, os
import types
try:
    import npyscreen as curses
except ImportError:
    curses= None
try:
    import pyglet
    import kytten
except ImportError:
    kytten = None

mode = "curses"

#Percent of the screen (either height or width, depending) to put between each
#widget
WIDGET_SPACING = 5

#TEmporary hack
#(Npyscreen makes true proint() awful)
def print(*args):
    f = open("a.txt", "a")
    f.write(",".join(map(str, args))+"\n")
    f.close()

def calc_screen_type():
    #TODO: Add a (better) setting to set this
    if mode == "pyglet":
        return Pyglet_View
    return Curses_View

#Yeah, it turns out I needed a global context for the gui after all. : )
class GUI:
    def __init__(self, previous_view=None):
        super().__init__()
        self.view = None
        self.window = None

    def update(self):
        """Duh."""
        self.view.update()
    def set_next_screen(self, screen_class):
        """Lets the GUI know what window we're going to go to next. Sets up
        any information that next_screen will need to do its work."""
        pass
    def next_screen(self):
        """Switches the current screen to the one set up by set_next_screen."""
        pass
    def run(self):
        self.view.setup()
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

class View:
    def __init__(self, gui, previous_view=None):
        """Right now, this is pointless. Just indicates the interface.
        If it never becomes functional, to-be-removed."""
        super().__init__()
        self.screen = None
        self.gui = gui
        #This is a function that when called (takes no arguments) switches the screen
        #I don't think this belongs in View, but I don't remmeber.
        self.next_screen_function = None

    def setup(self):
        """Resonsible for configuring the GUI. Is only called for the first view."""
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

if curses:
    class Curses_GUI(GUI, curses.NPSAppManaged):
        def __init__(self):
            super().__init__()
        def onStart(self, form_name=None):
            self.screen = curses.Form()
            if form_name is None:
                form_name = "MAIN"
            self.registerForm(form_name, self.screen)

            for parms in self.view.planned_widgets:
                args, kwargs = parms
                self.screen.add(*args, **kwargs)

            self.planned_widgets = []
            print("Finished onstart")
            self.screen.afterEditing = lambda: self.next_screen()
        def run(self):
            super().run()
    if mode != "pyglet":
        GUI = Curses_GUI
    class Curses_View(View):
        def __init__(self, gui, previous_view=None):
            self.planned_widgets = []
            super().__init__(gui)

        def setup(self):
            pass

        def add_widget(self, args):
            self.planned_widgets.append(args)

        def text_box(self, label=None, x=None, y=None, secret=False):
            #This currently does NOT follow the API. Needs to return an object
            #with width, height, x, and y. TODO
            if not secret:
                cls = curses.TitleText
            else:
                cls = curses.TitlePassword
            args = (curses.TitleText,)
            if label is not None:
                args = ((cls,), {"name": label})
            return self.add_widget(args)
        def set_next_screen(self, screen_class):
            print("setting next", screen_class)
            #Due to the way npyscreen works, I can't do this in __init__
            def switch_screen(self):
                #So application is set only once we try to switch to another view
                #HAAACK
                print(self, "oprevious view", screen_class)
                screen_class.__init__(self, previous_view=self)
                print("switching")
                self.gui.onStart(self)
                self.setNextForm(screen_class.__name__)
            self.next_screen_function = lambda: switch_screen(self)

        def next_screen(self):
            print("Actually doing the switch")
            self.next_screen_function()

if kytten:
    class Pyglet_GUI(GUI):
        def run(self):
            pyglet.app.run()
        
        @property
        def height(self):
            return self.window.height

        @property
        def width(self):
            return self.window.width
    if mode == "pyglet":
        GUI = Pyglet_GUI
    class Pyglet_View(View):
        def __init__(self, gui):
            super().__init__(gui)
            self.widgets = []
            gui.window = pyglet.window.Window(resizable=True)
            gui.group=pyglet.graphics.OrderedGroup(0)
            self.theme = kytten.Theme("/home/mark/Proyectos/Kytten/theme/", override={
                "gui_color": [255, 235, 128, 255]})
            self.gui.window.register_event_type("on_update")
            def update(dt):
                self.gui.window.dispatch_event("on_update", dt)
            pyglet.clock.schedule(update)
            gui.batch = pyglet.graphics.Batch()
            @gui.window.event
            def on_draw():
                gui.window.clear()
                gui.batch.draw()
                #for widget in self.widgets:
                #    widget.draw()

        def setup(self):
            pass
        def text_box(self, label=None, x=None, y=None,  secret=False):
            x = ((x or 0) / 100) * self.gui.width
            y = ((y or 0) / 100) * self.gui.height
            box = kytten.Dialog( 
                kytten.HorizontalLayout([
                    kytten.Label(label),
                    kytten.Input()]
                ), theme=self.theme,anchor=kytten.ANCHOR_BOTTOM_LEFT, batch=self.gui.batch, offset=(x, y), group=self.gui.group, window=self.gui.window)
            self.widgets.append(box)
            box.do_layout()
            return box

class Login_View(calc_screen_type()):
    def __init__(self, gui, previous_view=None):
        super().__init__(gui)
        #Wow, this API ended up god-awful. It works (for pyglet anyway), but man is it hideous
        #Fixing this is a priority.
        self.username = self.text_box("Username:", 20, 80)
        self.password = self.text_box("Password:", 20, 100*((self.username.y - self.username.height - WIDGET_SPACING) / self.gui.height), secret=True)
        self.server_url = self.text_box("Server Url:", 20, 100*((self.password.y - self.password.height - WIDGET_SPACING) /self.gui.height))
        self.gui.set_next_screen(Lobby_View)

class Lobby_View(calc_screen_type()):
    def __init__(self, gui, previous_view=None):
        super().__init__(gui)
        self.room_name = self.text_box("Room name:")
