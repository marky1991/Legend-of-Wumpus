try:
    import npyscreen as curses
except ImportError:
    curses= None

from ..log import debug, warning, error

from .base import *#GUI, View

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
        self.views = []
        self.view_cache = {}
        debug(self.views, "VIEWS")

    def onStart(self):
        debug("Setting up gui", self.view)
        #Why is thuis check needed?
        self.setNextForm("MAIN")
        debug(self.view)
        #TODO delete the check
        if self.view is None:
            debug(self.views, "views")
            for index in range(len(self.views)):
                debug(index)
                screen_class = self.views[index]
                debug("cls", screen_class)
                #npycurses really likes the first screen to be named
                #main. I don't rememer if this is required or not. Please
                #investigate later. It'd be nice to remove the special case.
                if index == 0:# and False:
                    kwargs = {"form_name": "MAIN"}

                else:
                    kwargs = {}


                #One issue here is that this requires that there is only one screen
                #of each type in the game. It would be nice to remove this restriction
                debug(self.view_cache)
                self.register_view(screen_class, kwargs)

        #Doing this here doesn't feel right. Please look into me. Might be
        #right, it's just a feeling
        self.view = self.view_cache[self.views[0]]
        self.view.post_init()

        debug("Setting up")
        debug("seting afterediting")
        def after_editing(self):
            debug("Calling next screen now")
            self.gui.view = self.next_screen
            sely.gui.view.post_init()
            debug("finished afterEdit")
        self.view.afterEditing = after_editing
        debug("Done start")
        
    def run(self):
        debug("Running")
        super().run()
        debug("ran")
    
    @property
    def width(self):
        return self.view.columns
    
    @property
    def height(self):
        return self.view.lines

    def register_view(self, view_type, kwargs=None):
        super().register_view(view_type, kwargs=kwargs)
        if kwargs is None:
            kwargs = {}
        self.views.append(view_type)
        #The first check is to make sure that the gui ahs already been started.
        #nypyscreen doesn"t like instantiating forms before the gui is set up
        debug("registering {cls} with kwargs {kw}".format(cls=view_type,
                                                          kw=kwargs))
        if view_type not in self.view_cache:
            self.view_cache[view_type] = view_type(self, **kwargs)
            self.registerForm(self.view_cache[view_type].form_name, self.view_cache[view_type])

class Curses_View(View, curses.Form):
    def __init__(self, gui, form_name=None):
        super().__init__(gui)
        self.form_name = form_name or type(self).__qualname__

    def post_init(self):
        debug("Calling base view post_init")
        super().post_init()
        debug("finished base post_init")
        #This really belongs in the gui class (register_view), but I don't
        #presently have a way to do it cleanly. #FIXME
        self.gui.registerForm(self.form_name, self)
        debug("Registered", self.form_name)

    def set_next_screen(self, screen_class):
        debug("setting next", screen_class, self)
        debug(self, "previous view", screen_class)
        self.gui.register_view(screen_class)
        try:
            self.next_view = self.gui.view_cache[screen_class]
        except KeyError as e:
            error("Didn't find {cls} in the view_cache. The cache: {cache}".format(
                        cls=str(screen_class), cache=self.gui.view_cache))
        debug("switching")
        """
        try:
            if not first_screen:
                self.onStart()
        except Exception as e:
            error(e)
        """
        self.gui.setNextForm(screen_class.__qualname__)
        debug("Finished")

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
        try:
            return Curses_Widget(self.add(*args, **kwargs))
        except Exception as e:
            error(e)
            raise e

