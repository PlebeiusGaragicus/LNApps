import pygame
import random

from gamelib.viewstate import ViewState

from grubvsnek.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from grubvsnek.config import *


class MainMenu(ViewState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Snake Game', True, WHITE)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.start_text = self.font.render('Press Space to Start', True, WHITE)
        self.start_text_rect = self.start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    def setup(self):
        print(f"{self.__class__.__name__} setup")
    
    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                App.get_instance().manager.change_state("gameplay")

    def draw(self):
        APP_SCREEN.fill(BLACK)
        APP_SCREEN.blit(self.text, self.text_rect)
        APP_SCREEN.blit(self.start_text, self.start_text_rect)
