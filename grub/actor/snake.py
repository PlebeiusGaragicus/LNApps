import os
import time
import logging
logger = logging.getLogger()


from gamelib.globals import *
from gamelib.colors import Colors, arcade_colors

from grub.app import MY_DIR
from grub.config import LIFE_SUCK_RATE

# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 30

SNAKE_STARTING_POS = (20, 20)

BORDER_WIDTH = 6

TOP_SPEED = 6

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50
        # self.texture = pygame.image.load("./grub/resources/img/whiteplayer.PNG").convert_alpha()
        self.texture = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'whiteplayer.PNG')).convert_alpha()


        self.speed_x = 1
        self.speed_y = 1

        self.life = 100
        self.last_life_loss = time.time()


        self.snake = []
        self.snake.append(SNAKE_STARTING_POS)
        for i in range(10):
            self.snake.append((SNAKE_STARTING_POS[0] + (i * 4) * self.speed_x, SNAKE_STARTING_POS[1] + (i * 4) * self.speed_y))


    def update(self):
        # lose life every second
        if time.time() > self.last_life_loss + 1:
            self.life -= LIFE_SUCK_RATE
            self.last_life_loss = time.time()
            # logger.info("life: %s", self.life)

        ### MOVEMENT AND CONFINEMENT
        head = self.snake[0]
        new_head = (head[0] + self.speed_x, head[1] + self.speed_y)

        if new_head[0] < BORDER_WIDTH:
            self.speed_x = -self.speed_x
            new_head = (BORDER_WIDTH, new_head[1])

        if new_head[0] > SCREEN_WIDTH - BORDER_WIDTH - self.size:
            self.speed_x = -self.speed_x
            new_head = (SCREEN_WIDTH - BORDER_WIDTH - self.size, new_head[1])

        if new_head[1] < BORDER_WIDTH:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], BORDER_WIDTH)
        
        if new_head[1] > SCREEN_HEIGHT - BORDER_WIDTH - self.size:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], SCREEN_HEIGHT - BORDER_WIDTH - self.size) # hmmm

        self.snake.insert(0, new_head)
        self.snake.pop()

    
    def draw(self):
        # for i in range(len(self.snake) - 1):
        for i in range(len(self.snake) - 1, 0, -1):
            # pygame.draw.rect(APP_SCREEN, self.texture, (self.snake[i][0], self.snake[i][1], self.size - i, self.size - i))
            APP_SCREEN.blit(self.texture, (self.snake[i][0], self.snake[i][1]))


    def change_speed_cap(self, x_delta: int = None, y_delta: int = None) -> None:
        if x_delta is not None:
            if abs(self.speed_x) > TOP_SPEED:
                self.speed_x = TOP_SPEED if self.speed_x > 0 else -TOP_SPEED # cap to TOP SPEED
                if self.speed_y != 0: # ... the goal is to reduce the X speed by 1, if not zero
                    self.speed_y -= 1 if self.speed_y > 0 else -1 # move the X speed down (towards zero)
            else:
                self.speed_x += x_delta # do the speed increase

        if y_delta is not None:
            if abs(self.speed_y) > TOP_SPEED:
                self.speed_y = TOP_SPEED if self.speed_y > 0 else -TOP_SPEED # cap to TOP SPEED
                if self.speed_x != 0: # ... the goal is to reduce the X speed by 1, if not zero
                    self.speed_x -= 1 if self.speed_x > 0 else -1 # move the X speed down (towards zero)
            else:
                self.speed_y += y_delta # do the speed increase
