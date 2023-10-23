import time

import arcade

from slideobj import SlideObject, SlideMode
from gamelib.texteffect import FlashText

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class SplashScreen(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.title_slide = SlideObject("snek3.png", -300, SCREEN_HEIGHT * 0.75, 
                                       SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, slide_duration=3, mode=SlideMode.LINEAR)

        self.press_start = FlashText("Press Start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8, 24, arcade.color.YELLOW, flash=True, bold=True)



    def on_draw(self):
        arcade.start_render()

        self.press_start.draw()



    def on_update(self, delta_time):
        self.press_start.update(delta_time)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            print("Start the game!")



if __name__ == "__main__":
    window = SplashScreen(SCREEN_WIDTH, SCREEN_HEIGHT, "testing")
    arcade.run()
