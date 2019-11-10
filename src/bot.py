import math, numpy as np

import behaviour.strategy
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from gamestate import GameState
from util.pipe import RenderPipe
from util.constants import consts

from actiomatic.action import *
from behaviour.agent import BehaviourAgent


class Starbot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up

        # Fetch controller state and make a deep copy of blank controller state
        self.controller_state = SimpleControllerState()
        self.pipe = RenderPipe(self.renderer, self.logger)

        self.info = self.get_field_info()
        self.action_manager = ActionManager(self)
        self.behaviour_agent = BehaviourAgent(self.action_manager)

        self.pipe = RenderPipe(self.renderer, self.logger)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
    
        game_state = GameState(packet, self, SimpleControllerState() )

        self.behaviour_agent.set_controller_state(game_state)

        self.pipe.render()

        self.action_manager.run_actions(game_state)
        return game_state.controller

    def draw_ball_prediction(self, packet):
            ball_prediction = self.get_ball_prediction_struct()

            if ball_prediction is not None:
                list_locations = [slice.physics.location for slice in ball_prediction.slices]

            for slice in ball_prediction.slices:
                if slice.physics.location.z <= consts.ball_radius + 1:
                    action_display = "Time to impact: %s" % round(slice.game_seconds - packet.game_info.seconds_elapsed, 2)
                    self.pipe.draw_text_3d(slice.physics.location, action_display)
                    break


            self.pipe.draw_polyline_3d(list_locations)
