import os
import random
import time
import logging
logger = logging.getLogger()


from gamelib.globals import *
from gamelib.colors import Colors

import fishyfrens.debug as debug
from fishyfrens.config import *
from fishyfrens.app import MY_DIR
from fishyfrens.view.camera import CAMERA



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2(random.randint(100, PLAYFIELD_WIDTH - 100), random.randint(100, PLAYFIELD_HEIGHT - 100))  # Use Vector2 for position
        self.velocity = pygame.Vector2(random.randint(-2, 2), random.randint(-2, 2))  # Use Vector2 for velocity
        self.velocity_dampening = 0.98
        self.acceleration = pygame.Vector2(0, 0)

        self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'player.png')).convert_alpha()
        scale_by = 3
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_by), int(self.image.get_height() * scale_by)))
        self.image = pygame.transform.flip(self.image, True, False)
        self.size = pygame.Vector2(self.image.get_size())
        self.image_orientation: pygame.Vector2 = pygame.Vector2(1, 0)

        # self.rect = self.image.get_rect()
        # NOTE: this is the key to getting the collision detection bounding box to move with the sprite
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)

        self.life = 100
        self.last_life_loss = time.time()




    def update(self):
        if time.time() > self.last_life_loss + 1:
            self.life -= LIFE_SUCK_RATE
            self.last_life_loss = time.time()

        ### MOVEMENT AND CONFINEMENT
        # Normalize velocity and acceleration to get direction vectors
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
            self.acceleration *= 0.3 # max_force
        else:
            # If moving in the same direction (or stopped), no need to apply the turning resistance
            self.acceleration *= 1

        self.velocity += self.acceleration
        self.acceleration *= 0.4

        # DAMPEN VELOCITY (but allow for a minimum 'drift' velocity)
        if self.velocity.magnitude() > 0.5:
            self.velocity *= self.velocity_dampening

        if self.velocity.magnitude() > PLAYER_TOP_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_TOP_SPEED

        self.position += self.velocity
        self.bounce_off_walls(attenuate=True)

        # this is necessary for the camera to follow the player (as well as the collision detection mask, I think)
        self.rect.topleft = self.position

        # Update mask for pixel-perfect collision
        # Note: Only necessary if the sprite's appearance or orientation changes
        angle = self.velocity.angle_to(self.image_orientation)
        rotated_image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(rotated_image)


    def draw(self):
        angle = self.velocity.angle_to(self.image_orientation)
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Convert world coordinates to screen coordinates
        screen_pos = self.position - pygame.Vector2(CAMERA.offset)

        # Draw the sprite at its screen position
        APP_SCREEN.blit(rotated_image, screen_pos)

        if debug.DRAW_MASKS:
            mask_surface = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
            mask_surface.fill((255, 0, 0, 100))  # Red with alpha transparency
            mask_surface.blit(rotated_image, (0, 0), None, pygame.BLEND_RGBA_MULT)
            APP_SCREEN.blit(mask_surface, screen_pos)

        if debug.DRAW_VECTORS:
            self.draw_vectors()

        if debug.DRAW_RECTS:
            # Convert the sprite's rect to screen coordinates for drawing
            screen_rect = self.rect.copy()
            screen_rect.topleft = screen_pos
            pygame.draw.rect(APP_SCREEN, Colors.WHITE, screen_rect, 2)
        
        self.draw_life_bar()


    # def draw(self):
    #     # rotate the image based on the velocity
    #     if debug.DRAW_MASKS:
    #         # draw the collision mask and verify proper rotation, collisions.. etc
    #         # TODO - this is not working properly
    #         _img = pygame.transform.rotate(self.mask.to_surface(), self.velocity.angle_to(self.image_orientation))
    #         _img.set_colorkey((0, 0, 0))
    #     else:
    #         _img = pygame.transform.rotate(self.image, self.velocity.angle_to(self.image_orientation))

    #     # if velocity is negative, flip the image
    #     # if self.velocity.x < 0:
    #     #     _img = pygame.transform.flip(_img, False, True)

    #     # calculate camera offset and true screen pixel position
    #     _pos = pygame.Vector2(self.position.x - CAMERA.offset.x, self.position.y - CAMERA.offset.y)
    #     APP_SCREEN.blit(_img, _pos)

    #     if debug.DRAW_VECTORS:
    #         self.draw_velocity_overlay()

    #     # draw the collision detection bounding box
    #     if debug.DRAW_RECTS:
    #         self.rect = self.image.get_rect(topleft=_pos)
    #         pygame.draw.rect(APP_SCREEN, Colors.WHITE, self.rect, 2)

    #     self.draw_life_bar()



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
        # TODO - this is poor collision detection, but it works for now
        if self.position.x < BORDER_WIDTH:
            self.velocity.x = abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.x)
            self.position.x = BORDER_WIDTH

        if self.position.x > PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x // 2:
            self.velocity.x = -abs(self.velocity.x) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.x)
            self.position.x = PLAYFIELD_WIDTH - BORDER_WIDTH - self.size.x // 2

        if self.position.y < BORDER_WIDTH:
            self.velocity.y = abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else abs(self.velocity.y)
            self.position.y = BORDER_WIDTH

        if self.position.y > PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y // 2:
            self.velocity.y = -abs(self.velocity.y) * WALL_BOUNCE_ATTENUATION if attenuate else -abs(self.velocity.y)
            self.position.y = PLAYFIELD_HEIGHT - BORDER_WIDTH - self.size.y // 2

    def adjust_life(self, amount: int):
        self.life += amount
        self.life = max(0, min(100, self.life))






    # def update(self):
    #     if time.time() > self.last_life_loss + 1:
    #         self.life -= LIFE_SUCK_RATE
    #         self.last_life_loss = time.time()

    #     ### MOVEMENT AND CONFINEMENT

    #     self.velocity += self.acceleration
    #     self.acceleration *= 0.4

    #     # DAMPEN VELOCITY (but allow for a minimum 'drift' velocity)
    #     if self.velocity.magnitude() > 0.5:
    #         self.velocity *= self.velocity_dampening

    #     if self.velocity.magnitude() > PLAYER_TOP_SPEED:
    #         self.velocity = self.velocity.normalize() * PLAYER_TOP_SPEED

    #     self.position += self.velocity

    #     self.bounce_off_walls(attenuate=True)

    #     # this is necessary for the camera to follow the player (as well as the collision detection mask, I think)
    #     self.rect.topleft = self.position