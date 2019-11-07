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
        self.duration = 0
        self.delay = 0
        self.priority = 0


    def should_execute(self):
        # Overwrite this for an action
        return False

    def execute(self):
        # Overwrite this for an action
        pass

    def should_remove(self):
        # TODO: check if the 
        return True

    def duration(self, time : float):
        self.duration = time
        return self

    def delay(self, time : float):
        self.delay = time
        return self

    def priority(self, number : int):
        self.priority = number
        return self

class Throttle(Action):
    def __init__(self, game_state, amount = 1):
        super().__init__(game_state)
        self.amount = amount

    def execute(self):
        self.agent.controller_state.throttle = self.amount