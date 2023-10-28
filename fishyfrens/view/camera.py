import pygame

from gamelib.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.utils import lerp

from fishyfrens.config import *

# BUFFER = SCREEN_WIDTH // 3
# BUFFER = min(100, SCREEN_WIDTH // 3)


class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.target = None
        # self.camera_overpan = None
        self.camera_overpan_x = min(100, PLAYFIELD_WIDTH // 3)
        self.camera_overpan_y = min(100, PLAYFIELD_HEIGHT // 3)

    def resize_playfield(width: int, height: int) -> None:
        # self.camera_overpan = min(100, SCREEN_WIDTH // 3)
        pass

    def update(self):

        if self.target == None:
            self.offset = pygame.Vector2(0, 0)
            return

        if PLAYFIELD_WIDTH > SCREEN_WIDTH:
            # player_ratio_x = self.target.rect.x / ( PLAYFIELD_WIDTH - self.camera_overpan_x )
            player_ratio_x = self.target.rect.x / ( PLAYFIELD_WIDTH )
            max_camera_x = PLAYFIELD_WIDTH - SCREEN_WIDTH + self.camera_overpan_x
            # offx = max_camera_x * player_ratio_x - BUFFER // 3
            offx = max_camera_x * player_ratio_x - self.camera_overpan_x // 2
            self.offset.x = lerp(self.offset.x, offx, 0.2) # 0.02
        else:
            # centered
            # self.offset.x = SCREEN_WIDTH // 2 - PLAYFIELD_WIDTH // 2
            self.offset.x = -(PLAYFIELD_WIDTH // 2)

        if PLAYFIELD_HEIGHT > SCREEN_HEIGHT:
            # player_ratio_y = self.target.rect.y / ( PLAYFIELD_HEIGHT - self.camera_overpan_y )
            player_ratio_y = self.target.rect.y / PLAYFIELD_HEIGHT
            max_camera_y = PLAYFIELD_HEIGHT - SCREEN_HEIGHT + self.camera_overpan_y
            # offy = max_camera_y * player_ratio_y - BUFFER // 3
            offy = max_camera_y * player_ratio_y - self.camera_overpan_y // 2
            self.offset.y = lerp(self.offset.y, offy, 0.2)
        else:
            self.offset.y = -(PLAYFIELD_HEIGHT // 2)

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


CAMERA: Camera = Camera()
