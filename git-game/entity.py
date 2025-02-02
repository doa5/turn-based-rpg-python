from globals import *
from abc import ABC, abstractmethod
from message_display import MessageDisplay

class Entity(ABC):
    def __init__(self, name: str, hp: int =10, max_hp: int=20, attack: int=5, shield: int =0, agility: int=5, evasion: int=5, guarded: bool=False, healer: bool=False):
        self.name = name
        self.__hp = hp
        self.__max_hp = max_hp
        self.__attack = attack
        self.__shield = shield
        self.__agility = agility # Does not change
        self.__evasion = evasion # Range (1-100) does not change
        self.__guarded = guarded
        self.__healer = healer # Defines role
        self._message_display = MessageDisplay()
    
    # Getters and setters
    def set_hp(self, value):
        if value < 0:
            if self.get_hp() + value < self.get_max_hp():
                self.__hp = value
            else:
                self.__hp = self.get_max_hp()

    def get_hp(self):
        return self.__hp
      
    def set_max_hp(self, value):
        if value < 0:
            value = 0
        self.__max_hp = value

    def get_max_hp(self):
        return self.__max_hp
      
    def set_attack(self, value):
        if value < 0:
            value = 0
        self.__attack = value

    def get_attack(self):
        return self.__attack
      
    def get_agility(self):
        return self.__agility
      
    def get_evasion(self):
        return self.__evasion
      
    def set_shield(self, value):
        if value < 0:
            value = 0
        self.__shield = value

    def get_shield(self):
        return self.__shield
        
    def set_guarded(self, value):
        if isinstance(value, bool):
            self.__guarded = value

    def get_guarded(self):
        return self.__guarded

    def get_healer(self):
        return self.__healer
    
    def is_dead(self):
        return self.get_hp() <= 0
    
    # Abstract methods
    @abstractmethod
    def deal_damage(self):
        pass
    
    @abstractmethod
    def take_turn(self):
        pass

    @abstractmethod
    def execute_action(self):
        pass

    # Methods
    def evade_chance(self):
        random_value = random.randint(1, 100) 
        # Returns true if entity's evasion is higher than the random value, meaning they dodged successfully
        return random_value <= self.get_evasion()
    
    def apply_damage(self, shield_damage, hp_damage):
        self.set_shield(self.get_shield() - shield_damage)
        self._message_display.show_message(f"{self.name} shielded {shield_damage} damage!")
        
        if hp_damage > 0: # If hp damage is leftover, apply it to character
            self.set_hp(self.get_hp() - hp_damage)
            if self.get_hp() <= 0:
                self._message_display.show_message(f"{self.name} was defeated!")
            else:
                self._message_display.show_message(f"{self.name} took {hp_damage} damage!")
        else:
            # If no hp damage was taken, the attack was blocked.
            self._message_display.show_message(f"{self.name} fully blocked the attack!")

    

