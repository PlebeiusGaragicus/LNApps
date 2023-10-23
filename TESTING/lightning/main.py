import pygame
import random
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LIGHTNING_COLOR = (250, 218, 94)
SPEED = 20
SPREAD = 40
BRANCH_PROBABILITY = 0.2  # Probability for creating a new branch
BRANCH_LIMIT = 7  # Limit for branching out
LINE_WIDTH = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lightning Effect")


def rand_in_range(start, end):
    return random.randint(start, end)


class Bolt:
    def __init__(self, start_point, angle=90, depth=0):
        self.start_point = start_point
        self.angle = angle
        self.point = list(start_point)
        self.children = []
        self.depth = depth

    def draw(self):
        radians = self.angle * math.pi / 180

        end_point = [
            self.point[0] + math.cos(radians) * SPEED,
            self.point[1] + math.sin(radians) * SPEED
        ]

        pygame.draw.line(screen, LIGHTNING_COLOR, self.point, end_point, LINE_WIDTH)
        self.point = end_point

        if random.random() < BRANCH_PROBABILITY and self.depth < BRANCH_LIMIT:
            child_angle = self.angle + rand_in_range(-SPREAD, SPREAD)
            child = Bolt(self.point, child_angle, self.depth+1)
            self.children.append(child)

        for child in self.children:
            child.draw()

    def is_done(self):
        return self.point[1] >= HEIGHT


def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        main_bolt = Bolt((WIDTH // 2, 0))
        while not main_bolt.is_done():
            main_bolt.draw()

        pygame.display.flip()
        pygame.time.wait(500)  # Wait for 500 milliseconds before the next lightning

        screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

        pygame.time.wait(500)  # Add some delay between lightning strikes

    pygame.quit()


if __name__ == "__main__":
    main()
