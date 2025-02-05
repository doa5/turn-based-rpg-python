import pygame
import time
from globals import *

class MessageDisplay:
    def __init__(self):
        self.__screen = SCREEN
        self.__font = FONT
        self.__colour = WHITE
        self.__position = (480, 50)
        self.__message = None
        self.__start_time = None
        
    def show_message(self, text):
        self.__message = text
        self.__start_time = time.time()

    def update(self):
        if self.__message:
            elapsed_time = time.time() - self.__start_time
            if elapsed_time < 2:
                text_surface = self.__font.render(self.__message, True, self.__colour)
                text_rect = text_surface.get_rect()

                # Center text and adjust vertical position
                text_rect.centerx = SCREEN_WIDTH // 2
                text_rect.y = self.__position[1]

                self.__screen.blit(text_surface, text_rect)
            else:
                self.__message = None  # Remove message after 3 seconds


if __name__ == "__main__":
    pygame.init()
    message_display = MessageDisplay()

    running = True
    while running:
        SCREEN.fill((0, 0, 0))  # Clear screen each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                message_display.show_message("Hello.")

        message_display.update()
        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()