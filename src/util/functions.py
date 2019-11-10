import numpy as np
from util.vec import Vec3

class Point: # Holder for objects in space, which require the location attribute
    def __init__(self, location):
        self.location = location

    def get_vec(self):
        return Vec3(self.location)

    def __add__(self, other):
        return self.location + other.location


def scale_value(val, a,b, c,d):
    "scale a value from area [a,b] to [c,d]"
    # if value is above or below [a,b], set it it to the respective limit

    # if a > b or c > d, swap them around
    if a > b: a,b = b, a
    if c > d: c,d = d, c

    if val < a: val = a
    if val > b: val = b

    scaled = c + (d-c)/(b-a) * (val-a)
    return scaled

def angle_lines(line_1, line_2):

    numerator = line_1.dot(line_2)
    denominator = line_1.length() * line_2.length()

    if denominator == 0:
        return 0

    ret = np.arccos(numerator / denominator)

    return ret

def distance_point_line(point, line_1, line_2):
    point, line_1, line_2 = Vec3(point), Vec3(line_1), Vec3(line_2)
    return ((line_2 - line_1).cross(line_1-point)).length()/(line_2-line_1).length()

def point_between_points(amount, point1, point2):
    """ point_between_points(amount, point1, point2) -> Vec3

    return a point spaced between two points.
    amount = 0 -> point1
    amount = 1 -> point2
    """
    point1, point2 = Vec3(point1), Vec3(point2)
    vector_between = point2 - point1

    return point1 + vector_between * amount

def find_correction(current: Vec3, ideal: Vec3) -> float:
    # Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.

    # The in-game axes are left handed, so use -x
    current_in_radians = np.arctan2(current.y, -current.x)
    ideal_in_radians = np.arctan2(ideal.y, -ideal.x)

    diff = ideal_in_radians - current_in_radians

    # Make sure that diff is between -pi and +pi.
    if abs(diff) > np.pi:
        if diff < 0:
            diff += 2 * np.pi
        else:
            diff -= 2 * np.pi

    return diff
