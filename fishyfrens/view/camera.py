from icecream import ic

import pygame

from gamelib.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.utils import lerp



class Camera:

    # BUFFER = SCREEN_WIDTH // 3
    # BUFFER = min(100, SCREEN_WIDTH // 3)
    # CAMERA_LERP = 0.04
    CAMERA_LERP = 0.2


    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.playfield_width = SCREEN_WIDTH
        self.playfield_height = SCREEN_HEIGHT
        self.camera_overpan_x = min(100, self.playfield_width // 3)
        self.camera_overpan_y = min(100, self.playfield_height // 3)

        print("camera overpan:", self.camera_overpan_x, self.camera_overpan_y)

        self.target = None
        self.target_ratio_x = 0
        self.target_ratio_y = 0


    def resize(self, playfield_width: int, playfield_height: int):
        self.playfield_width = playfield_width
        self.playfield_height = playfield_height
        self.camera_overpan_x = min(100, self.playfield_width // 3)
        self.camera_overpan_y = min(100, self.playfield_height // 3)



    def update(self):
        if self.target == None:
            raise Exception("Camera should have a target")
            self.offset = pygame.Vector2(0, 0)
            return

        if self.playfield_width > SCREEN_WIDTH:
            self.target_ratio_x = self.target.rect.x / ( self.playfield_width - self.camera_overpan_x - self.target.rect.width)
            max_camera_x = self.playfield_width - SCREEN_WIDTH + self.camera_overpan_x // 2
            offx = max_camera_x * self.target_ratio_x - self.camera_overpan_x // 2
            self.offset.x = lerp(self.offset.x, offx, Camera.CAMERA_LERP)
        else:
            self.offset.x = (self.playfield_width // 2) - SCREEN_WIDTH // 2 # centered

        if self.playfield_height > SCREEN_HEIGHT:
            self.target_ratio_y = self.target.rect.y / ( self.playfield_height - self.camera_overpan_y - self.target.rect.height * 2) # * 2 because it's an oblong fishy
            max_camera_y = self.playfield_height - SCREEN_HEIGHT + self.camera_overpan_y // 2
            offy = max_camera_y * self.target_ratio_y - self.camera_overpan_y // 2
            self.offset.y = lerp(self.offset.y, offy, Camera.CAMERA_LERP)
        else:
            self.offset.y = (self.playfield_height // 2) - SCREEN_HEIGHT // 2 # centered


_camera = None

def camera() -> Camera:
    global _camera
    if _camera is None:
        _camera = Camera()
    return _camera
