import pygame

from grub.config import *
from grub.view.gameplay import SCREEN_WIDTH, SCREEN_HEIGHT

BUFFER = SCREEN_WIDTH // 3

def lerp(a, b, t):
    return a + (b - a) * t

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.target = None

    def update(self):
        if self.target == None:
            self.offset = pygame.Vector2(0, 0)
            return

        player_ratio_x = self.target.rect.x / ( PLAYFIELD_WIDTH - BUFFER )
        player_ratio_y = self.target.rect.y / ( PLAYFIELD_HEIGHT - BUFFER )

        max_camera_x = PLAYFIELD_WIDTH - SCREEN_WIDTH
        max_camera_y = PLAYFIELD_HEIGHT - SCREEN_HEIGHT

        self.offset.x = max_camera_x * player_ratio_x - BUFFER // 3
        self.offset.y = max_camera_y * player_ratio_y - BUFFER // 3

        # self.offset.x = self.target.rect.x - int(SCREEN_WIDTH / 2)
        # self.offset.y = self.target.rect.y - int(SCREEN_HEIGHT / 2)

        # OLD WAY THAT WORKS... v1
        # self.offset.x = self.target.rect.x - int(SCREEN_WIDTH / 2)
        # self.offset.y = self.target.rect.y - int(SCREEN_HEIGHT / 2)


        # DOESN"T SEEM TO DO ANYTHING
        # self.offset.x = lerp(self.offset.x, self.target.rect.x - int(SCREEN_WIDTH / 2), 0.5)
        # self.offset.y = lerp(self.offset.y, self.target.rect.y - int(SCREEN_HEIGHT / 2), 0.5)

        # DO I EVEN NEED THIS...?
        # if self.target.rect.x < self.offset.x:
        #     self.offset.x = self.target.rect.x
        # if self.target.rect.right > self.offset.x + SCREEN_WIDTH:
        #     self.offset.x = self.target.rect.x - SCREEN_WIDTH
        # if self.target.rect.y < self.offset.y:
        #     self.offset.y = self.target.rect.y
        # if self.target.rect.bottom > self.offset.y + SCREEN_HEIGHT:
        #     self.offset.y = self.target.rect.y - SCREEN_HEIGHT


CAMERA: Camera = Camera()
