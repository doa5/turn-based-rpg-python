from globals import *
from abc import ABC, abstractmethod

class Spell(ABC):
    def __init__(self, spell_cost: int = 5) -> None:
        self.__spell_cost = spell_cost

    # Getter
    def get_spell_cost(self):
        return self.__spell_cost

    # Abstract method
    @abstractmethod
    def cast(self):
        pass

    # Methods
    def check_MP(self, main_character, spell):
        return main_character.get_mp() >= spell.spell_cost()

class FireSpell(Spell):
    def __init__(self, spell_cost: int = 5) -> None:
        super().__init__(spell_cost)

    def cast(self, main_character, target):
        if main_character.get_magic() < target.get_shield():
            shield_damage = main_character.get_magic() - target.get_shield() # All damage has been absorbed by the shield
            hp_damage = 0
        else:
            shield_damage = target.get_shield()
            hp_damage = main_character.get_magic - target