import os
import sys
import platform
import time
import json
import logging
logger = logging.getLogger()
# from icecream import ic

import pygame


# from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib import globals
from gamelib.logger import setup_logging
from gamelib.singleton import Singleton
from gamelib.viewstate import ViewManager

from fishyfrens.config import *
# from fishyfrens import config

# APP_SCREEN: pygame.Surface = None
# SCREEN_HEIGHT = None
# SCREEN_WIDTH = None


SECOND_DISPLAY = False


class App(Singleton):
    manifest: dict = None
    viewmanager: ViewManager = None
    running: bool = None


    @classmethod
    def get_instance(cls) -> 'App':
        if cls._instance:
            return cls._instance
        else:
            return cls.configure_instance()

    @classmethod
    def configure_instance(cls) -> 'App':
        if cls._instance:
            raise Exception("Instance already configured")
        app = cls.__new__(cls)
        cls._instance = app

        setup_logging()

        #### load manifest
        manifest_path = os.path.join( MY_DIR, 'manifest.json' )
        with open( manifest_path ) as f:
            app.manifest = json.load(f)
        # logger.debug("manifest: %s", app.manifest)

        #### setup app variables
        pygame.init()
        pygame.font.init() # really needed?
        app.clock = pygame.time.Clock()

        # _info = pygame.display.Info()
        # app.width, app.height = _info.current_w, _info.current_h

        # if platform.system() == "Darwin":
        #     app.height -= 34 # TODO - this is a hack for the macbook air menu bar / camera cutout

        # logger.debug("Display size: %s x %s", app.width, app.height)


        if SECOND_DISPLAY:
            app.screen = pygame.display.set_mode(flags=pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN, display=1)
            _info = pygame.display.Info()
            app.width, app.height = _info.current_w, _info.current_h
        else:
            _info = pygame.display.Info()
            app.width, app.height = _info.current_w, _info.current_h

            if platform.system() == "Darwin":
                app.height -= 34 # TODO - this is a hack for the macbook air menu bar / camera cutout

                app.screen = pygame.display.set_mode((app.width, app.height), flags=pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SRCALPHA)
                # this 'hack' ensures that the newly created window becomes active
                time.sleep(0.1)
                pygame.display.toggle_fullscreen()
                time.sleep(0.1)
                pygame.display.toggle_fullscreen()
            else:
                app.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        logger.debug("Display size: %s x %s", app.width, app.height)

        pygame.display.set_allow_screensaver(False)

        if app.manifest.get("debug", False) == False:
            pygame.mouse.set_visible(False)

        # global APP_SCREEN
        globals.APP_SCREEN = app.screen
        # global SCREEN_WIDTH
        globals.SCREEN_WIDTH = app.width
        # global SCREEN_HEIGHT
        globals.SCREEN_HEIGHT = app.height

        pygame.display.set_caption( app.manifest['name'] ) # NOTE: potential KeyError

        #### setup views
        app.viewmanager = ViewManager()
        from fishyfrens.view.splash import SplashScreenView
        app.viewmanager.add_view("splash_screen", SplashScreenView())
        from fishyfrens.view.menu import MainMenuView
        app.viewmanager.add_view("main_menu", MainMenuView())
        from fishyfrens.view.gameplay import GameplayView
        app.viewmanager.add_view("gameplay", GameplayView())
        from fishyfrens.view.results import ResultsView
        app.viewmanager.add_view("results", ResultsView())


        return cls._instance


    def start(self):
        logger.debug("App.start()")

        if self.manifest_key_value('skip_to_gameplay', False) == True:
            # self.viewmanager.run_view("gameplay") # TODO clean up this manifest variable action
            self.viewmanager.run_view("main_menu")
        else:
            self.viewmanager.run_view("splash_screen")

        self.running = True
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        continue
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.running = False
                        continue

                    self.viewmanager.handle_event(event)

                self.viewmanager.update()
                self.viewmanager.draw()

                # pygame.display.update() # TODO is this needed?
                pygame.display.flip()
                self.clock.tick(FPS)

            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt")
                self.running = False

            except NotImplementedError as e:
                logger.exception(e)
                self.running = False

            except Exception as e:
                # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
                logger.exception(e)
                self.running = False

        pygame.quit()
        sys.exit()

    def stop(self):
        self.running = False
        # pygame.quit()
        # sys.exit()

    def manifest_key_value(self, key: str, default = None):
        return self.manifest.get(key, default)
