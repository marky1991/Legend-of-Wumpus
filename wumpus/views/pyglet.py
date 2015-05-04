try:
    import pyglet
    import kytten
except ImportError:
    kytten = None
    pyglet = None
    error("Failed to import either kytten or pyglet")

from .. import debug, error
from .base import GUI, View

class Pyglet_GUI(GUI):
    def run(self):
        debug(pyglet, kytten)
        debug("Running pyglet gjui")
        debug("first class", self.first_view_class)
        self.view = self.first_view_class(self)
        self.view.post_init()
        debug("Created the first view")
        pyglet.app.run()
    
    @property
    def height(self):
        return self.window.height

    @property
    def width(self):
        return self.window.width

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

    def text_box(self, label=None, x=None, y=None,  secret=False):
        x = ((x or 0) / 100) * self.gui.width
        y = ((y or 0) / 100) * self.gui.height
        debug("Adding a text box with label", label)
        box = kytten.Dialog( 
            kytten.HorizontalLayout([
                kytten.Label(label),
                kytten.Input()]
            ), theme=self.theme,anchor=kytten.ANCHOR_BOTTOM_LEFT, batch=self.gui.batch, offset=(x, y), group=self.gui.group, window=self.gui.window)
        self.widgets.append(box)
        box.do_layout()
        return box
        #thing = Thing(Lazy_Coord(box, "x"), Lazy_Coord(box, "y"), height=Lazy_Coord(box, "height"), width=Lazy_Coord(box, "width"))
        #return thing

