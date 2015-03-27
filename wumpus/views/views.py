#This is an implementation of View and GUI, not the base classes themselves
from . import View, GUI


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
        self.gui.set_next_screen(Lobby_View)
        self.username = self.text_box("Username:", 20, 80)
        self.password = self.text_box("Password:", 20, 100*((self.username.y - self.username.height - WIDGET_SPACING) / self.gui.height), secret=True)
        self.server_url = self.text_box("Server Url:", 20, 100*((self.password.y - self.password.height - WIDGET_SPACING) /self.gui.height))

class Lobby_View(View):
    def __init__(self, gui, *args, **kwargs):
        super().__init__(gui, *args, **kwargs)

    def add_widgets(self):
        self.room_name = self.text_box("Room name:")

