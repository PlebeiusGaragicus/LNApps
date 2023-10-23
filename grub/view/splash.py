import time
import logging
logger = logging.getLogger()

import arcade

from gamelib.texteffect import FlashText

from grub.app import GAME_WINDOW, Game


class SplashScreenView( arcade.View ):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.skip_intro = False

        self.press_start = FlashText("Press Start", GAME_WINDOW.width / 2, GAME_WINDOW.height / 8, 24, arcade.color.YELLOW, flash=True, bold=True)


    def on_show_view(self):
        super().on_show_view()
        arcade.set_background_color(arcade.color.BLACK)

        Game.get_instance().play_sound( "epic-background.wav" )




    def on_update(self, delta_time):
        if self.skip_intro:
            Game.get_instance().stop_sound()

            from grub.view.menu import MenuView
            self.window.show_view( MenuView() )

        self.press_start.update(delta_time)




    def on_draw(self):
        arcade.start_render()

        self.press_start.draw()


    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER:
            self.skip_intro = True
