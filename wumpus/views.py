import itertools

import npyscreen as curses

def print(*args):
    f = open("a.txt", "a")
    f.write(",".join(map(str, args))+"\n")
    f.close()


def calc_screen_type():
    #TODO: Add a setting to set this instead of always doing curses.
    return Curses_View

class View:
    def __init__(self, previous_view=None):
        """Right now, this is pointless. Just indicates the interface.
        If it never becomes functional, to-be-removed."""
        self.screen = None
        #This is a function that when called (takes no arguments) switches the screen
        #I don't think this belongs in View, but I don't remmeber.
        self.next_screen_function = None

    def setup(self):
        """Does whatever setup your particular view needs to do."""
        pass
    def update(self):
        """Duh."""
        pass
    def text_box(self, label=None, secret=False):
        """This function attaches it to the screen, whether you assign it to
        self (e.g. self.blah = return_value) or not. So don't forget to bind
        it to self.
        
        If secret is true, the values are to be hidden. (Replaced with
        asterisks, for example)"""
        pass
    def set_next_screen(self, screen_class):
        """Lets the GUI know what window we're going to go to next. Sets up
        any information that next_screen will need to do its work."""
        pass
    def next_screen(self):
        """Switches the current screen to the one set up by set_next_screen."""
        pass

class Curses_View(curses.NPSAppManaged, View):
    """Implementation note: To support both pygame and curses with the same API,
    I have to do some awkward juggling. Each view has to be an application.
    The first view (login view typically, but it doesn't have to be) gets run
    as an actual npyscreen application. The rest just get their various methods
    called when we switch to them. This pattern allows us to switch between
    view at will without having to consider a global "application". (which 
    isn't needed for pygame, as no such thing exists, and goes against how
    I want to design this.) (The application is stored in the view though.)"""
    def __init__(self, previous_view=None):
        if previous_view is None:
            super().__init__()
        self.application = previous_view.application if previous_view is not None else None
        self.planned_widgets = []

    def onStart(self, form_name=None):
        self.screen = curses.Form()
        if form_name is None:
            if self.application is None:
                form_name = "MAIN"
            else:
                raise Exception("not one")
                form_name = type(self).__name__
        self.registerForm(form_name, self.screen)

        for parms in self.planned_widgets:
            args, kwargs = parms
            self.screen.add(*args, **kwargs)

        self.planned_widgets = []
        print("Finished onstart")
        self.screen.afterEditing = lambda: self.next_screen()

    def add_widget(self, args):
        self.planned_widgets.append(args)

    def text_box(self, label=None, secret=False):
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
            self.application = self
            #HAAACK
            print(self, "oprevious view", screen_class)
            screen_class.__init__(self, previous_view=self)
            print("switching")
            screen_class.onStart(self, form_name=screen_class.__name__)
            self.setNextForm(screen_class.__name__)
        self.next_screen_function = lambda: switch_screen(self)

    def next_screen(self):
        print("Actually doing the switch")
        self.next_screen_function()

class Login_View(calc_screen_type()):
    def __init__(self, previous_view=None):
        if previous_view is None:
            super().__init__()
        self.username = self.text_box("Username:")
        self.password = self.text_box("Password:", secret=True)
        self.server_url = self.text_box("Server Url:")
        self.set_next_screen(Lobby_View)

class Lobby_View(calc_screen_type()):
    def __init__(self, previous_view=None):
        if previous_view is None:
            super().__init__()
        self.room_name = self.text_box("Room name:")
