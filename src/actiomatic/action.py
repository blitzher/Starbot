""" 
definition of an action
"""


class Action:
    """
    High level action
    contains information about what, when and how an action should be performed
    """
    def __init__(self, game_state):
        self.initialization_time = game_state.game_info.seconds_elapsed
        self.agent = game_state.agent
        self._duration = 0
        self._delay = 0
        self._priority = 0

    def should_execute(self, time):
        # TODO: check if duration and delay allow execution
        return False

    def execute(self):
        # Overwrite this for an action
        pass

    def should_remove(self):
        # TODO: check if duration and delay has been surpassed
        return True

    def duration(self, time : float):
        self._duration = time
        return self

    def delay(self, time : float):
        self._delay = time
        return self

    def priority(self, number : int):
        self._priority = number
        return self

class Throttle(Action):
    def __init__(self, game_state, throttle = 0):
        super().__init__(game_state)
        self.throttle = throttle

    def execute(self):
        self.agent.controller_state.throttle = self.throttle

class Turn(Action):

    
    def __init__(self, game_state, turn = 0):
        super().__init__(game_state)
        self.turn = turn

    def execute(self):
        self.agent.controller_state.turn = self.turn

class Handbrake(Action):
    
    def __init__(self, game_state, handbrake = False):
        super().__init__(game_state)
        self.handbrake = handbrake

    def execute(self):
        self.agent.controller_state.handbrake = self.handbrake

class Boost(Action):

    def __init__(self, game_state, boost = 0):
        super().__init__(game_state)
        self.boost = boost

    def execute(self):
        self.agent.controller_state.boost = self.boost

class Roll(Action):
    
    def __init__(self, game_state, roll = 0):
        super().__init__(game_state)
        self.roll = roll

    def execute(self):
        self.agent.controller_state.roll = self.roll


class Pitch(Action):
    
    def __init__(self, game_state, pitch = 0):
        super().__init__(game_state)
        self.pitch = pitch

    def execute(self):
        self.agent.controller_state.pitch = self.pitch

class Yaw(Action):
    
    def __init__(self, game_state, yaw = 0):
        super().__init__(game_state)
        self.yaw = yaw

    def execute(self):
        self.agent.controller_state.yaw = self.yaw



