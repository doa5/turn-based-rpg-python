import random
import time
from globals import *  # Make sure LEVEL_UP_XP and any other globals are defined
from character import Character
from enemy import Enemy

if __name__ == "__main__":
    # Create dummy player party characters.
    # Different HP, attack, evasion, and healer values to trigger different decision branches
    player1 = Character("Player1", hp=40, max_hp=50, attack=10, evasion=20, healer=False)
    player2 = Character("Player2", hp=15, max_hp=50, attack=8, evasion=10, healer=True)
    player3 = Character("Player3", hp=30, max_hp=50, attack=12, evasion=5, healer=False)
    
    # Create a list of player party members.
    player_party = [player1, player2, player3]
    
    # Create an enemy.
    enemy = Enemy("Goblin", give_xp=30, hp=35, max_hp=40, attack=7, shield=2, agility=5, evasion=10, healer=False)
    
    # Print enemy's current HP for context.
    print(f"Enemy {enemy.name} has {enemy.get_hp()} HP out of {enemy.get_max_hp()}.")

    # Call enemy_decide_action using the player party.
    action, target = enemy.enemy_decide_action(player_party)
    
    # Since target is an object, we can directly use its name attribute.
    if target is not None:
        target_name = target.name
    else:
        target_name = "None"
    
    print(f"Enemy {enemy.name} decided to perform '{action}' on target: {target_name}")
