# Global imports
import random
import pygame
import pygame_gui
pygame.init()
import time

# Game
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 544
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
UI_MANAGER = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

# Font
FONT = pygame.font.Font(None, 36)

# Character
LEVEL_UP_XP = 100
