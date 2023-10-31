import time
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.viewstate import View
from gamelib.colors import arcade_color
from gamelib.text import text

# NOTE - untested!
from gamelib.texteffect import FlashText

from fishyfrens.app import App
from fishyfrens.audio import audio

AUTO_ADVANCE_SEC = 20
MANDITORY_WAIT_SEC = 2


class SplashScreenView( View ):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.skip_intro = False

        # self.press_start = FlashText("Press Start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8, 24, arcade_color.YELLOW, flash=True, bold=True)


    def setup(self):
        audio().play_bg()


    def update(self):
        if time.time() - self.start_time > AUTO_ADVANCE_SEC: # just move on to the main menu after awhile...
            self.skip_intro = True

        if self.skip_intro == True:
            App.get_instance().viewmanager.run_view("main_menu")

    
        if time.time() - self.start_time > MANDITORY_WAIT_SEC:
            pass
            # self.press_start.update(delta_time)



    def draw(self):
        APP_SCREEN.fill((10, 50, 50))

        text(APP_SCREEN, "your friends are...", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4), font_size=100, color=arcade_color.CYBER_YELLOW, center=True)
        text(APP_SCREEN, "Fishy!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), font_size=120, color=arcade_color.BLUSH, center=True)
        text(APP_SCREEN, "I'm a fishy... you're a fishy... we're all a little fishy!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.85), font_size=30, color=arcade_color.BLUE_GREEN, center=True)

        if time.time() - self.start_time > MANDITORY_WAIT_SEC:
            pass
            # self.press_start.draw()


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            print(time.time() - self.start_time)
            if time.time() - self.start_time > MANDITORY_WAIT_SEC:
                self.skip_intro = True
