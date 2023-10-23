import os
import json
import logging
logger = logging.getLogger()

import arcade
# for type hinting
from pyglet.media import Player

from gamelib.logger import setup_logging
from gamelib.singleton import Singleton

MY_DIR = os.path.dirname(os.path.abspath(__file__))

GAME_WINDOW: arcade.Window = None





class Game(Singleton):
    window: arcade.Window = None
    manifest: dict = None

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
        game = cls.__new__(cls)
        cls._instance = game

        setup_logging()

        # load manifest
        manifest_path = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'manifest.json' )
        with open( manifest_path ) as f:
            game.manifest = json.load(f)

        window_title = game.manifest['name']
        logger.debug("manifest: %s", game.manifest)

        display_width, display_height = arcade.get_display_size()

        game.music_player: Player = None

        


        # TODO - consider making all windows resizable in order to test layout for multiple monitors
        game.window = arcade.Window(width=display_width, height=display_height, title=window_title, fullscreen=False, style="borderless")

        game.window.set_mouse_visible(False)

        return cls._instance


    def play_sound(self, file_name):
        sound_path = os.path.join(MY_DIR, 'resources', 'sounds', file_name)
        theme_sound = arcade.sound.load_sound( sound_path )
        # theme_len = arcade.sound.Sound.get_length( theme_sound )

        # self.music_player( theme_sound )
        self.music_player = arcade.sound.play_sound( theme_sound )
    

    def stop_sound(self):
        if self.music_player:
            arcade.sound.stop_sound( self.music_player )


    def start(self):
        global GAME_WINDOW
        GAME_WINDOW = self.window


        from grub.view.splash import SplashScreenView
        from grub.view.menu import MenuView

        # view = SplashScreenView( MenuView(), skip_intro=self.manifest.get('skip_intro', False) )
        view = SplashScreenView( )
        self.window.show_view(view)

        # if self.manifest.get('skip_intro', False):
        #     from grub.view.menu_screen import MenuView
        #     view = MenuView(self)
        #     self.window.show_view(view)
        # else:

        try:
            arcade.run()
        except Exception as e:
            # TODO - do something useful and cool here.. make my own exception view like the seedsigner!
            logger.exception(e)
            raise e

    def start_gameplay(self):
        from grub.view.gameplay import GameplayView
        view = GameplayView()
        self.window.show_view(view)
