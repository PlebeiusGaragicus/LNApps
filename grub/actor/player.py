import os
import platform
import time
import logging
logger = logging.getLogger()


from gamelib.globals import *
from gamelib.colors import Colors, arcade_colors

from grub.app import MY_DIR
from grub.config import LIFE_SUCK_RATE

# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 0
if platform.system() == "Darwin":
    TOP_BAR_HEIGHT = 34

SNAKE_STARTING_POS = (20, 20)

BORDER_WIDTH = 6

TOP_SPEED = 100

WALL_BOUNCE_ATTENUATION = 0.80


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.size = pygame.Vector2(50, 50)  # Use Vector2 for size as well
        # self.size = 50
        self.texture = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'snakehead.PNG')).convert_alpha()
        self.size = pygame.Vector2(self.texture.get_size())
        # self.texture = pygame.transform.scale(self.texture, (int(self.size.x), int(self.size.y)))  # Scale texture to size

        self.life = 100
        self.last_life_loss = time.time()

        self.position = pygame.Vector2(SNAKE_STARTING_POS)  # Use Vector2 for position
        self.velocity = pygame.Vector2(1, 1)  # Use Vector2 for velocity
        self.acceleration = pygame.Vector2(0, 0)  # Use Vector2 for acceleration

    def update(self):
        if time.time() > self.last_life_loss + 1:
            self.life -= LIFE_SUCK_RATE
            self.last_life_loss = time.time()

        ### MOVEMENT AND CONFINEMENT

        self.velocity += self.acceleration
        self.acceleration *= 0.4
        self.velocity *= 0.98

        self.velocity.x = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.x))
        self.velocity.y = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.y))

        self.position += self.velocity

        self.bounce_off_walls(attenuate=True)


    def draw(self):
        # rotate the texture
        texture = pygame.transform.rotate(self.texture, self.velocity.angle_to(pygame.Vector2(0, -1)))
        APP_SCREEN.blit(texture, (int(self.position.x), int(self.position.y)))

        self.draw_velocity_overlay()
        self.draw_life_bar()


    def draw_velocity_overlay(self):
        player_center = self.position + self.size // 2
        pygame.draw.line(APP_SCREEN, Colors.GREEN, player_center, player_center + self.velocity * 8, 3)


    def draw_life_bar(self):
        life_bar_width = 100
        life_bar_height = 10
        life_bar_x = SCREEN_WIDTH - life_bar_width - 10
        life_bar_y = 10

        life_bar_rect = pygame.Rect(life_bar_x, life_bar_y, life_bar_width, life_bar_height)
        pygame.draw.rect(APP_SCREEN, Colors.WHITE, life_bar_rect, 2)

        life_bar_fill_rect = pygame.Rect(life_bar_x + 2, life_bar_y + 2, life_bar_width - 4, life_bar_height - 4)
        life_bar_fill_rect.width = int(life_bar_fill_rect.width * (self.life / 100))
        pygame.draw.rect(APP_SCREEN, Colors.RED, life_bar_fill_rect)


    def bounce_off_walls(self, attenuate: bool = False):
        if self.position.x < BORDER_WIDTH:
            self.velocity.x = abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.x)
            self.position.x = BORDER_WIDTH

        if self.position.x > SCREEN_WIDTH - BORDER_WIDTH - self.size.x:
            self.velocity.x = -abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.x)
            self.position.x = SCREEN_WIDTH - BORDER_WIDTH - self.size.x

        if self.position.y < BORDER_WIDTH:
            self.velocity.y = abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.y)
            self.position.y = BORDER_WIDTH

        if self.position.y > SCREEN_HEIGHT - BORDER_WIDTH - self.size.y:
            self.velocity.y = -abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.y)
            self.position.y = SCREEN_HEIGHT - BORDER_WIDTH - self.size.y
