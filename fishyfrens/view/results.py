import time
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.viewstate import View
from gamelib.menuaction import MenuAction
from gamelib.colors import Colors, arcade_color
from gamelib.text import text

from fishyfrens.app import App
from fishyfrens.config import AFK_TIMEOUT
from fishyfrens.audio import audio



class ResultsView( View ):
    def __init__(self):
        super().__init__()

        self.last_input = time.time()

        self.selected_menu_item = 0
        self.menu_actions = []
        self.menu_action = []
        self.menu_actions.append( MenuAction("Play Again!", self.revive) )
        # self.menu_actions.append( MenuAction("Revive ($)", self.revive) )
        self.menu_actions.append( MenuAction("Give up", self.main_menu) )


    def revive(self):
        audio().you_died_effect.stop()
        App.get_instance().viewmanager.run_view("gameplay")

    def main_menu(self):
        audio().you_died_effect.stop()
        App.get_instance().viewmanager.run_view("main_menu")


    def setup(self):
        # audio().you_died()
        audio().you_died_effect.play()


    def update(self):
        if time.time() > self.last_input + AFK_TIMEOUT: # self-destruct in ten seconds if no input (user is AFK)
            logger.warning("AFK timeout reached, exiting game - user is AFK!")
            self.main_menu()



    def draw(self):
        APP_SCREEN.fill((0, 0, 0))

        text(APP_SCREEN, "GAME OVER", (APP_SCREEN.get_width() // 2, APP_SCREEN.get_height() * 0.2), font_size=200, color=Colors.RED, center=True)

        x = SCREEN_WIDTH * 0.1
        y = SCREEN_HEIGHT // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade_color.YELLOW
                text(APP_SCREEN, "<", (x + 500, y + i * 100), font_size=90, color=color)
            else:
                color = arcade_color.AIR_FORCE_BLUE
            # TODO - go for a monospaced font here
            text(APP_SCREEN, menu_item.name, (x, y + i * 100), font_size=80, color=color)


    def handle_event(self, event):
        self.last_input = time.time()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                if self.selected_menu_item > 0:
                    self.selected_menu_item -= 1

            elif event.key == pygame.K_DOWN:
                if self.selected_menu_item < len(self.menu_actions) - 1:
                    self.selected_menu_item += 1

            elif event.key == pygame.K_RETURN:
                self.menu_actions[self.selected_menu_item].action()

            elif event.key == pygame.K_ESCAPE:
                self.main_menu()
