import time
import logging
logger = logging.getLogger()

import arcade

from grub.app import GAME_WINDOW
from grub.config import LIFE_SUCK_RATE

# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 30

SNAKE_STARTING_POS = (20, 20)

BORDER_WIDTH = 6

TOP_SPEED = 10

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50
        self.texture = arcade.make_soft_square_texture(self.size, arcade.color.YELLOW, center_alpha=255, outer_alpha=55)

        # self.center_x = 100
        # self.center_y = 100

        self.speed_x = 1
        self.speed_y = 1

        self.life = 100
        self.last_life_loss = time.time()


        self.snake = []
        for i in range(10):
            self.snake.append((SNAKE_STARTING_POS[0] + (i * 4) * self.speed_x, SNAKE_STARTING_POS[1] + (i * 4) * self.speed_y))


    def update(self):
        # lose life every second
        if time.time() > self.last_life_loss + 1:
            self.life -= LIFE_SUCK_RATE
            self.last_life_loss = time.time()
            # logger.info("life: %s", self.life)

        # self.center_x += self.dir_x
        # self.center_y += self.dir_y

        # if self.center_x > GAME_WINDOW.width - self.size // 2:
        #     self.dir_x = -self.dir_x
        # elif self.center_x < 0 + self.size // 2:
        #     self.dir_x = -self.dir_x

        # if self.center_y > GAME_WINDOW.height - self.size // 2 - TOP_BAR_HEIGHT:
        #     self.dir_y = -self.dir_y
        # elif self.center_y < 0 + self.size // 2:
        #     self.dir_y = -self.dir_y


        ### MOVEMENT AND CONFINEMENT
        head = self.snake[0]
        new_head = (head[0] + self.speed_x, head[1] + self.speed_y)

        if new_head[0] < BORDER_WIDTH:
            self.speed_x = -self.speed_x
            new_head = (BORDER_WIDTH, new_head[1])

        if new_head[0] > GAME_WINDOW.width - BORDER_WIDTH - self.size:
            self.speed_x = -self.speed_x
            new_head = (GAME_WINDOW.width - BORDER_WIDTH - self.size, new_head[1])

        if new_head[1] < BORDER_WIDTH:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], BORDER_WIDTH)
        
        if new_head[1] > GAME_WINDOW.height - BORDER_WIDTH - self.size:
            self.speed_y = -self.speed_y
            new_head = (new_head[0], GAME_WINDOW.height - BORDER_WIDTH - self.size) # hmmm

        self.snake.insert(0, new_head)
        self.snake.pop()

    
    def draw(self):
        for i in range(len(self.snake) - 1):
            arcade.draw_lrwh_rectangle_textured(self.snake[i][0], self.snake[i][1], self.size - i, self.size - i, self.texture)
            # arcade.draw_xywh_rectangle_filled(self.snake[i][0], self.snake[i][1], self.size - i, self.size - i, arcade.color.WHITE)
            # arcade.draw_line(
            #     self.snake[i][0] + self.size / 2, self.snake[i][1] + self.size / 2, self.snake[i + 1][0] + self.size / 2, self.snake[i + 1][1] + self.size / 2,
            #     arcade.color.WHITE,
            #     line_width=self.size - i)

                # # [self.snake[i][0] + self.bigness / 2, self.snake[i][1] + self.bigness / 2, self.snake[i + 1][0] + self.bigness / 2, self.snake[i + 1][1] + self.bigness / 2],
                # fill=SNAKE_COLOR,
                # # width= i + self.bigness)
                # # width=i + 1)
                # width=self.bigness - i)



    def change_speed(self, delta: int) -> None:
        if self.speed_x != 0:
            self.speed_x -= delta if self.speed_x > 0 else -delta
        if self.speed_y != 0:
            self.speed_y -= delta if self.speed_y > 0 else -delta


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