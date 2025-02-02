import pygame
import pygame_gui
from globals import *
from login_ui import LoginUI
from menu_ui import MenuUI
from story_ui import StoryUI
from combat_ui import CombatUI

class UIController:
    def __init__(self, main_character):
        pygame.init()
        self.__running = True
        self.__current_screen = "login"
        self.main_character = main_character
        
    def run(self):
        while self.__running:
            # Depending on the current screen, show the relevant UI class
            if self.__current_screen == "login":
                current_ui = LoginUI()
            elif self.__current_screen == "menu":
                current_ui = MenuUI()
            elif self.__current_screen == "combat":
                current_ui = CombatUI(self.main_character)
            elif self.__current_screen == "story":
                current_ui = StoryUI()
            else:
                self.__running = False
                return

            # Run the UI and get the next screen
            self.__current_screen = current_ui.run()  # This method returns the next screen

            # Handle quitting
            if self.__current_screen == "quit":
                self.__running = False

        pygame.quit()

if __name__ == "__main__":
    ui_controller = UIController()
    ui_controller.run()
