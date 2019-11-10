"""
implementation of strategies
"""

from behaviour.agent import Activity
from actiomatic.action import *

class KickOff(Activity):
    
    def set_controller_state(self, game_state):
        self.get_information(game_state)
        self.drive_to(self.ball_location, game_state, boost = True, flip = True)

    @staticmethod
    def activity_available(game_state):

        available = True#game_state.game_info.is_kickoff_pause
        importance = 10 if available else 0
        return {'available': available, 'importance' : importance}