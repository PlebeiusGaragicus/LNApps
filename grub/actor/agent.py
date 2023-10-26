import os
import random
import enum
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.colors import Colors, arcade_colors

from grub.config import *
from grub.app import MY_DIR
from grub.actor.steeringbehaviour import SteeringBehaviour, BehaviorType

WALL_BOUNCE_ATTENUATION = 0.80
SNAKE_STARTING_POS = (170, 170)
TOP_SPEED = 50


class AgentType(enum.Enum):
    Shrimp = enum.auto()
    Crab = enum.auto()
    Octopus = enum.auto()
    Fish = enum.auto()
    Dolphin = enum.auto()
    Shark = enum.auto()
    Whale = enum.auto()
    Humpback = enum.auto()



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
                                   velocity=pygame.Vector2(1, 1),
                                   heading=pygame.Vector2(1, 1))

        self.type = type

        if type == AgentType.Shrimp:
            self.position.x = random.randint(0, SCREEN_WIDTH)
            self.position.y = random.randint(0, SCREEN_HEIGHT)
            self.velocity.x = random.randint(-2, 2)
            self.velocity.y = random.randint(-2, 2)
            self.max_speed = 9
            self.max_force = 0.08
            self.deceleration_tweaker = 1.4
            self.behavior_type = BehaviorType.FLEE
            self.wall_behavior = 'bounce'
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'yellowshot.PNG')).convert_alpha()
        elif type == AgentType.Crab:
            self.position.x = random.randint(0, SCREEN_WIDTH)
            self.position.y = random.randint(0, SCREEN_HEIGHT)
            self.velocity.x = random.randint(-2, 2)
            self.velocity.y = random.randint(-2, 2)
            self.max_speed  = 12 #4
            self.max_force  = 0.1 #0.05
            self.deceleration_tweaker = 2.4
            self.behavior_type = BehaviorType.SEEK
            self.wall_behavior = 'bounce'
            self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'purplesquare2.PNG')).convert_alpha()

        # self.image.set_colorkey((0, 0, 0))
        # self.rect = self.image.get_rect()
        self.size = pygame.Vector2(self.image.get_size())
        self.rect = self.image.get_rect(topleft=self.position) # <-- this is the key to getting the collision detection bounding box to move with the sprite
        self.mask = pygame.mask.from_surface(self.image)


        self.invisible = False
        self.dead = False


    def update(self, player):
        if self.dead:
            return

        # super().update() # this is the SteeringBehaviour update() and isn't working - perhaps because there are multiple inherited classes?
        self.update_steering()

        # TODO - just use a type class...
        if self.wall_behavior == 'bounce':
            self.bounce_off_walls(attenuate=True)
        elif self.wall_behavior == 'wrap':
            self.wrap_screen()
        else:
            logger.warning("Unknown wall behavior: %s", self.wall_behavior)
        
        self.rect.topleft = self.position

    def draw(self):
        if not self.invisible:
            image = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(0, -1)))
            APP_SCREEN.blit(image, (int(self.position.x), int(self.position.y)))

        self.draw_vectors()

        # pygame.draw.rect(APP_SCREEN, Colors.WHITE, self.rect, 2)




    def bounce_off_walls(self, attenuate: bool = True) -> None:
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.x > SCREEN_WIDTH - self.size.x:
            self.position.x = SCREEN_WIDTH - self.size.x
            self.velocity.x *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -WALL_BOUNCE_ATTENUATION if attenuate else -1
        if self.position.y > SCREEN_HEIGHT - self.size.y:
            self.position.y = SCREEN_HEIGHT - self.size.y
            self.velocity.y *= -WALL_BOUNCE_ATTENUATION if attenuate else -1

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH - self.size.x
        if self.position.x > SCREEN_WIDTH - self.size.x:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT - self.size.x
        if self.position.y > SCREEN_HEIGHT - self.size.x:
            self.position.y = 0
