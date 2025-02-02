import pygame
import pygame_gui
from globals import *
pygame.init()
from message_display import MessageDisplay

class CombatUI:
    def __init__(self, main_character, enemies):
        self.__screen = SCREEN
        # Initialised the Pygame GUI manager with the screen dimensions to handle all UI elements (buttons, text boxes) for the game
        self.__manager = UI_MANAGER
        self.__clock = CLOCK
        self.__enemies = enemies
        self._message_display = MessageDisplay()

        # Store main character object to check abilities
        self.main_character = main_character

        # Creating a text box to display the current dialogue, managed by the UI manager
        self.__attack_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 500), (100, 50)),
            text="Attack",
            manager=self.__manager)
        
        self.__guard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 500), (100, 50)),
            text="Guard",
            manager=self.__manager)
        
        spell_button_text = "Spell" if self.main_character.get_summon() else "Spell (Locked)"
        self.__spell_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 500), (100, 50)),
            text=spell_button_text,
            manager=self.__manager)
        
        self.__item_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 500), (100, 50)),
            text="Item",
            manager=self.__manager)
        
        self.current_action = None
        self.selected_target = None
        self.target_buttons = []  # List to store target buttons
        self.target_selection_active = False  # Flag to track if target selection is active


    def get_enemy_list(self):
        return self.__enemies

    def get_player_attack_input(self):
        # Listen for button presses and return the action chosen
        if self.current_action:
            return self.current_action  # Return the action once selected
        return None # Action is pending

    def get_player_target_input(self):
        # Return the target chosen by the player
        return self.selected_target
    
    def get_player_item_choice(self):
        pass # Show list of items to choose from
    
    def execute_guard(self):
        # Handle the guard action, no target required.
        self._message_display.show_message(f"Guarding.")
        self.selected_target = None  # No target for guarding

    def execute_item(self):
        # Handle item action (currently just a placeholder).
        self._message_display.show_message(f"Using an item.")
        # Handle item use logic (e.g., open item menu, choose item, etc.)
        self.selected_target = None  # No target for item

    def show_target_selection(self):
        # Display available targets 
        enemies = self.get_enemy_list() 
        self.target_buttons.clear()
        
        # Create buttons for each enemy
        for i, enemy in enumerate(enemies): # Take index and item
            target_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50, 100 + (i * 60)), (100, 50)),
                text=f"{enemy.name}",
                manager=self.__manager)
            
            # Store each button for later use
            self.target_buttons.append((target_button, enemy))

        self.target_selection_active = True
        # Show a message prompting to select a target
        self._message_display.show_message("Select a target!")

    def handle_target_selection(self, event):
        if self.target_selection_active:
            # Check if the player clicked on a target button
            for target_button, enemy in self.target_buttons:
                if event.ui_element == target_button:
                    self.selected_target = enemy
                    self._message_display.show_message(f"Target selected: {enemy.name}")

                    # Remove buttons after selection
                    for button, _ in self.target_buttons:
                        button.kill()

                    self.target_buttons.clear() # Clear list
                    self.target_selection_active = False
                    self.target_selected = True
                    break  # Exit the loop after selecting the target

    
    def run(self):
        running = True
        while running:
            # This is needed because pygame_gui uses it for updating UI elements
            time_delta = self.__clock.tick(60) / 1000.0 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle GUI events
                self.__manager.process_events(event)

                # Check button clicks
                if event.type == pygame.USEREVENT:  # Handling user button interactions
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.__attack_button:
                            self.current_action = "attack"
                            self.show_target_selection()
                            self.target_selected = False # Reset taget selected flag

                        elif event.ui_element == self.__guard_button:
                            self.current_action = "guard"
                            self.execute_guard()
                            self.target_selected = True # Dont need to select a target so pass
                            
                        elif event.ui_element == self.__spell_button:
                            if self.main_character.get_summon():
                                self.current_action = "spell"
                                self.show_target_selection()  
                                self.target_selected = False
                            else:
                                self._message_display.show_message("Spell not unlocked")
                                
                        elif event.ui_element == self.__item_button:
                            self.current_action = "item"
                            self.execute_item()
                            self.target_selected = True

                        if self.target_selection_active:
                            self.handle_target_selection(event)

            if self.current_action and self.target_selected:
                self.main_character.take_turn(self)
                self.current_action = None # Reset the action and target after taking a turn
                self.selected_target = None

            # Update and draw UI
            self.__manager.update(time_delta)
            self.__screen.fill((0, 0, 0))
            self.__manager.draw_ui(self.__screen)
            self._message_display.update()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    from main_character import MainCharacter
    from enemy import Enemy  

    main_character = MainCharacter("Hero", summon=True)
    enemy_1 = Enemy("Goblin", give_xp=50)
    enemy_2 = Enemy("Orc", give_xp=100)
    
    combat_ui = CombatUI(main_character, [enemy_1, enemy_2])
    
    combat_ui.run()