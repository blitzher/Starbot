"""
Varying packet of ALL information about the 
current state of the game
"""

class GameState:
    def __init__(self, packet, agent):
        self.packet = packet
        self.packet.append(agent)
        