import os
import random
import enum
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.colors import Colors

from grub.config import *
from grub.app import MY_DIR
from grub.actor.steeringbehaviour import SteeringBehaviour, BehaviorType, NULL_VECTOR
from grub.view.camera import CAMERA

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
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'dotfish.PNG')).convert_alpha()
            SteeringBehaviour.__init__(self,
                                       mass=1,
                                       position=position,
                                       max_speed=1.5,
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
                                       max_speed=1.1,
                                       max_force=0.3,
                                       velocity=velocity,
                                       decay_rate=5,
                                       max_sight=400,
                                       behavior_type=BehaviorType.FLEE)

        elif type == AgentType.Crab:
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'crab.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))
            self.image_orientation = pygame.Vector2(-1, 1)

            # override the velocity to make the crabs slow
            velocity = pygame.Vector2( random.randint(-4, 4), random.randint(-4, 4) ) / 10
            # velocity /= 10
            SteeringBehaviour.__init__(self,
                                       mass=1,
                                       position=position,
                                       max_speed=1.7,
                                       max_force=0.3,
                                       velocity=velocity,
                                       decay_rate=1.5,
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

        self.rect.topleft = self.position

    def draw(self):
        # image = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(0, -1)))
        image = pygame.transform.rotate(self.image, self.velocity.angle_to(self.image_orientation))

        _pos = pygame.Vector2(self.position.x - CAMERA.offset.x, self.position.y - CAMERA.offset.y)
        APP_SCREEN.blit(image, _pos)

        # self.draw_vectors()



    def bounce_off_walls(self, attenuate: bool = True) -> None:
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.x > PLAYFIELD_WIDTH - self.size.x:
            self.position.x = PLAYFIELD_WIDTH - self.size.x
            self.velocity.x *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y > PLAYFIELD_WIDTH - self.size.y:
            self.position.y = PLAYFIELD_WIDTH - self.size.y
            self.velocity.y *= -WALL_BOUNCE_ATTENUATION if attenuate else -1

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = PLAYFIELD_WIDTH - self.size.x
        if self.position.x > PLAYFIELD_WIDTH - self.size.x:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = PLAYFIELD_WIDTH - self.size.x
        if self.position.y > PLAYFIELD_WIDTH - self.size.x:
            self.position.y = 0
