import math, numpy as np

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from gamestate import GameState

from util.orientation import Orientation
from util.vec import Vec3
from util.pipe import RenderPipe
from util.constants import consts

from actiomatic.action import Throttle

class Starbot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up

        # Fetch controller state and make a deep copy of blank controller state
        self.controller_state = SimpleControllerState()
        self.pipe = RenderPipe(self.renderer, self.logger)
        self.logger.info("initalized")

        self.info = self.get_field_info()

        self.pipe = RenderPipe(self.renderer, self.logger)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        game_state = GameState(packet, self)
        full_throttle = Throttle(game_state, throttle = 1)

        full_throttle.execute()

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
