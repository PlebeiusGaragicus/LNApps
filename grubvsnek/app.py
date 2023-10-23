import os
import platform
import json
import logging
logger = logging.getLogger()

import pygame

from gamelib.logger import setup_logging
from gamelib.singleton import Singleton
from gamelib.viewstate import ViewStateManager

from grubvsnek.config import *

APP_SCREEN: pygame.Surface = None
SCREEN_HEIGHT = None
SCREEN_WIDTH = None


class App(Singleton):
    manifest: dict = None
    manager: ViewStateManager = None


    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        else:
            return cls.configure_instance()

    @classmethod
    def configure_instance(cls):
        if cls._instance:
            raise Exception("Instance already configured")
        app = cls.__new__(cls)
        cls._instance = app

        setup_logging()

        # load manifest
        manifest_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'manifest.json' )
        with open( manifest_path ) as f:
            app.manifest = json.load(f)

        #### setup app variables! ####
        pygame.init()
        app.width, app.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if platform.system() == "Darwin":
            app.screen = pygame.display.set_mode((app.width, app.height), flags=pygame.NOFRAME)
        else:
            app.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)

        logger.debug("Display size: %s x %s", app.width, app.height)

        global APP_SCREEN
        APP_SCREEN = app.screen
        global SCREEN_WIDTH
        SCREEN_WIDTH = app.width
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = app.height

        pygame.display.set_caption("Snake Game")
        app.clock = pygame.time.Clock()
        app.manager = ViewStateManager()

        from grubvsnek.views.mainmenu import MainMenu
        from grubvsnek.views.gameplay import Gameplay
        from grubvsnek.views.gameover import GameOver
        app.manager.add_state("main_menu", MainMenu())
        app.manager.add_state("gameplay", Gameplay())
        app.manager.add_state("game_over", GameOver())

        app.window_title = app.manifest['name']
        logger.debug("manifest: %s", app.manifest)


        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        # game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        self.manager.change_state("main_menu")

        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    self.manager.handle_event(event)

                self.manager.update()
                self.manager.draw()

                pygame.display.flip()
                self.clock.tick(FPS)
        except Exception as e:
            # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
            logger.exception(e)
            raise e

        pygame.quit()
