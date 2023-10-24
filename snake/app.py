import os
import platform
import json
import logging
logger = logging.getLogger()

import pygame

from gamelib.logger import setup_logging
from gamelib.singleton import Singleton
from gamelib.viewstate import ViewStateManager

from snake.config import *

MY_DIR = os.path.dirname(os.path.abspath(__file__))
APP_SCREEN: pygame.Surface = None
SCREEN_HEIGHT = None
SCREEN_WIDTH = None
FPS = 10




class App(Singleton):
    manifest: dict = None
    manager: ViewStateManager = None
    running: bool = None


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

        #### load manifest
        manifest_path = os.path.join( MY_DIR, 'manifest.json' )
        with open( manifest_path ) as f:
            app.manifest = json.load(f)
        logger.debug("manifest: %s", app.manifest)

        #### setup app variables
        pygame.init()
        pygame.font.init() # really needed?
        app.clock = pygame.time.Clock()

        _info = pygame.display.Info()
        app.width, app.height = _info.current_w, _info.current_h
        if platform.system() == "Darwin":
            app.height -= 34 # TODO - this is a hack for the macbook air menu bar / camera cutout

        logger.debug("Display size: %s x %s", app.width, app.height)

        if platform.system() == "Darwin":
            app.screen = pygame.display.set_mode((app.width, app.height), flags=pygame.NOFRAME)
        else:
            app.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)


        global APP_SCREEN
        APP_SCREEN = app.screen
        global SCREEN_WIDTH
        SCREEN_WIDTH = app.width
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = app.height

        pygame.display.set_caption( app.manifest['name'] )

        app.viewmanager = ViewStateManager()

        from snake.views.mainmenu import MainMenuView
        from snake.views.gameplay import GameplayView
        from snake.views.gameover import GameOverView
        app.viewmanager.add_view("main_menu", MainMenuView())
        app.viewmanager.add_view("gameplay", GameplayView())
        app.viewmanager.add_view("game_over", GameOverView())

        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        # game.window.set_mouse_visible(False)

        return cls._instance


    def start(self):
        logger.debug("App.start()")

        self.viewmanager.run_view("main_menu")

        self.running = True
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False
                    self.viewmanager.handle_event(event)

                self.viewmanager.update()
                self.viewmanager.draw()

                pygame.display.flip()
                self.clock.tick(FPS)
        except Exception as e:
            # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
            logger.exception(e)
            raise e

        pygame.quit()
