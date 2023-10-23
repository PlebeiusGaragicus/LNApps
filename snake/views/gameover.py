import pygame

from gamelib.colors import Colors
from gamelib.viewstate import ViewState

from snake.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from snake.config import *


class GameOverView(ViewState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Game Over', True, Colors.WHITE)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.restart_text = self.font.render('Press Space to Restart', True, Colors.WHITE)
        self.restart_text_rect = self.restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    def setup(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                App.get_instance().viewmanager.run_view("gameplay")

    def draw(self):
        APP_SCREEN.fill(Colors.DARK)
        APP_SCREEN.blit(self.text, self.text_rect)
        APP_SCREEN.blit(self.restart_text, self.restart_text_rect)
