
from util.orientation import Orientation
from util.vec import Vec3
from util.constants import consts
from util.functions import *

from rlbot.agents.base_agent import SimpleControllerState
from actiomatic.action import *

class BehaviourAgent:
    def __init__(self, action_manager):
        self.action_manager = action_manager
        self.activity = None

        self.all_activites = Activity.__subclasses__()


    def __repr__(self):
        return "<BehaviourAgent at %s with activity %s>" % (hex(id(self)),self.activity.__class__.__name__)

    def set_controller_state(self, game_state):
        my_car = game_state.game_cars[game_state.agent.index]
        game_state.agent.pipe.draw_text_3d(my_car.physics.location, self.activity.__class__.__name__)

        if self.activity:
            try:
                self.activity.set_controller_state(game_state)
            except Exception as e:
                game_state.agent.logger.error("Could not set controller state from %s" % self.activity.__class__.__name__)
                game_state.agent.logger.error(e)
                self.activity = None
                game_state.controller = SimpleControllerState()
        else:
            self.activity = self.get_activity(game_state)

    def add_index(self, dic, ind):

        dic.update({'index':ind})

        return dic

    def get_activity(self, game_state):

        activities = [activity.activity_available(game_state) for activity in self.all_activites]
        available_activites = [self.add_index(activity, c) for c, activity in enumerate(activities) if activity['available']]
        if len(available_activites) > 0:
            significant_activities = sorted(available_activites, key = lambda x: x['importance'], reverse = True)
            significant_activity = significant_activities[0]
            activity = self.all_activites[significant_activity['index']](game_state.agent)
        else:
            activity = None

        return activity


class Activity:
    def __init__(self, action_manager):
        # Set and generate static information

        self.action_manager = action_manager
        self.initialized = True
        self.informed = False

        self.flipping = False
        self.importance = 0

        self.controller_state = SimpleControllerState()

    def set_controller_state(self, game_state):
        # Overwrite this in specific activity
        pass

    @staticmethod
    def activity_available(game_state):
        """
        returns dictionary of availability and importance
        overwrite for specific activity
        function must be callable without an object instance

        Activity.activity_available(game_state, agent) -> {'available': bool, 'importance': float/int}
        """
        return {'available':False, 'importance': 0}  # Return if the activity is available for beginning, and the current importance level

    def get_information(self, game_state): # Sets object information for getting controller state

        self.informed = True

        self.my_car = game_state.game_cars[game_state.agent.index]
        self.car_location = Vec3(self.my_car.physics.location)
        self.car_velocity = Vec3(self.my_car.physics.velocity)
        self.car_grounded = self.car_location.z < 50
        self.wheel_contact = self.my_car.has_wheel_contact

        self.ball_location = Vec3(game_state.game_ball.physics.location)
        self.ball_velocity = Vec3(game_state.game_ball.physics.velocity)

        self.car_orientation = Orientation(self.my_car.physics.rotation)
        self.car_direction = self.car_orientation.forward
        self.car_stable = angle_lines(self.car_velocity, self.car_direction) < consts.angular_threshold / 20

        self.get_additional_information(game_state)
        return None

    def get_additional_information(self, game_state): # Gets additional information. Overwrite in class
        pass

    
    def drive_to(self, position, game_state, boost = False, flip = False, max_thrust = 1):

        def handle_flip():
            flip_condition_1 = x_y_angle_within_threshhold and self.car_grounded
            # Car is driving somewhat quickly and car isn't gonna overshoot the target
            flip_condition_2 = self.car_velocity.length() > 750# and (position-self.car_location).length() > self.car_velocity.length()
            # Do front flip, if conditions are met

            if flip_condition_1 and flip_condition_2:
                Jump(game_state, duration = 0.4)
                Pitch(game_state, pitch = -1, delay = 0.4, duration = 0.2)
                Jump(game_state, delay = 0.5)
                return True
            return False

        def handle_boost():
            if abs(x_y_angle) < consts.angular_threshold / 10 and not self.flipping and boost:
                Boost(game_state)

        def land_right():
            roll_correction = scale_value(-game_state.car.physics.rotation.roll, -np.pi/2, np.pi/2, -1, 1)
            Roll(game_state, roll = roll_correction)


        if not self.informed:
            self.action_manager.agent.logger.error("Can't use Action.drive_to when Action.get_information(game_state) hasn't been called")

        if not self.car_grounded and not self.wheel_contact:
            land_right()

        action_display = "Time to target %ss" % round(self.rough_time_to_position(position, game_state), 2)        

        position = Vec3(position)

        car_to_pos = position - self.car_location
        angle = - find_correction(self.car_direction, car_to_pos)

        if abs(angle) > np.pi / 3:
            # TODO: self.controller_state.handbrake = True
            pass

        x_y_direction = Vec3(self.car_direction.x, self.car_direction.y, 0)
        x_y_location = Vec3(self.car_location.x, self.car_location.y, 0)
        x_y_angle = angle_lines(x_y_direction, position - x_y_location)
        x_y_angle_within_threshhold = x_y_angle < consts.angular_threshold / 50

        if flip == True:
            if not handle_flip() and boost == True:
                handle_boost()
        elif boost == True:
            handle_boost()

        dist_to_pos = (position - self.car_location).length()

        turn = scale_value(angle, -np.pi, np.pi, -1, 1)
        turn = np.sign(turn) * abs(turn) ** (1/3)
        thrust = scale_value(dist_to_pos, 0, 2500, 0.6, max_thrust)

        if abs(turn) < consts.angular_threshold / 100: 
            turn = 0

        Turn(game_state, turn = turn)
        Throttle(game_state, throttle = thrust)
        if x_y_angle > np.pi / 4:
            Handbrake(game_state)

        action_display = "\n Speed %s \n Dist %s" % (self.car_velocity.length(), (position - self.car_location).length())
        game_state.agent.pipe.draw_text_3d(self.car_location, action_display)

    def rough_time_to_position(self, position, game_state):
        if self.car_velocity.length() > 500:
            return self.car_location.dist(position) / self.car_velocity.length()
        else:
            return self.car_location.dist(position) / 500

    def hover(self, position, game_state, radius = 250):
        self.drive_to(position, game_state, max_thrust = 0.4)
