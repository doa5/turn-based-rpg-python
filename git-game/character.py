from globals import *
from entity import Entity

class Character(Entity):
    # Class variable 
    crit_multiplier = 2

    def __init__(self, name: str, hp: int = 10, max_hp: int = 20, attack: int = 5, shield: int = 0, agility: int = 5, evasion: int = 5, guarded: bool = False, healer: bool = False, level: int = 1, xp:int = 0, crit_rate: int = 10):
        super().__init__(name, hp, max_hp, attack, shield, agility, evasion, guarded, healer)
        self.__level = level
        self.__xp = xp
        self.__crit_rate = crit_rate
        
    # Getters and setters
    def get_level(self):
        return self.__level
    
    def set_level(self, value):
        if value > 0:
            self.__level = value

    def get_xp(self):
        return self.__xp
    
    def set_xp(self, value):
        self.__xp = value

    def get_crit_rate(self):
        return self.__crit_rate

    # Methods

    def check_level_up(self):
        if self.get_xp() >= LEVEL_UP_XP:
            self.__level_up()

    def __level_up(self):
        self.set_level(self.get_level() + 1)
        self.set_attack(self.get_attack() + (self.get_level() * 2))
        self.set_max_hp(self.get_max_hp() + 10)
        self.set_xp(0) # Reseting XP after leveling up
        self._message_display.show_message("You leveled up!")

    def deal_damage(self, target):
        if self.get_attack() < target.get_shield():
            shield_damage = self.get_attack() - target.get_shield()  # All damage absorbed by shield
            hp_damage = 0
        else:
            shield_damage = target.get_shield()  # All shield is gone
            hp_damage = self.get_attack() - target.get_shield()  # Remaining damage goes to HP

        # Test for critical hit
        if self.__critical_hit_test():
            hp_damage *= Character.crit_multiplier  # Apply critical multiplier
            self._message_display.show_message(f"{self.name} landed a critical hit!")

        target.apply_damage(shield_damage, hp_damage)

    def __critical_hit_test(self):
        return random.randint(1,100) < self.get_crit_rate()

    def take_turn(self, enemies):
        self._message_display.show_message(f"{self.name} is taking their turn...")
        # Take a 2 second delay between actions.
        time.sleep(2)

        # AI controlled characters decide an action then execute it
        chosen_action, chosen_target = self.party_decide_action(enemies)

        # Execute action on the target
        self.execute_action(chosen_action, chosen_target)
        time.sleep(1)

    def execute_action(self, chosen_action, chosen_target):
        if chosen_action == "attack": # Attack target
            self.deal_damage(chosen_target)
        elif chosen_action == "guard": # Guard self
            self.perform_guard()
        elif chosen_action == "heal": # Heal target
            self.heal(chosen_target)
        else:
            print("Error: Invalid action")
    
    def party_decide_action(self, enemies, player_party, forced_attack_type=None, retry_count=0):
        # Can pass a value as parameter for testing 
        player_ai_attack_type = forced_attack_type if forced_attack_type else random.randint(1, 5)
        # Recursive decision-making function for a party member to decide an action. It returns a tuple (chosen_action, chosen_target)

        # Stopping case, if retry limit is reached, pick a random enemy
        if retry_count > 5:
            chosen_action = "attack"
            chosen_target = random.choice(enemies)
            return chosen_action, chosen_target

        # If this character is a healer, check if any party member has low HP and heal them.
        if self.get_healer():
            for character in player_party:
                if character.get_hp() <= int(character.get_max_hp() * 0.3):
                    chosen_action = "heal" # Heal character
                    chosen_target = character
                    print(f"Character {self.name} chooses to heal {chosen_target.name} because they have low HP.")
                    return chosen_action, chosen_target
        else:
            # If not a healer and HP is low, choose to guard.
            if self.get_hp() <= (self.get_max_hp() * 0.3):
                chosen_action = "guard"
                chosen_target = "self"
                print(f"Character {self.name} chooses to guard because they have low HP.")
                return chosen_action, chosen_target

        # If there is only one enemy, target that enemy.
        if len(enemies) == 1:
            chosen_action = "attack"
            chosen_target = enemies[0]
            return chosen_action, chosen_target

        # Player AI 5 decision paths
        match player_ai_attack_type:
            case 1:
                # Avoid attacking the enemy with the highest evasion.
                max_evasion = 0 # Start with a value lower than any possible evasion
                avoid_target = None
                for enemy in enemies:
                    if enemy.get_evasion() > max_evasion:
                        max_evasion = enemy.get_evasion()
                        avoid_target = enemy

                # Choose among enemies except the one with the highest evasion.
                available_targets = [enemy for enemy in enemies if enemy != avoid_target]

                if not available_targets:
                    return self.party_decide_action(enemies, retry_count + 1)
                
                chosen_target = random.choice(available_targets)
                chosen_action = "attack"
                print(f"Character {self.name} chooses to attack {chosen_target.name}, avoiding {avoid_target.name} with high evasion.")
                return chosen_action, chosen_target

            case 2:
                # Attack the enemy with the lowest HP.
                lowest_hp = float('inf')  # Start with the highest possible value
                low_hp_target = None 
                for enemy in enemies:
                    if enemy.get_hp() < lowest_hp:
                        lowest_hp = enemy.get_hp()
                        low_hp_target = enemy

                chosen_target = low_hp_target
                chosen_action = "attack"
                print(f"Character {self.name} chooses to attack {chosen_target.name} with the lowest HP.")
                return chosen_action, chosen_target

            case 3:
                # Attack the enemy with the highest attack.
                max_attack = 0  # Start with the lowest possible value
                high_attack_target = None  
                for enemy in enemies:
                    if enemy.get_attack() > max_attack:
                        max_attack = enemy.get_attack()
                        high_attack_target = enemy

                chosen_target = high_attack_target
                chosen_action = "attack"
                print(f"Character {self.name} chooses to attack {chosen_target.name} with the highest attack.")
                return chosen_action, chosen_target

            case 4:
                # Attack an enemy healer if one exists.
                support_target = None
                for enemy in enemies:
                    if enemy.get_healer():
                        support_target = enemy
                        break
                if support_target:
                    chosen_target = support_target
                    chosen_action = "attack"
                    print(f"Character {self.name} chooses to attack the healer, {chosen_target.name}.")
                    return chosen_action, chosen_target
                else:
                    return self.party_decide_action(enemies, retry_count + 1)

            case 5:
                # Default: perform a random attack.
                chosen_target = random.choice(enemies)
                chosen_action = "attack"
                print(f"Character {self.name} chooses to attack {chosen_target.name}.")
                return chosen_action, chosen_target

            case _: 
                # Error
                print("ERROR: Invalid action path. Retrying...")
                return self.party_decide_action(enemies, retry_count + 1)

        # Fallback return (should not be reached).
        return None, None

    def deal_damage(self, target):
        if self.get_attack() < target.get_shield():
            shield_damage = self.get_attack() - target.get_shield()  # All damage absorbed by shield
            hp_damage = 0
        else:
            shield_damage = target.get_shield()  # All shield is gone
            hp_damage = self.get_attack() - target.get_shield()  # Remaining damage goes to HP

            # Test for critical hit
            if self.__critical_hit_test():
                hp_damage *= Character.crit_multiplier  # Apply critical multiplier
                self._message_display.show_message(f"{self.name} landed a critical hit!")

        target.apply_damage(shield_damage, hp_damage)

    def heal(self, healed, player_party):
        if healed in player_party:
            heal_amount = int(healed.get_hp() * 0.5)
            healed.set_hp(healed.get_hp() + heal_amount)
            print(f"{self.name} healed {healed.name} for {heal_amount} HP!")
        else:
            print(f"ERROR: {healed.name} is not an ally. Healing failed.")

if __name__ == "__main__":
    char1 = Character("Hero", crit_rate=100)
    crit_test_result = char1.__critical_hit_test() # Should be successful
    print(crit_test_result)


    