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
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        SteeringBehaviour.__init__(self=self,
                                   mass=100,
                                #    position=pygame.Vector2(SNAKE_STARTING_POS),
                                   position=pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                                   max_speed=5,
                                   max_force=0.03,
                                   velocity=pygame.Vector2(1, 1))
                                #    heading=pygame.Vector2(1, 1))

        self.type = type
        self.wall_behavior: BoundaryBehaviour = BoundaryBehaviour.Bounce

        if type == AgentType.Dot:
            self.position.x = random.randint(SAFE_BUFFER, PLAYFIELD_WIDTH - SAFE_BUFFER)
            self.position.y = random.randint(SAFE_BUFFER, PLAYFIELD_HEIGHT - SAFE_BUFFER)
            # self.velocity = NULL_VECTOR
            self.velocity.x = random.randint(-2, 2)
            self.velocity.y = random.randint(-2, 2)
            self.max_speed = 3
            self.max_force = 0.5
            self.decay_rate = 8
            # self.distance_sensitivity = 0.0005
            self.behavior_type = BehaviorType.FLEE
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'particle.PNG')).convert_alpha()
        elif type == AgentType.Shrimp:
            # TODO: make a SafeXY() just like grigwars
            self.position.x = random.randint(SAFE_BUFFER, PLAYFIELD_WIDTH - SAFE_BUFFER)
            self.position.y = random.randint(SAFE_BUFFER, PLAYFIELD_HEIGHT - SAFE_BUFFER)
            # self.velocity = NULL_VECTOR
            self.velocity.x = random.randint(-2, 2)
            self.velocity.y = random.randint(-2, 2)
            self.max_speed = 1.5
            self.max_force = 0.3
            self.decay_rate = 5
            # self.distance_sensitivity = 5
            self.behavior_type = BehaviorType.FLEE
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'yellowshot.PNG')).convert_alpha()
        elif type == AgentType.Crab:
            self.position.x = random.randint(SAFE_BUFFER, PLAYFIELD_WIDTH - SAFE_BUFFER)
            self.position.y = random.randint(SAFE_BUFFER, PLAYFIELD_HEIGHT - SAFE_BUFFER)
            # self.velocity = NULL_VECTOR
            self.velocity.x = random.randint(-2, 2)
            self.velocity.y = random.randint(-2, 2)
            self.max_speed  = 2
            self.max_force  = 0.3
            self.decay_rate = 1.5
            self.max_sight = 90
            # self.distance_sensitivity = 2.4
            self.behavior_type = BehaviorType.SEEK
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'purplesquare2.PNG')).convert_alpha()
        else:
            raise Exception(f"Unknown AgentType: {type}")
    

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
        image = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(0, -1)))
        # APP_SCREEN.blit(image, (int(self.position.x), int(self.position.y)))

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
