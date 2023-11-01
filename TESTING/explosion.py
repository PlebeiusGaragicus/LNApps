import random
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Explosion Animation Demo"

TILE_SCALING = 0.5
CHARACTER_SCALING = 1


class AnimatedExplosion(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Used for flipping between image sequences
        self.cur_texture = 0
        # self.scale = 0.5
        self.scale = random.randint(45, 55) / 100
        self.time = 0
        self.angle = random.randint(0, 360)

        self.center_x = x
        self.center_y = y
        self.active = True  # Active when it's first created

        # Images from Kenney.nl's Asset Pack 3
        main_path = "/Users/myca/LNApps/fishyfrens/resources/img/explode/explode"

        # Load textures for walking
        self.plosion_textures = []
        for i in range(7):
            texture = arcade.load_texture(f"{main_path}{i}.png")
            self.plosion_textures.append(texture)


        # Set the initial texture
        self.texture = self.plosion_textures[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points


    def draw(self):
        super().draw()

        # hit box
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, arcade.color.RED)


    def update_animation(self, delta_time: float):
        self.time += delta_time

        if self.time > 0.06:
            self.time = 0
            self.cur_texture += 1
            if self.cur_texture > 6:
                self.active = False  # Deactivate instead of looping
                return
            self.texture = self.plosion_textures[self.cur_texture]






class Explosion(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        # self.animation = AnimatedExplosion()

        self.explosions = arcade.SpriteList()  # A list to manage explosions
        # self.explosions.append(AnimatedExplosion())  # Add an explosion when needed 

    def on_draw(self):
        arcade.start_render()
        # self.animation.draw()
        self.explosions.draw()  # Draw all active explosions

    def update(self, delta_time: float):
        # self.animation.update_animation(delta_time=delta_time)

        # Update only active explosions and remove inactive ones
        active_explosions = [explosion for explosion in self.explosions if explosion.active]
        for explosion in active_explosions:
            explosion.update_animation(delta_time)
        self.explosions = arcade.SpriteList()  # Clear the list
        self.explosions.extend(active_explosions)  # Add back only the active explosions

    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.explosions.append(AnimatedExplosion(x, y))
        # return super().on_mouse_press(x, y, button, modifiers)

if __name__ == "__main__":
    window = Explosion()
    arcade.run()
