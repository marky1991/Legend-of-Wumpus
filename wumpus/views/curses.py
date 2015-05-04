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
        self.setNextForm("MAIN")
        debug(self.view)
        #Why is thuis check needed?
        #TODO delete the check
        if self.view is None:
            self.register_view(self.first_view_class, {"form_name": "MAIN"})

        #Doing this here doesn't feel right. Please look into me. Might be
        #right, it's just a feeling
        self.view = self.view_cache[self.views[0]]
        self.view.post_init()

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
            raise e
        debug("setting next form to", screen_class.__qualname__)

        debug("seting afterediting")
        def after_editing(self):
            debug("Calling next screen now")

            self.gui.setNextForm(screen_class.__qualname__)
            debug("setting next view to", self.next_view)
            self.gui.view = self.next_view
            self.gui.view.post_init()
            debug("finished afterEdit")
        self.afterEditing = lambda: after_editing(self)
        debug("Finished setting the next screen")

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
        debug("Adding a widget with label: {lbl}".format(lbl=label))
        try:
            return Curses_Widget(self.add(*args, **kwargs))
        except Exception as e:
            error(e)
            raise e

