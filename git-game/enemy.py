from globals import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, name, give_xp: int = 30, weakness: str = None, hp = 10, max_hp = 20, attack = 5, shield = 0, agility = 5, evasion = 5, guarded = False, healer = False):
        super().__init__(name, hp, max_hp, attack, shield, agility, evasion, guarded, healer)
        self.__give_xp = give_xp
        self.weakness = weakness

    # Getter

    def get_give_xp(self):
        return self.__give_xp

    # Methods
    
    def take_turn(self, player_party):
        self._message_display.show_message(f"{self.name} is taking their turn...")
        # Take a 2 second delay between actions.
        time.sleep(2)

        # Enemies decide an action then execute it
        chosen_action, chosen_target = self.enemy_decide_action(player_party)

        # Execute action on the target
        self.execute_action(chosen_action, chosen_target)
        time.sleep(1)

    def enemy_decide_action(self, player_party, retry_count=0):
        # Recursive enemy AI decision making function
    
        # Stopping case, if retry limit is reached, pick a random target
        if retry_count > 5:
            chosen_action = "attack"
            chosen_target = random.choice(player_party)
            return chosen_action, chosen_target

        # Determine action based on enemy health
        if self.get_hp() <= (self.get_max_hp() * 0.3):
            if self.healer:
                chosen_action = "heal"
                chosen_target = self  # Heals itself
                print(f"Enemy {self.name} chooses to heal itself due to low HP.")
                return chosen_action, chosen_target
            else:
                chosen_action = "guard"
                chosen_target = self  # Guards itself
                print(f"Enemy {self.name} chooses to guard itself due to low HP.")
                return chosen_action, chosen_target

        # If only one person in the player party is left, target them
        if len(player_party) == 1:
            chosen_action = "attack"
            chosen_target = player_party[0]
            return chosen_action, chosen_target

        # Enemy AI has 5 attacking paths.
        enemy_ai_attack_type = random.randint(1, 5)
        match enemy_ai_attack_type:
            case 1:
                # Avoid damaging a character with high evasion.
                max_evasion = 0  # Start with a value lower than any possible evasion
                avoid_target = None
                for character in player_party:
                    if character.get_evasion() > max_evasion:
                        max_evasion = character.get_evasion()
                        avoid_target = character

                # Choose target at random except the one with the highest evasion.
                available_targets = [character for character in player_party if character != avoid_target]
                
                # If available_targets is empty, try another attack method.
                if not available_targets:
                    return self.enemy_decide_action(player_party, retry_count + 1)
                
                chosen_target = random.choice(available_targets)
                chosen_action = "attack"
                print(f"Enemy {self.name} chooses to attack {chosen_target.name}, avoiding {avoid_target.name} with high evasion.")
                return chosen_action, chosen_target

            case 2:
                # Damage the character with the lowest HP.
                lowest_hp = float('inf') # Start with highest possible value
                low_hp_target = None
                for character in player_party:
                    if character.get_hp() < lowest_hp:
                        lowest_hp = character.get_hp()
                        low_hp_target = character

                chosen_target = low_hp_target
                chosen_action = "attack"
                print(f"Enemy {self.name} chooses to attack {chosen_target.name} with the lowest HP.")
                return chosen_action, chosen_target

            case 3:
                # Target the character with the highest attack.
                max_attack = 0 # Start with the lowest possible value
                high_attack_target = None
                for character in player_party:
                    if character.get_attack() > max_attack:
                        max_attack = character.get_attack()
                        high_attack_target = character

                chosen_target = high_attack_target
                chosen_action = "attack"
                print(f"Enemy {self.name} chooses to attack {chosen_target.name} with the highest attack.")
                return chosen_action, chosen_target

            case 4:
                # Target a healer character
                support_target = None
                for character in player_party:
                    if character.get_healer():
                        support_target = character
                        break
                if support_target:
                    chosen_target = support_target
                    chosen_action = "attack"
                    print(f"Enemy {self.name} chooses to attack the healer, {chosen_target.name}.")
                else:
                    return self.enemy_decide_action(player_party, retry_count + 1)

            case 5:
                # Default random attack.
                chosen_target = random.choice(player_party)
                chosen_action = "attack"
                print(f"Enemy {self.name} chooses to attack {chosen_target.name}.")
                return chosen_action, chosen_target

            case _:
                # Error: Invalid action path.
                print("ERROR: Invalid action path. Retrying...")
                return self.enemy_decide_action(player_party, retry_count + 1)

        # Fallback return (should not be reached)
        return None, None

    def execute_action(self, chosen_action, chosen_target):
        if chosen_action == "attack": # Attack target
            self.deal_damage(chosen_target)
        elif chosen_action == "guard": # Guard self
            self.perform_guard()
        elif chosen_action == "heal": # Heal self
            self.heal(chosen_target)
        else:
            print("Error: Invalid action")

    def deal_damage(self, target):
        if self.get_attack() < target.get_shield():
            shield_damage = self.get_attack() - target.get_shield()  # All damage absorbed by shield
            hp_damage = 0
        else:
            shield_damage = target.get_shield()  # All shield is gone
            hp_damage = self.get_attack() - target.get_shield()  # Remaining damage goes to HP
            
        target.apply_damage(shield_damage, hp_damage)

    def heal(self):
        heal_amount = int(self.get_hp() * 0.5)
        self.set_hp(self.get_hp() + heal_amount)
        print(f"{self.name} healed themselves for {heal_amount} HP!")
