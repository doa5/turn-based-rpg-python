import pygame
import pygame_gui
from globals import *
pygame.init()
from message_display import MessageDisplay

class StoryUI:
    def __init__(self):
        self.__screen = SCREEN
        self.__manager = UI_MANAGER  # GUI Manager initialisation
        self.__clock = CLOCK
        self._message_display = MessageDisplay()
        
        self.__dialogue = [
            "Hello.",
            "This is an example of visual novel dialogue.",
            "End."
        ]
        self.__current_dialogue = 0
        
        # Defining UI elements  
        self.__dialogue_box = pygame_gui.elements.UITextBox(
            html_text=self.__dialogue[self.__current_dialogue],  
            relative_rect=pygame.Rect((50, SCREEN_HEIGHT - 150), (SCREEN_WIDTH - 100, 120)),
            manager=self.__manager,
            object_id="#dialoguebox"  # For theming in the future
        )
        
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
                if event.type == pygame.MOUSEBUTTONDOWN:  # Handling dialogue progression
                    if self.__current_dialogue < len(self.__dialogue) - 1:
                        self.__current_dialogue += 1
                        # Update the text on the dialogue box
                        self.__dialogue_box.set_text(self.__dialogue[self.__current_dialogue])
                    else:
                        running = False

            # Refresh and update
            self.__manager.update(time_delta)
            self.__screen.fill((0, 0, 0))

            # Drawing a white border around the dialogue box
            pygame.draw.rect(self.__screen, (255, 255, 255), pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 120), 3)  

            # Draw UI
            self.__manager.draw_ui(self.__screen)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    story_ui = StoryUI()  # Instantiate StoryUI
    story_ui.run()  # Run the StoryUI
