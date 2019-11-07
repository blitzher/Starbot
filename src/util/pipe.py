

def draw_line(renderer, point1, point2):
    renderer.begin_rendering()
    renderer.draw_line_3d(point1, point2, renderer.white())
    renderer.end_rendering()

def draw_debug(renderer, car, ball, action_display, *args):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())

class RenderPipe:
    def __init__(self, renderer, logger):
        self.renderer = renderer
        self.logger = logger
        self.tasks = []

    def draw_ui(self, args):
        " RenderPipe.draw_ui  (position, text)"
        self.renderer.draw_string_2d(args[0], args[1], 2, 2, str(args[2]), self.renderer.white())

    # Rendering functions
    def _draw_line(self, args):
        self.renderer.draw_line_3d(args[0], args[1], self.renderer.white())
    def _draw_text(self, args):
        self.renderer.draw_string_3d(args[0], 2, 2, str(args[1]), self.renderer.white())
    def _draw_polyline(self, args):
        self.renderer.draw_polyline_3d(args[0], self.renderer.white())

    # Wrappers
    def draw_line(self, *args):
        " RenderPipe.draw_line(position, text) "
        self.add_task(self._draw_line, *args)
    def draw_polyline(self, *args):
        " RenderPipe.draw_text(position, text) "
        self.add_task(self._draw_polyline, *args)
    def draw_text(self, *args):
        " RenderPipe.draw_text(position, text) "

        self.add_task(self._draw_text, *args)


    def add_task(self, *task):
        " RenderPipe.add_task(RenderPipe.add_task(task, *args) "
        self.tasks.append(task)

    def render(self):
        self.renderer.begin_rendering()

        for task in self.tasks:
            task[0](task[1:])

        self.renderer.end_rendering()
        self.tasks = []
