import numpy as np

class Const:
    def __init__(self):
        self.car_height = 50

        self.ball_radius = 92.75
        self.side_wall = 4096
        self.back_wall = 5120
        self.ceiling = 2044
        self.map = np.array((self.side_wall, self.back_wall, self.ceiling))

        self.goal_height = 642
        self.goal_width = 1786
        self.goal_nearby = 1000

        self.angular_threshold = np.pi / 1

        self.neutral    = ( 0, 0, 0)

        self.forward    = (-1, 0, 0)
        self.backwards  = ( 1, 0, 0)

        self.right      = ( 0, 1, 0)
        self.left       = ( 0,-1, 0)

        self.up         = ( 0, 0, 1)
        self.down       = ( 0, 0,-1)

consts = Const()
