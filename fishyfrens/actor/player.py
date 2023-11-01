import os
import math
import random
import time
import logging
logger = logging.getLogger()


from gamelib.globals import *
from gamelib.colors import Colors
from gamelib.utils import lerp_color

import fishyfrens.debug as debug
from fishyfrens.config import *
from fishyfrens.app import App

from fishyfrens.view.camera import camera
from fishyfrens.audio import audio

# from fishyfrens.level import level
from fishyfrens.actor.singletons import level



class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()

        self.name = name
        self.top_speed = 5
        self.position = pygame.Vector2(random.randint(100, camera().playfield_width - 100), random.randint(100, camera().playfield_height - 100))  # Use Vector2 for position
        self.velocity = pygame.Vector2(random.randint(-2, 2), random.randint(-2, 2))  # Use Vector2 for velocity
        self.velocity_dampening = 0.97
        self.acceleration = pygame.Vector2(0, 0)

        self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', f'player{self.name}.png')).convert_alpha()
        self.scale_by = 3
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_by), int(self.image.get_height() * self.scale_by)))
        self.image = pygame.transform.flip(self.image, True, False)
        self.flipped = False
        self.size = pygame.Vector2(self.image.get_size())
        self.image_orientation: pygame.Vector2 = pygame.Vector2(1, 0)

        # self.rect = self.image.get_rect()
        # NOTE: this is the key to getting the collision detection bounding box to move with the sprite
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)

        self.life = 100
        self.last_life_loss = time.time()
        self.boost_time = 0




    def update(self):
        if time.time() > self.last_life_loss + 1:
            self.last_life_loss = time.time()
            self.adjust_life(-level().life_suck_rate)

        ### MOVEMENT AND CONFINEMENT
        # # Normalize velocity and acceleration to get direction vectors
        if self.velocity.magnitude() != 0:
            velocity_direction = self.velocity.normalize()
        else:
            velocity_direction = pygame.Vector2(0, 0)
        
        if self.acceleration.magnitude() != 0:
            acceleration_direction = self.acceleration.normalize()
        else:
            acceleration_direction = pygame.Vector2(0, 0)

        # Calculate the dot product to determine the alignment of velocity and acceleration
        dot_product = velocity_direction.dot(acceleration_direction)

        # If the dot product is less than 0, the acceleration is in a different direction than the velocity (turning)
        if dot_product < 0:
            # Apply resistance to turning by reducing the acceleration
            self.acceleration *= 0.6 # RESISTANCE TO TURNING
        else:
            # If moving in the same direction (or stopped), no need to apply the turning resistance
            self.acceleration *= 1

        self.velocity += self.acceleration
        self.acceleration *= 0.4

        # DAMPEN VELOCITY (but allow for a minimum 'drift' velocity)
        if self.velocity.magnitude() > 0.5:
            self.velocity *= self.velocity_dampening

        time_remaining = self.boost_time - time.time()
        speed_boost = max(0, time_remaining * 9) # SPEED_BOOST_AMOUNT

        if self.velocity.magnitude() > self.top_speed + speed_boost:
            self.velocity = self.velocity.normalize() * (self.top_speed + speed_boost)

        # if velocity is negative, flip the image
        if self.velocity.x < 0.0 and self.flipped == False:
            self.flipped = True
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.velocity.x > 0.0 and self.flipped == True:
            self.flipped = False
            self.image = pygame.transform.flip(self.image, False, True)

        self.position += self.velocity
        self.bounce_off_walls(attenuate=True)

        # this is necessary for the camera to follow the player (as well as the collision detection mask, I think)
        self.rect.topleft = self.position

        # Update mask for pixel-perfect collision
        # Note: Only necessary if the sprite's appearance or orientation changes
        angle = self.velocity.angle_to(self.image_orientation)
        self.rotated_image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.rotated_image)


    def draw(self):
        # angle = self.velocity.angle_to(self.image_orientation)
        # rotated_image = pygame.transform.rotate(self.image, angle)

        # Convert world coordinates to screen coordinates
        screen_pos = self.position - pygame.Vector2(camera().offset)

        if debug.DRAW_MASKS:
            # _img = pygame.transform.rotate(self.mask.to_surface(), self.velocity.angle_to(self.image_orientation))
            _img = self.mask.to_surface()
            _img.set_colorkey((0, 0, 0))
            APP_SCREEN.blit(_img, screen_pos)
        else:
            APP_SCREEN.blit(self.rotated_image, screen_pos)

        if debug.DRAW_VECTORS:
            # self.draw_vectors()
            self.draw_velocity_overlay()

        if debug.DRAW_RECTS:
            # Convert the sprite's rect to screen coordinates for drawing
            screen_rect = self.rect.copy()
            screen_rect.topleft = screen_pos
            pygame.draw.rect(APP_SCREEN, Colors.WHITE, screen_rect, 2)


    def boost(self):
        if self.life > 20:
            audio().boost()
            self.adjust_life(-8)
            self.velocity += self.velocity.normalize() * 4
            self.boost_time = time.time() + 1  # Set the boost time to 3 seconds in the future
            # TODO make a wave effect with particles or something
        else:
            # audio().too_tired()   # TODO:
            pass




    def draw_velocity_overlay(self):
        player_center = self.position + self.size // 2
        player_center -= camera().offset
        pygame.draw.line(APP_SCREEN, Colors.GREEN, player_center, player_center + self.velocity * 8, 3)
        # pygame.draw.line(APP_SCREEN, Colors.YELLOW, player_center, player_center + self.dot_product * 8, 3)


    def draw_life_bar(self):
        life_bar_width = 200
        life_bar_height = 20
        life_bar_x = SCREEN_WIDTH - life_bar_width - 20
        # life_bar_x = 20
        life_bar_y = 20

        life_bar_rect = pygame.Rect(life_bar_x, life_bar_y, life_bar_width, life_bar_height)
        pygame.draw.rect(APP_SCREEN, Colors.WHITE, life_bar_rect, 2)

        life_bar_fill_rect = pygame.Rect(life_bar_x + 2, life_bar_y + 2, life_bar_width - 4, life_bar_height - 4)
        life_bar_fill_rect.width = int(life_bar_fill_rect.width * (self.life / 100))

        color = lerp_color(Colors.RED, Colors.GREEN, self.life / 100)
        pygame.draw.rect(APP_SCREEN, color, life_bar_fill_rect)


    def bounce_off_walls(self, attenuate: bool = False):
        # TODO - this is poor collision detection, but it works for now
        # if self.position.x < BORDER_WIDTH - self.size.x // 2:
        #     self.velocity.x = abs(self.velocity.x) * PLAYER_WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.x)
        #     self.position.x = BORDER_WIDTH - self.size.x // 2
        
        # if self.position.x > PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x:
        #     self.velocity.x = -abs(self.velocity.x) * PLAYER_WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.x)
        #     self.position.x = PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x

        # self.position.x = max(BORDER_WIDTH - self.size.x // 2, self.position.x)
        self.position.x = max(0, self.position.x)
        # self.position.x = min(PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.y, self.position.x)
        self.position.x = min(camera().playfield_width - self.size.x, self.position.x)

        # if self.position.y < BORDER_WIDTH - self.size.y // 3:
        #     self.velocity.y = abs(self.velocity.y) * PLAYER_WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.y)
        #     self.position.y = BORDER_WIDTH - self.size.y // 3

        # # NOTE: position is actually the top-left of the player rect, so we need to add the full height to the player's bottom side
        # if self.position.y > PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y:
        #     self.velocity.y = -abs(self.velocity.y) * PLAYER_WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.y)
        #     self.position.y = PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y

        # self.position.y = max(BORDER_WIDTH - self.size.y // 2, self.position.y)
        # self.position.y = min(PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y, self.position.y)
        self.position.y = max(0, self.position.y)
        self.position.y = min(camera().playfield_height - self.size.y * 2, self.position.y)

    def adjust_life(self, amount: int):
        if App.get_instance().manifest.get("god_mode", False):
            return

        self.life += amount
        self.life = max(0, min(100, self.life))







# _p = None

# def create_player(name):
#     global _p
#     if _p is not None:
#         raise Exception("Player instance already exists")
#     _p = Player(name)
#     return _p

# def player():
#     # global _p # not needed as we are only accessing, not modifying it
#     if _p is None:
#         raise Exception("Player has not been created yet")
#     return _p
