import random
from icecream import ic

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
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

        self.parallax_background = ParallaxBackground(SCREEN_WIDTH * PSIZEFACTOR,
                                                      SCREEN_HEIGHT * PSIZEFACTOR)

        self.target = None
        self.target_ratio_x = 0
        self.target_ratio_y = 0


    def resize(self, playfield_width: int, playfield_height: int):
        self.playfield_width = playfield_width
        self.playfield_height = playfield_height
        self.camera_overpan_x = min(100, self.playfield_width // 3)
        self.camera_overpan_y = min(100, self.playfield_height // 3)
        self.parallax_background = ParallaxBackground(playfield_width * PSIZEFACTOR,
                                                      playfield_height * PSIZEFACTOR)



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
        
        self.parallax_background.update()


    def draw_effects(self):
        self.parallax_background.draw()

_camera = None

def camera() -> Camera:
    global _camera
    if _camera is None:
        _camera = Camera()
    return _camera










class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(0.8, 3)
        self.color = (random.randint(200, 255), random.randint(170, 245), 255, random.randint(60, 140))
        self.velocity = [random.uniform(-0.2, 0.4), random.uniform(-0.2, 0.6)]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# PSIZEFACTOR = 0.3
PSIZEFACTOR = 1.3
PARLLAX_PARTICLES = 500 # TODO: This should be a function of the playfield size (particle density)


class ParallaxBackground:
    def __init__(self, width, height):
        # self.width = int(camera().playfield_width * PSIZEFACTOR)
        # self.height = int(camera().playfield_height * PSIZEFACTOR)
        self.width = int( width )
        self.height = int( height )
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # self.layers = [[Particle(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)] for _ in range(3)]
        self.particles = [Particle(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(500)]  # 100 particles
        self.offset = pygame.Vector2(0, 0)

        self.markers = [
            pygame.Rect(0, 0, 10, 10),  # Top Left
            pygame.Rect(0, self.height // 5, 10, 10),  # Top Left
            pygame.Rect(self.width - 10, 0, 10, 10),  # Top Right
            pygame.Rect(0, self.height - 10, 10, 10),  # Bottom Left
            pygame.Rect(self.width - 10, self.height - 10, 10, 10),  # Bottom Right
        ]

    def update(self):
        for particle in self.particles:
                particle.update()
        # for layer in self.layers:
        #     for particle in layer:
        #         particle.update()

        parallax_range_x = self.width - SCREEN_WIDTH
        parallax_offset_x = parallax_range_x * (1 - camera().target_ratio_x) - parallax_range_x

        parallax_range_y = self.height - SCREEN_HEIGHT
        parallax_offset_y = parallax_range_y * (1 - camera().target_ratio_y) - parallax_range_y

        self.offset = pygame.Vector2(parallax_offset_x, parallax_offset_y)


    def draw(self):
        # self.surface.fill((0, 0, 0, 0))  # Clear surface
        # for i, layer in enumerate(self.layers):
        #     parallax_factor = 0.1 + i * 0.01
        #     offset_x = self.offset.x * parallax_factor
        #     offset_y = self.offset.y * parallax_factor
        #     for particle in layer:
        #         particle.draw(self.surface)

        # TODO: really need to optimize this...
        self.surface.fill((0, 0, 0, 0))  # Clear surface
        for particle in self.particles:
            particle.draw(self.surface)
        for marker in self.markers:
            pygame.draw.rect(self.surface, (255, 0, 0), marker)  # Draw on parallax surface
        APP_SCREEN.blit(self.surface, (int(self.offset.x), int(self.offset.y)))
