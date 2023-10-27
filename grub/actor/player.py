import os
import platform
import time
import logging
logger = logging.getLogger()


from gamelib.globals import *
from gamelib.colors import Colors

# from grub.config import LIFE_SUCK_RATE, BORDER_WIDTH, PLAYER_STARTING_POS, TOP_SPEED, WALL_BOUNCE_ATTENUATION
from grub.config import *
from grub.app import MY_DIR
from grub.view.camera import CAMERA

# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 0
if platform.system() == "Darwin":
    TOP_BAR_HEIGHT = 34





class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2(PLAYER_STARTING_POS)  # Use Vector2 for position
        self.velocity = pygame.Vector2(1, 1)  # Use Vector2 for velocity
        self.velocity_dampening = 0.96
        self.acceleration = pygame.Vector2(0, 0)  # Use Vector2 for acceleration

        self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'snakehead.PNG')).convert_alpha()
        self.size = pygame.Vector2(self.image.get_size())
        # self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(topleft=self.position) # <-- this is the key to getting the collision detection bounding box to move with the sprite
        # self.image = pygame.transform.scale(self.image, (int(self.size.x), int(self.size.y)))  # Scale image to size
        self.mask = pygame.mask.from_surface(self.image)


        self.life = 100
        self.last_life_loss = time.time()


    def update(self):
        if time.time() > self.last_life_loss + 1:
            self.life -= LIFE_SUCK_RATE
            self.last_life_loss = time.time()

        ### MOVEMENT AND CONFINEMENT

        self.velocity += self.acceleration
        self.acceleration *= 0.4
        self.velocity *= self.velocity_dampening

        self.velocity.x = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.x))
        self.velocity.y = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.y))

        self.position += self.velocity

        self.bounce_off_walls(attenuate=True)

        self.rect.topleft = self.position # <-- this is the key to getting the collision detection bounding box to move with the sprite


    def draw(self):
        # rotate the image
        _img = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(0, -1)))

        # pixel location is player pos - camera offset
        _x = int(self.position.x - CAMERA.offset.x)
        _y = int(self.position.y - CAMERA.offset.y)
        # print(f"player pos: {self.position}, camera offset: {CAMERA.offset}, draw pos: ({_x}, {_y})")
        APP_SCREEN.blit(_img, (_x, _y))

        # self.draw_velocity_overlay()
        self.draw_life_bar()

        # draw the collision detection bounding box
        # pygame.draw.rect(APP_SCREEN, Colors.WHITE, self.rect, 2)


    def draw_velocity_overlay(self):
        player_center = self.position + self.size // 2
        player_center -= CAMERA.offset
        pygame.draw.line(APP_SCREEN, Colors.GREEN, player_center, player_center + self.velocity * 8, 3)


    def draw_life_bar(self):
        life_bar_width = 200
        life_bar_height = 20
        # life_bar_x = SCREEN_WIDTH - life_bar_width - 10
        life_bar_x = 20
        life_bar_y = 20

        life_bar_rect = pygame.Rect(life_bar_x, life_bar_y, life_bar_width, life_bar_height)
        pygame.draw.rect(APP_SCREEN, Colors.WHITE, life_bar_rect, 2)

        life_bar_fill_rect = pygame.Rect(life_bar_x + 2, life_bar_y + 2, life_bar_width - 4, life_bar_height - 4)
        life_bar_fill_rect.width = int(life_bar_fill_rect.width * (self.life / 100))
        pygame.draw.rect(APP_SCREEN, Colors.RED, life_bar_fill_rect)


    def bounce_off_walls(self, attenuate: bool = False):
        if self.position.x < BORDER_WIDTH:
            self.velocity.x = abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.x)
            self.position.x = BORDER_WIDTH

        if self.position.x > PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x:
            self.velocity.x = -abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.x)
            self.position.x = PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x

        if self.position.y < BORDER_WIDTH:
            self.velocity.y = abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.y)
            self.position.y = BORDER_WIDTH

        if self.position.y > PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y:
            self.velocity.y = -abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.y)
            self.position.y = PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y

    def adjust_life(self, amount: int):
        self.life += amount
        self.life = max(0, min(100, self.life))
