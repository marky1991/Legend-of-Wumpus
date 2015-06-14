#This is an implementation of View and GUI, not the base classes themselves
from . import View, GUI
from ..log import debug, error

#This ought to be factored out into the framework.
#(Side note: ought to create a framework : ) )
WIDGET_SPACING = 1

class Login_View(View):
    def __init__(self, gui, *args, **kwargs):
        print("doing login view")
        super().__init__(gui, *args, **kwargs)
        print("INIT")
        print("FINISHED")

    def add_widgets(self):
        #Wow, this API ended up god-awful. It works (for pyglet anyway), but man is it hideous
        #Fixing this is a priority.
        #Putting this here is a hack too
        debug("in ad widgets")
        self.set_next_screen(Menu_View)
        self.username = self.text_box("Username:", 20, 80)
        self.password = self.text_box("Password:", 20, 100*((self.username.y - self.username.height - WIDGET_SPACING) / self.gui.height), secret=True)
        self.server_url = self.text_box("Server Url:", 20, 100*((self.password.y - self.password.height - WIDGET_SPACING) /self.gui.height))
        debug("finished add_widgets for login_view")

class Menu_View(View):
    def __init__(self, gui, *args, **kwargs):
        super().__init__(gui, *args, **kwargs)

    def add_widgets(self):
        self.room_name = self.text_box("Room name:")

class Lobby_View(View):
    def __init__(self, gui, *args, **kwargs):
        super().__init__(gui, *args, **kwargs)
    def add_widgets(self):
        with self.row() as row:
            self.map = self.map(idk, parent=row)
            self.player_list = self.list(max_lines=20, parent=row)
        self.chat_box = self.dialog_box(max_lines=6)

