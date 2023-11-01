import pygame
import random
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LIGHTNING_COLOR = (250, 218, 94)
SPEED = 29
SPREAD = 70
BRANCH_PROBABILITY = 0.22  # Probability for creating a new branch
BRANCH_LIMIT = 3  # Limit for branching out
BRANCH_LENGTH = 67  # Length after which branch will die out
LINE_WIDTH = 1
DIE_OUT_PROBABILITY = 0.03  # Probability for a branch to die out before reaching its length
ZIGZAG_SPREAD = 70  # Range of horizontal zig-zag for the main bolt

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lightning Effect")


def rand_in_range(start, end):
    return random.randint(start, end)


class Bolt:
    def __init__(self, start_point, angle=90, depth=0, max_length=None, is_main_bolt=False):
        self.start_point = start_point
        self.angle = angle
        self.point = list(start_point)
        self.children = []
        self.depth = depth
        self.max_length = max_length if max_length else random.randint(50, HEIGHT)
        self.current_length = 0
        self.is_main_bolt = is_main_bolt

    def draw(self):
        if self.current_length >= self.max_length or (random.random() < DIE_OUT_PROBABILITY and self.depth > 0):
            return

        radians = self.angle * math.pi / 180

        # If it's the main bolt, introduce zig-zag by slightly adjusting the angle
        if self.is_main_bolt:
            zigzag_angle = random.randint(-ZIGZAG_SPREAD, ZIGZAG_SPREAD)
            radians += zigzag_angle * math.pi / 180

        end_point = [
            self.point[0] + math.cos(radians) * SPEED,
            self.point[1] + math.sin(radians) * SPEED
        ]

        pygame.draw.line(screen, LIGHTNING_COLOR, self.point, end_point, LINE_WIDTH)
        self.point = end_point
        self.current_length += SPEED

        if random.random() < BRANCH_PROBABILITY and self.depth < BRANCH_LIMIT:
            child_angle = self.angle + rand_in_range(-SPREAD, SPREAD)
            child = Bolt(self.point, child_angle, self.depth+1, BRANCH_LENGTH)
            self.children.append(child)

        for child in self.children:
            child.draw()

    def is_done(self):
        return self.point[1] >= HEIGHT or self.current_length >= self.max_length


def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        main_bolt = Bolt((WIDTH // 2, 0), is_main_bolt=True)
        while not main_bolt.is_done():
            main_bolt.draw()
            pygame.display.flip()
            clock.tick(60)  # FPS to control growth speed

        pygame.time.wait(1000)  # Wait for 1 second before the next lightning

    pygame.quit()


if __name__ == "__main__":
    main()
