"""
Varying packet of ALL information about the 
current state of the game
"""

class GameState:
    def __init__(self, packet, agent, controller):
        self.packet = packet
        self.packet.agent = agent
        self.packet.car = packet.game_cars[agent.team]
        self.packet.controller = controller

    def __repr__(self):
        return str(self.packet)

    def __getattr__(self, name):
        return getattr(self.packet, name)
        