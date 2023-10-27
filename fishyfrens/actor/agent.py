import os
import random
import enum
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.colors import Colors

import fishyfrens.debug as debug
from fishyfrens.config import *
from fishyfrens.app import MY_DIR
from fishyfrens.actor.steeringbehaviour import SteeringBehaviour, BehaviorType, NULL_VECTOR
from fishyfrens.view.camera import CAMERA


# TODO: For the edge of the screen??? the wall boundary?  Nah, fix this
SAFE_BUFFER = 100



class AgentType(enum.Enum):
    Dot = enum.auto()
    Shrimp = enum.auto()
    Crab = enum.auto()
    Octopus = enum.auto()
    Fish = enum.auto()
    Dolphin = enum.auto()
    Shark = enum.auto()
    Whale = enum.auto()
    Humpback = enum.auto()



class BoundaryBehaviour(enum.Enum):
    Bounce = enum.auto()
    Wrap = enum.auto()



class Agent(pygame.sprite.Sprite, SteeringBehaviour):
    def __init__(self, type: AgentType):
        pygame.sprite.Sprite.__init__(self)
        
        position = pygame.Vector2(
            random.randint(SAFE_BUFFER, PLAYFIELD_WIDTH - SAFE_BUFFER),
            random.randint(SAFE_BUFFER, PLAYFIELD_HEIGHT - SAFE_BUFFER)
        )
        
        velocity = pygame.Vector2(
            random.randint(-1, 1),
            random.randint(-1, 1)
        )

        self.image_orientation: pygame.Vector2 = pygame.Vector2(0, -1)

        self.type = type
        if type == AgentType.Dot:
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'dotfish.png')).convert_alpha()
            SteeringBehaviour.__init__(self,
                                       mass=1,
                                       position=position,
                                       max_speed=1.8,
                                       max_force=0.5,
                                       velocity=velocity,
                                       decay_rate=8,
                                       max_sight=400,
                                       behavior_type=BehaviorType.FLEE)

        elif type == AgentType.Shrimp:
            r = random.randint(1, 3)
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', f'shrimp{r}.png')).convert_alpha()
            SteeringBehaviour.__init__(self,
                                       mass=1,
                                       position=position,
                                       max_speed=1.3,
                                       max_force=0.3,
                                       velocity=velocity,
                                       decay_rate=5,
                                       max_sight=400,
                                       behavior_type=BehaviorType.FLEE)

        elif type == AgentType.Crab:
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'kraken.png')).convert_alpha()
            # scale_by = 1
            # self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_by), int(self.image.get_height() * scale_by)))
            self.image_orientation = pygame.Vector2(-1, 1)

            # override the velocity to make the crabs slow
            velocity = pygame.Vector2( random.randint(-4, 4), random.randint(-4, 4) ) / 10
            # velocity /= 10
            SteeringBehaviour.__init__(self,
                                       mass=1,
                                       position=position,
                                    #    max_speed=1.7,
                                       max_speed=3,
                                    #    max_force=0.3,
                                       max_force=0.3,
                                       velocity=velocity,
                                    #    decay_rate=1.5,
                                       decay_rate=0.1,
                                       max_sight=300,
                                       behavior_type=BehaviorType.SEEK)

        else:
            raise Exception(f"Unknown AgentType: {type}")

        self.wall_behavior: BoundaryBehaviour = BoundaryBehaviour.Bounce
    
        # self.image.set_colorkey((0, 0, 0))
        # self.rect = self.image.get_rect()
        self.size = pygame.Vector2(self.image.get_size())
        self.rect = self.image.get_rect(topleft=self.position) # <-- this is the key to getting the collision detection bounding box to move with the sprite
        self.mask = pygame.mask.from_surface(self.image)

        # self.invisible = False
        self.hide_out_of_sight = False
        self.dead = False



    def update(self):
        if self.dead:
            return

        # super().update() # this is the SteeringBehaviour update() and isn't working - perhaps because there are multiple inherited classes?
        self.update_steering()

        # TODO - just use a type class...
        if self.wall_behavior == BoundaryBehaviour.Bounce:
            self.bounce_off_walls(attenuate=True)
        elif self.wall_behavior == BoundaryBehaviour.Wrap:
            self.wrap_screen()

        # self.rect.topleft = self.position # NOTE: this is being done in draw (not sure i even need a rect...) but it also needs to be offset by the camera

        # Update mask for pixel-perfect collision
        # Note: Only necessary if the sprite's appearance or orientation changes
        # angle = self.velocity.angle_to(self.image_orientation)
        # rotated_image = pygame.transform.rotate(self.image, angle)
        # self.mask = pygame.mask.from_surface(rotated_image)
        self.rect.topleft = self.position

        # Update mask for pixel-perfect collision
        # Note: Only necessary if the sprite's appearance or orientation changes
        angle = self.velocity.angle_to(self.image_orientation)
        rotated_image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(rotated_image)



    # def draw(self):
    #     if debug.DRAW_MASKS:
    #         _img = pygame.transform.rotate(self.mask.to_surface(), self.velocity.angle_to(self.image_orientation))
    #         _img.set_colorkey((0, 0, 0))
    #     else:
    #         _img = pygame.transform.rotate(self.image, self.velocity.angle_to(self.image_orientation))

    #     _pos = pygame.Vector2(self.position.x - CAMERA.offset.x, self.position.y - CAMERA.offset.y)
    #     APP_SCREEN.blit(_img, _pos)

    #     if debug.DRAW_VECTORS:
    #         self.draw_vectors()

    #     if debug.DRAW_RECTS:
    #         self.rect = self.image.get_rect(topleft=_pos)
    #         pygame.draw.rect(APP_SCREEN, Colors.WHITE, self.rect, 2)

    def draw(self):
        # only show agents within "sight" of the player
        if self.hide_out_of_sight:
            if self.position.distance_to(self.target.position) > self.max_sight:
                return

        angle = self.velocity.angle_to(self.image_orientation)
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Convert world coordinates to screen coordinates
        screen_pos = self.position - pygame.Vector2(CAMERA.offset)

        # Draw the sprite at its screen position
        # APP_SCREEN.blit(rotated_image, screen_pos)

        # self.rect = self.image.get_rect(topleft=pos)

        if debug.DRAW_MASKS:
            # _img = pygame.transform.rotate(self.mask.to_surface(), self.velocity.angle_to(self.image_orientation))
            _img = self.mask.to_surface()
            _img.set_colorkey((0, 0, 0))
            APP_SCREEN.blit(_img, screen_pos)
            # mask_surface = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
            # mask_surface.fill((255, 0, 0, 100))  # Red with alpha transparency
            # mask_surface.blit(rotated_image, (0, 0), None, pygame.BLEND_RGBA_MULT)
            # APP_SCREEN.blit(mask_surface, screen_pos)
        else:
            APP_SCREEN.blit(rotated_image, screen_pos)

        
        if debug.DRAW_VECTORS:
            self.draw_vectors()
            
        if debug.DRAW_RECTS:
            # Convert the sprite's rect to screen coordinates for drawing
            screen_rect = self.rect.copy()
            screen_rect.topleft = screen_pos
            pygame.draw.rect(APP_SCREEN, Colors.WHITE, screen_rect, 2)



    def bounce_off_walls(self, attenuate: bool = True) -> None:
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -AGENT_WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.x > PLAYFIELD_WIDTH - self.size.x:
            self.position.x = PLAYFIELD_WIDTH - self.size.x
            self.velocity.x *= -AGENT_WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -AGENT_WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y > PLAYFIELD_WIDTH - self.size.y:
            self.position.y = PLAYFIELD_WIDTH - self.size.y
            self.velocity.y *= -AGENT_WALL_BOUNCE_ATTENUATION if attenuate else -1



    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = PLAYFIELD_WIDTH - self.size.x
        if self.position.x > PLAYFIELD_WIDTH - self.size.x:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = PLAYFIELD_WIDTH - self.size.x
        if self.position.y > PLAYFIELD_WIDTH - self.size.x:
            self.position.y = 0
