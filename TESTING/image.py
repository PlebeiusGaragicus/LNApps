import os

import arcade


MY_DIR = os.path.dirname(os.path.realpath(__file__))


class ResourceImage():
    def __init__(self, img_name):
        try:
            self.texture = arcade.load_texture( os.path.join(MY_DIR, img_name) )
        except FileNotFoundError:
            self.texture = arcade.load_texture("./missing.png")

        self.position = [0, 0]

    def draw(self):
        """Draw the slide object."""
        arcade.draw_texture_rectangle(self.position[0], self.position[1],
                                      self.texture.width, self.texture.height,
                                      self.texture)
