from globals import *

class Combat:
    def __init__(self, player_party: list = [], enemies: list = []):
        self.__player_party = player_party
        self.__enemies = enemies
        self.__participants = player_party + enemies

        def get_player_party(self):
            return self.__player_party
        
        def get_enemies(self):
            return self.__enemies
        
        def start_combat(self):
            pass