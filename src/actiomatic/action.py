""" 
definition of an action
"""


class ActionManager:
    def __init__(self, agent):
        self.actions = []
        self.agent = agent

    def run_actions(self, game_state):
        # TODO: Add priority check
        # then execute, and remove appropriately
        for action in self.actions:
            
            if action.should_execute(game_state.game_info.seconds_elapsed):
                action.execute(game_state)                
            if action.should_remove(game_state.game_info.seconds_elapsed):
                self.actions.remove(action)

    def add(self, action):
        # append an action to self.actions
        self.actions.append(action)

class Action:
    """
    Low level action
    contains information about what, when and how an action should be performed
    """
    def __init__(self, game_state, duration = 0, delay = 0, priority = 0):
        self.initialization_time = game_state.game_info.seconds_elapsed
        self.agent = game_state.agent
        self.manager = self.agent.action_manager
        self.manager.add(self)
        self.duration = duration
        self.delay = delay   
        self.priority = priority
        self.init()

    def __repr__(self):
        return "<Activity:{:<10} [executes at {:.2f}, for {:.2f}s]>".format(self.__class__.__name__, self.initialization_time+self.delay, self.duration)

    def init(self):
        # overwrite with initialization code for subclasses
        pass

    def should_execute(self, time):
        # DONE: check if duration and delay allow execution
        #self.agent.pipe.draw_text_2d((0, 100), (round(self.initialization_time,2), self._delay, round(time,2)))
        #self.agent.pipe.draw_text_2d((0, 150), str(self.initialization_time - self._delay >= time))
        if self.initialization_time + self.delay <= time:
            return True
        return False

    def execute(self, game_state):
        # Overwrite this for an action
        pass

    def should_remove(self, time):
        # DONE: check if duration and delay has been surpassed
        if self.initialization_time + self.delay + self.duration <= time:
            
            return True 
        
        return False

class Throttle(Action):

    def __init__(self, game_state, throttle = 1, **kwargs):
        super().__init__(game_state, **kwargs)
        self.throttle = throttle

    def execute(self, game_state):
        game_state.controller.throttle = self.throttle

class Turn(Action):
    
    def __init__(self, game_state, turn = 0, **kwargs):
        super().__init__(game_state, **kwargs)
        self.turn = turn

    def execute(self, game_state):
        game_state.controller.steer = self.turn
        #print("set turn to %s" % self.turn)

class Jump(Action):

    
    def init(self):
        self.jump = True

    def execute(self, game_state):
        game_state.controller.jump = self.jump

class Handbrake(Action):
    
    def init(self):
        self.handbrake = True

    def execute(self, game_state):
        game_state.controller.handbrake = self.handbrake

class Boost(Action):

    def init(self):
        self.boost = True

    def execute(self, game_state):
        game_state.controller.boost = self.boost

class Roll(Action):
    
    def __init__(self, game_state, roll = 0, **kwargs):
        super().__init__(game_state, **kwargs)
        self.roll = roll

    def execute(self, game_state):
        game_state.controller.roll = self.roll


class Pitch(Action):
    
    def __init__(self, game_state, pitch = 0, **kwargs):
        super().__init__(game_state, **kwargs)
        self.pitch = pitch

    def execute(self, game_state):
        game_state.controller.pitch = self.pitch

class Yaw(Action):
    
    def __init__(self, game_state, yaw = 0, **kwargs):
        super().__init__(game_state, **kwargs)
        self.yaw = yaw

    def execute(self, game_state):
        game_state.controller.yaw = self.yaw



