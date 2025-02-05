import pygame
import pygame_gui
from globals import *
pygame.init()
from message_display import MessageDisplay
class MenuUI:
    def __init__(self):
        self.__screen = SCREEN
        self.__manager = UI_MANAGER  # GUI Manager initialisation
        self.__clock = CLOCK
        self._message_display = MessageDisplay()

        # Defining UI elements
        self.__start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((430, 237), (100, 50)),
            text="Start",
            manager=self.__manager)
        
        self.__quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((430, 307), (100, 50)),
            text="Quit",
            manager=self.__manager)
        
    def run(self):
        running = True
        while running:
            time_delta = self.__clock.tick(60) / 1000.0  # Convert to milliseconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle GUI events
                self.__manager.process_events(event)

                # Check button clicks
                if event.type == pygame.USEREVENT:  # Handling user button interactions
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.__start_button:
                            self._message_display.show_message("Start pressed")
                            return "story"
                        if event.ui_element == self.__quit_button:
                            running = False
            
            # Update and draw UI
            self.__manager.update(time_delta)
            self.__screen.fill((0, 0, 0))
            self.__manager.draw_ui(self.__screen)
            self._message_display.update()
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    menu_ui = MenuUI()  # Instantiate MenuUI
    result = menu_ui.run()  # Run the MenuUI
    print(f"Next screen: {result}")  # Print the result (story or none)
