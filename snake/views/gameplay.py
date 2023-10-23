import random

import pygame

from gamelib.colors import Colors
from gamelib.viewstate import ViewState

from snake.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from snake.config import *


class GameplayView(ViewState):
    def __init__(self):
        super().__init__()
        # TODO: I'm not sure how to do this best...
        self.snake = None
        self.direction = None
        self.food = None
        self.grow: bool = None


    def setup(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)  # Right
        self.food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                     random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))
        self.grow = False


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif event.key == pygame.K_ESCAPE:
                exit(0)

    def update(self):
        head_x, head_y = self.snake[0]
        new_x, new_y = self.direction
        new_head = ((head_x + new_x) % (SCREEN_WIDTH // CELL_SIZE), (head_y + new_y) % (SCREEN_HEIGHT // CELL_SIZE))

        if new_head in self.snake:
            # manager.run_view("game_over")
            App.get_instance().viewmanager.run_view("game_over")
            return

        self.snake.insert(0, new_head)
        if not self.grow:
            self.snake.pop()
        else:
            self.grow = False

        if new_head == self.food:
            self.grow = True
            self.food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                         random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))

    def draw(self):
        APP_SCREEN.fill(Colors.DARK)
        for segment in self.snake:
            pygame.draw.rect(APP_SCREEN, Colors.GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(APP_SCREEN, Colors.RED, (self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
