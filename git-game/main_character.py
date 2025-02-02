from globals import *
from character import Character

class MainCharacter(Character):
    def __init__(self, name: str, hp: int = 10, max_hp: int = 20, attack: int = 5, shield: int = 0, agility: int = 5, evasion: int = 5, guarded: bool = False, healer: bool = False, level: int = 1, xp: int = 0, crit_rate: int = 5, summon: bool = False, spell: object = None, magic: int = 0, mp: int = 0, max_mp: int = 0, current_node_id: int = 1, player_party: list = []):
        super().__init__(name, hp, max_hp, attack, shield, agility, evasion, guarded, healer, level, xp, crit_rate, player_party)
        self.__summon = summon
        self.__spell = spell
        self.__magic = magic
        self.__mp = mp
        self.__max_mp = max_mp
        self.__current_node_id = current_node_id

    # Getters and setters
    def get_summon(self):
        return self.__summon
    
    def set_spell(self, object):
        self.__spell = object

    def get_spell(self):
        return self.__spell
    
    def set_magic(self, value):
        if value > 0:
            self.__magic += value

    def get_magic(self):
        return self.__magic
    
    def set_mp(self, value):
        if value > 0:
            self.__mp += value

    def get_max_mp(self):
        return self.__max_mp

    def set_max_mp(self, value):
        if value > 0:
            self.__max_mp += value

    def get_current_node_id(self):
        return self.__current_node_id
    
    def set_current_node_id(self, id_num):
        self.__current_node_id = id_num

    # Methods

    def take_turn(self, combat_ui):
        chosen_action = combat_ui.get_player_attack_input()
        
        if chosen_action == None:
            return
        
        # Handle actions based on what the player selects
        if chosen_action == "item":
            # If "Item" action, item would need to be selected
            chosen_item = combat_ui.get_player_item_choice()
            self.execute_action(chosen_action, None, chosen_item)
        elif chosen_action == "guard":
            self.execute_action(chosen_action, None)
        else:
            # For attack and spell, we need the target
            chosen_target = combat_ui.get_player_target_input()
            self.execute_action(chosen_action, chosen_target)

    def execute_action(self, chosen_action, chosen_target, chosen_item=None):
        if chosen_action == "attack":
            #self.deal_damage(chosen_target) removed during testing
            #print(f"{self.name} attacks {chosen_target.name}")
            print(f"{self.name} attacks {chosen_target.name}")
        elif chosen_action == "guard":
            #self.perform_guard() removed during testing
            print(f"{self.name} guards")
        elif chosen_action == "spell":
            if self.get_summon():
                # self.cast_spell(chosen_target)  Future implementation
                print(f"{self.name} spell")
            else:
                print(f"{self.name} cannot cast spell (spell not unlocked).")
        elif chosen_action == "item":
            print(f"{self.name} uses item") # *Implement item handling after database

    def unlock_summon(self):
        self.__summon = True
    
    def reroll_initiative(self):
        pass

    def training(self):
        STATS_TO_INCREASE = {"attack": 5, "max_hp": 10}
        for stat, increment in STATS_TO_INCREASE.items():
            if stat == "attack":
                self.set_attack(self.get_attack() + increment)
            elif stat == "max_hp":
                self.set_max_hp(self.get_max_hp() + increment)
        print(f"{self.name} trained and increased their stats.")



if __name__ == "__main__":
    hero = MainCharacter(name="Hero", attack=10, max_hp=50)
    print(f"Before training: Attack = {hero.get_attack()}, Max HP = {hero.get_max_hp()}")
    hero.training()
    print(f"After training: Attack = {hero.get_attack()}, Max HP = {hero.get_max_hp()}")