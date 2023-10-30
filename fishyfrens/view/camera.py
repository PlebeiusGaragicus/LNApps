from icecream import ic

import pygame

from gamelib.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.utils import lerp

# from fishyfrens.config import *
from fishyfrens import config

# BUFFER = SCREEN_WIDTH // 3
# BUFFER = min(100, SCREEN_WIDTH // 3)

# def resize_playfield(width: int, height: int) -> None:
#     # self.camera_overpan = min(100, SCREEN_WIDTH // 3)
#     pass

# CAMERA_LERP = 0.2
# CAMERA_LERP = 0.04
CAMERA_LERP = 0.2

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.target = None
        self.camera_overpan_x = min(100, config.PLAYFIELD_WIDTH // 3)
        self.camera_overpan_y = min(100, config.PLAYFIELD_HEIGHT // 3)
        print("camera overpan:", self.camera_overpan_x, self.camera_overpan_y)
        # self.camera_overpan_x = 0
        # self.camera_overpan_y = 0

        self.player_ratio_x = 0
        self.player_ratio_y = 0


    def resize(self):
        self.camera_overpan_x = min(100, config.PLAYFIELD_WIDTH // 3)
        self.camera_overpan_y = min(100, config.PLAYFIELD_HEIGHT // 3)



    def update(self):
        if self.target == None:
            raise Exception("Camera should have a target")
            self.offset = pygame.Vector2(0, 0)
            return

        if config.PLAYFIELD_WIDTH > SCREEN_WIDTH:
            self.player_ratio_x = self.target.rect.x / ( config.PLAYFIELD_WIDTH - self.camera_overpan_x - self.target.rect.width)
            max_camera_x = config.PLAYFIELD_WIDTH - SCREEN_WIDTH + self.camera_overpan_x // 2
            offx = max_camera_x * self.player_ratio_x - self.camera_overpan_x // 2
            self.offset.x = lerp(self.offset.x, offx, CAMERA_LERP)
        else:
            self.offset.x = (config.PLAYFIELD_WIDTH // 2) - SCREEN_WIDTH // 2 # centered

        if config.PLAYFIELD_HEIGHT > SCREEN_HEIGHT:
            self.player_ratio_y = self.target.rect.y / ( config.PLAYFIELD_HEIGHT - self.camera_overpan_y - self.target.rect.height * 2) # * 2 because it's an oblong fishy
            max_camera_y = config.PLAYFIELD_HEIGHT - SCREEN_HEIGHT + self.camera_overpan_y // 2
            offy = max_camera_y * self.player_ratio_y - self.camera_overpan_y // 2
            self.offset.y = lerp(self.offset.y, offy, CAMERA_LERP)
        else:
            self.offset.y = (config.PLAYFIELD_HEIGHT // 2) - SCREEN_HEIGHT // 2 # centered

# CAMERA: Camera = Camera()










        # print(self.offset.x, self.offset.y)

        # self.offset.x = max_camera_x * player_ratio_x - BUFFER // 3
        # self.offset.y = max_camera_y * player_ratio_y - BUFFER // 3


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
