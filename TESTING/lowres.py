import arcade

# Define the low-res and physical screen sizes
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 240
SCALE = 4
SCREEN_WIDTH = VIRTUAL_WIDTH * SCALE
SCREEN_HEIGHT = VIRTUAL_HEIGHT * SCALE

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Low Res Arcade Game")
        self.render_texture = arcade.Texture.create_empty("RenderTexture", (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        
    def on_draw(self):
        """ Render the screen. """
        # Use the render texture to draw on
        self.render_texture(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)

        # ... Your drawing commands here ...
        arcade.draw_text("Hello Low Res World!", VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2, arcade.color.WHITE, 16, anchor_x="center")

        # Draw the low-res render texture to the screen, scaled up
        self.render_texture.draw_sized(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)

# Create and run the game
game = MyGame()
arcade.run()
