import math, numpy as np

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
from util.pipe import RenderPipe

from copy import deepcopy

class MyBot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up

        # Fetch controller state and make a deep copy of blank controller state
        self.controller_state = SimpleControllerState()
        self.pipe = RenderPipe(self.renderer, self.logger)

        self.info = self.get_field_info()

        # Get BehaviourAgent. Used to retrieve activities and controller states
        self.BehaviourAgent = BehaviourAgent(self)

        # Store relevant constant information for all behaviour agent
        self.flipping = False
        self.activity = None
        info = self.get_field_info()

        self.pipe = RenderPipe(self.renderer, self.logger)

        # Find the own and opponent goal
        self.own_goal = info.goals[self.team]
        self.opp_goal = info.goals[self.team + 1 % info.num_goals]

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        self.draw_ball_prediction(packet)

        if not self.BehaviourAgent.activity:
            old_activity = self.BehaviourAgent.activity.__class__.__name__
            self.BehaviourAgent.get_activity(packet)
            new_activity = self.BehaviourAgent.activity.__class__.__name__

        self.controller_state = self.BehaviourAgent.get_controller_state(packet)

        self.pipe.render()

        return self.controller_state

    def draw_ball_prediction(self, packet):
            ball_prediction = self.get_ball_prediction_struct()

            if ball_prediction is not None:
                list_locations = [slice.physics.location for slice in ball_prediction.slices]

            for slice in ball_prediction.slices:
                if slice.physics.location.z <= consts.ball_radius + 1:
                    action_display = "Time to impact: %s" % round(slice.game_seconds - packet.game_info.seconds_elapsed, 2)
                    self.pipe.draw_text(slice.physics.location, action_display)
                    break


            self.pipe.draw_polyline(list_locations)
