import pygame
import random


from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT

from fishyfrens.config import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
from fishyfrens.view.camera import CAMERA


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
    def __init__(self):
        self.width = int(PLAYFIELD_WIDTH * PSIZEFACTOR)
        self.height = int(PLAYFIELD_HEIGHT * PSIZEFACTOR)
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
        parallax_offset_x = parallax_range_x * (1 - CAMERA.player_ratio_x) - parallax_range_x

        parallax_range_y = self.height - SCREEN_HEIGHT
        parallax_offset_y = parallax_range_y * (1 - CAMERA.player_ratio_y) - parallax_range_y

        self.offset = pygame.Vector2(parallax_offset_x, parallax_offset_y)

        print("coff:", int(CAMERA.offset.x), "poff:", int(self.offset.x), "size:", SCREEN_WIDTH, PLAYFIELD_WIDTH, self.width, "player ratio", CAMERA.player_ratio_x)

    def draw(self):
        # self.surface.fill((0, 0, 0, 0))  # Clear surface
        # for i, layer in enumerate(self.layers):
        #     parallax_factor = 0.1 + i * 0.01
        #     offset_x = self.offset.x * parallax_factor
        #     offset_y = self.offset.y * parallax_factor
        #     for particle in layer:
        #         particle.draw(self.surface)
        self.surface.fill((0, 0, 0, 0))  # Clear surface
        for particle in self.particles:
            particle.draw(self.surface)
        for marker in self.markers:
            pygame.draw.rect(self.surface, (255, 0, 0), marker)  # Draw on parallax surface
        APP_SCREEN.blit(self.surface, (int(self.offset.x), int(self.offset.y)))
