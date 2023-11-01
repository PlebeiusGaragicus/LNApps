import time
import logging
logger = logging.getLogger()
# from icecream import ic

import pygame
import random

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.colors import Colors, arcade_color
from gamelib.viewstate import View
from gamelib.menuaction import MenuAction

from fishyfrens.app import App
from fishyfrens.config import *
# from fishyfrens.actor.player import create_player
from fishyfrens.actor.singletons import create_player
from fishyfrens.audio import audio



class MainMenuView(View):
    def __init__(self):
        super().__init__()
        self.last_input = time.time()

        self.menu_action = []
        self.menu_action.append( MenuAction("Play as Myca Fish", self.start_myca) )
        self.menu_action.append( MenuAction("Play as Charlie Fish", self.start_charlie) )
        # self.menu_action.append( MenuAction("Play as Presley Fish", self.start_game) )
        # self.menu_action.append( MenuAction("Purchase Power-up", None) )
        self.menu_action.append( MenuAction("Quit", App.get_instance().stop ) )
        self.menu_selected_item = 0


        # TODO
        # self.font_bg = pygame.font.Font(None, 74)
        self.font_bg = pygame.font.SysFont('Arial', 80)
        self.font_sm = pygame.font.SysFont('Arial', 54)

        self.text = self.font_bg.render('Snake Game', True, Colors.WHITE)
        # global SCREEN_WIDTH, SCREEN_HEIGHT
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        self.start_text = self.font_bg.render('Press Space to Start', True, Colors.WHITE)
        self.start_text_rect = self.start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))


    def start_game(self):
        audio().stop_bg()
        App.get_instance().viewmanager.run_view("gameplay")
    
    def start_myca(self):
        create_player(name="myca")
        self.start_game()

    def start_charlie(self):
        create_player(name="charlie")
        self.start_game()


    def setup(self):
        # NOTE: audio now started in the splash screen - but this is needed for when the results view opens the menu view
        audio().play_bg(0)


    def update(self):
        # self-destruct in ten seconds if no input (user is AFK)
        # TODO - maybe show a "you're afk" screen instead of just exiting the game? (like a screensaver or sample gameplay)
        if time.time() > self.last_input + AFK_TIMEOUT:
            logger.warning("AFK timeout reached, exiting game - user is AFK!")
            App.get_instance().quit()


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # reset the AFK timer
            self.last_input = time.time()

            if event.key == pygame.K_SPACE:
                App.get_instance().viewmanager.run_view("gameplay")

            elif event.key == pygame.K_UP:
                if self.menu_selected_item > 0:
                    self.menu_selected_item -= 1

            elif event.key == pygame.K_DOWN:
                if self.menu_selected_item < len(self.menu_action) - 1:
                    self.menu_selected_item += 1

            elif event.key == pygame.K_RETURN:
                logger.info("enter")
                self.menu_action[self.menu_selected_item].execute()



    def draw(self):
        APP_SCREEN.fill(Colors.BLACK)

        x = SCREEN_WIDTH * 0.1
        # x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2 - len(self.menu_action) * 40
        for i, menu_item in enumerate(self.menu_action):
            if i == self.menu_selected_item:
                yoff = -15
                color = Colors.YELLOW
                menu_item_text = self.font_bg.render(menu_item.name, True, color)

                # pygame.draw.rect(APP_SCREEN, color, (x - 40, y + i * 80, 20, 20))
                # TODO - draw long semi-transparent rectangle behind the text
            else:
                yoff = 0
                color = arcade_color.AIR_FORCE_BLUE
                menu_item_text = self.font_sm.render(menu_item.name, True, color)

            # menu_item_text_rect = menu_item_text.get_rect(center=(x, y + i * 80))
            menu_item_text_rect = menu_item_text.get_rect(left=x, top=y + i * 80 + yoff)
            APP_SCREEN.blit(menu_item_text, menu_item_text_rect)

            # pygame.Surface.get_rect()
