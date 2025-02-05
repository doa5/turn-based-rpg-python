from character import Character
from enemy import Enemy

if __name__ == "__main__":
    # Create a player party with distinct stats
    player1 = Character("Player1", hp=40, max_hp=50, attack=10, evasion=10, healer=False)
    player2 = Character("Player2", hp=30, max_hp=50, attack=8, evasion=20, healer=False)
    player3 = Character("Healer", hp=25, max_hp=50, attack=5, evasion=5, healer=True)
    player_party = [player1, player2, player3]

    # Create an enemy with health above 30% so that the low-HP branch isn't triggered
    enemy = Enemy("Goblin", hp=35, max_hp=40)

    def test_case(fixed_value, description):
        print(f"--- Testing {description} ---")
        action, target = enemy.enemy_decide_action(player_party, forced_attack_type=fixed_value)
        target_info = target.name if target else "None"
        print(f"Decided action: {action}")
        print(f"Decided target: {target_info}")

    # Testing all attack paths with forced values
    test_case(1, "Case 1 (Avoid high evasion)")
    test_case(2, "Case 2 (Attack lowest HP)")
    test_case(3, "Case 3 (Attack highest attack)")
    test_case(4, "Case 4 (Attack healer)")
    test_case(5, "Case 5 (Default random attack)")
