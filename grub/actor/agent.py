import os
import random

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.colors import Colors, arcade_colors

from grub.config import *
from grub.app import MY_DIR
from grub.actor.steeringbehaviour import SteeringBehaviour

WALL_BOUNCE_ATTENUATION = 0.80
SNAKE_STARTING_POS = (170, 170)
TOP_SPEED = 50

class Agent(pygame.sprite.Sprite, SteeringBehaviour):
    def __init__(self):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        SteeringBehaviour.__init__(self=self,
                                   mass=100,
                                #    position=pygame.Vector2(SNAKE_STARTING_POS),
                                   position=pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                                   max_speed=2,
                                   max_force=0.1,
                                   velocity=pygame.Vector2(1, 1),
                                   heading=pygame.Vector2(1, 1))

        self.image = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'yellowshot.PNG')).convert_alpha()
        self.size = pygame.Vector2(self.image.get_size())

        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        # self.position = pygame.Vector2(SNAKE_STARTING_POS)
        # self.velocity = pygame.Vector2(1, 1)
        # self.acceleration = pygame.Vector2(0, 0)

    def update(self):
        # self.velocity += self.acceleration
        # self.acceleration *= 0.4
        # self.velocity.x = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.x))
        # self.velocity.y = max(-TOP_SPEED, min(TOP_SPEED, self.velocity.y))
        # self.velocity += self.seek(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.velocity += self.seek()
        self.velocity *= 1.001
        self.position += self.velocity

        self.bounce_off_walls(attenuate=True)
        # self.wrap_screen()

    def draw(self):
        image = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(0, -1)))
        APP_SCREEN.blit(image, (int(self.position.x), int(self.position.y)))

        self.draw_velocity_overlay()


    def draw_velocity_overlay(self):
        player_center = self.position + self.size / 2
        pygame.draw.line(APP_SCREEN, Colors.RED, player_center, player_center + self.velocity * 8, 3)


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
