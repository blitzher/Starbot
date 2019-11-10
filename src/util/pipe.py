class RenderPipe:
    def __init__(self, renderer, logger):
        self.renderer = renderer
        self.logger = logger
        self.tasks = []

    def draw_ui(self, args):
        " RenderPipe.draw_ui  (position, text)"        

    def store_function_call(self, function, *args, **kwargs):
        # store a function call to be called later
        return lambda: function(*args, **kwargs)

    def draw_text_2d(self, pos, text, scale = 2, colour = (255, 255, 255), alpha = 255):
        draw_colour = self.renderer.create_color(alpha, *colour)
        func = self.renderer.draw_string_2d
        function_call = self.store_function_call(func, pos[0], pos[1], scale, scale, str(text), draw_colour)
        self.add_task(function_call)

    def draw_text_3d(self, position, text, scale = 2, colour = (255, 255, 255), alpha = 255):
        draw_colour = self.renderer.create_color(alpha, *colour)
        func = self.renderer.draw_string_3d
        function_call = self.store_function_call(func, position, scale, scale, str(text), draw_colour)
        self.add_task(function_call)

    def draw_line_3d(self, pos_1, pos_2, colour = (255, 255, 255), alpha = 255):
        draw_colour = self.renderer.create_color(alpha, *colour)
        func = self.renderer.draw_line_3d
        function_call = self.store_function_call(func, pos_1, pos_2, draw_colour)
        self.add_task(function_call)

    def draw_polyline_3d(self, positions, colour = (255, 255, 255), alpha = 255):
        draw_colour = self.renderer.create_color(alpha, *colour)
        func = self.renderer.draw_polyline_3d
        function_call = self.store_function_call(func, positions, draw_colour)
        self.add_task(function_call)


    def add_task(self, task):
        " RenderPipe.add_task(RenderPipe.add_task(task, *args) "
        self.tasks.append(task)

    def render(self):
        self.renderer.begin_rendering()

        for task in self.tasks:
            task()

        self.renderer.end_rendering()
        self.tasks = []
