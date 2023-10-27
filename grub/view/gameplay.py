import time
import random
import math
import logging
logger = logging.getLogger()

import pygame

from gamelib.colors import Colors
from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.cooldown_keys import CooldownKey, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from gamelib.viewstate import View

# from grub.config import HOLD_TO_QUIT_SECONDS, COOLDOWN_DIRECTIONAL_SECONDS
from grub.config import *
from grub.actor.player import Player
from grub.actor.agent import Agent, AgentType
from grub.actor.steeringbehaviour import BehaviorType
from grub.view.camera import CAMERA







class GameplayView(View):
    def __init__(self):
        super().__init__()

        ### CONTROL
        self.start_time = time.time()
        self.last_agent_spawn_time = time.time()
        self.last_flee_agent_spawn_time = time.time()
        self.last_seek_agent_spawn_time = time.time()

        self.paused = False
        self.escape_pressed_time = None
        self.alive = True
        self.cooldown_keys: dict[CooldownKey] = {
            # KEY_UP: CooldownKey(pygame.K_w, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_DOWN: CooldownKey(pygame.K_s, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_LEFT: CooldownKey(pygame.K_a, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_RIGHT: CooldownKey(pygame.K_d, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_UP: CooldownKey(pygame.K_UP, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_DOWN: CooldownKey(pygame.K_DOWN, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_LEFT: CooldownKey(pygame.K_LEFT, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_RIGHT: CooldownKey(pygame.K_RIGHT, COOLDOWN_DIRECTIONAL_SECONDS),
        }

        ### UI
        self.border_width = 6

        ### AGENTS
        # self.camera = Camera()
        self.player: Player = Player()
        CAMERA.target = self.player
        self.actor_group = pygame.sprite.Group()


    def revive(self):
        self.player.alive = True
        self.player.life = 100

        for key in self.cooldown_keys.values():
            key.reset()


    def setup(self):
        pass


    def update(self):
        if self.player.life <= 0 or self.alive is False:
            from grub.view.results import ResultsView
            next_view = ResultsView(self)
            self.window.show_view(next_view)

        if self.paused:
            return

        # every 10 seconds...
        while len(self.actor_group) < MAX_AGENTS:
            # ten percent chance:
            if random.randint(1, 100) <= 10:
                self.spawn_seek_agent()
            else:
                # 50 percent chance:
                if random.randint(1, 100) <= 50:
                    self.spawn_flee_agent()
                else:
                    self.spawn_dot_agent()


        # if time.time() > self.last_flee_agent_spawn_time + AGENT_SPAWN_INTERVAL_SECONDS:
        #     self.last_flee_agent_spawn_time = time.time()
        #     self.spawn_flee_agent()

        # if time.time() > self.last_seek_agent_spawn_time + AGENT_SPAWN_INTERVAL_SECONDS * 10:
        #     self.last_seek_agent_spawn_time = time.time()
        #     self.spawn_seek_agent()


        self.handle_cooldown_keys()
        # player_rect = self.player.texture.get_rect()
        # self.actor_group.update(player=self.player)
        self.actor_group.update()
        self.player.update()

        collisions = pygame.sprite.spritecollide(self.player, self.actor_group, False, pygame.sprite.collide_mask)
        for agent in collisions:
            logger.info("Player collided with agent")
            # agent.dead = True
            if agent.type == AgentType.Shrimp:
                # self.player.adjust_life(6)
                pass
            elif agent.type == AgentType.Crab:
                # self.player.adjust_life(-10)
                pass

            self.actor_group.remove(agent)
            del agent

        # self.camera.update( self.player )
        CAMERA.update()




    def draw(self):
        APP_SCREEN.fill(Colors.BLACK)

        # draw a border around the game window
        # arcade.draw_rectangle_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.GREEN, border_width=self.border_width)
        # pygame.draw.rect(APP_SCREEN, Colors.GREEN, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), self.border_width)

        # draw a line from 0,0 to 0, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        # pygame.draw.line(APP_SCREEN, Colors.GREEN, (0, 0), (0, SCREEN_HEIGHT), self.border_width)
        pygame.draw.line(APP_SCREEN, Colors.GREEN, _start, _end, self.border_width)

        # draw a line from 0,0 to screen width, 0 using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        pygame.draw.line(APP_SCREEN, Colors.GREEN, _start, _end, self.border_width)

        # draw a line from screen width, 0 to screen width, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        pygame.draw.line(APP_SCREEN, Colors.GREEN, _start, _end, self.border_width)

        # draw a line from 0, screen height to screen width, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        pygame.draw.line(APP_SCREEN, Colors.GREEN, _start, _end, self.border_width)


        # show life in top left corner
        # TODO
        # arcade.draw_text(f"Life: {self.player.life}", 10, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, font_size=20, anchor_x="left")

        # show player x and y direction
        # TODO
        # arcade.draw_text(f"dir_x: {self.player.speed_x} / dir_y: {self.player.speed_y}", SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.9, arcade.color.YELLOW, font_size=20, anchor_x="center")

        # show pressed keys
        pressed_keys = []
        for key, cooldown_key in self.cooldown_keys.items():
            if cooldown_key.pressed:
                pressed_keys.append(key)
        # TODO
        # arcade.draw_text(f"Pressed keys: {pressed_keys}", SCREEN_WIDTH - 10, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, font_size=20, anchor_x="right")


        # self.actor_group.draw(APP_SCREEN) # TODO: hmm... this doesn't work
        for a in self.actor_group:
            a.draw()

        # self.player.draw_hit_box(arcade.color.BLUE)
        # self.player.draw( self.camera )
        self.player.draw()

        if self.paused:
            pass
            # draw pause screen
            # TODO
            # arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK_OLIVE + (200,))
            # arcade.draw_text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, arcade.color.YELLOW_ROSE, font_size=60, anchor_x="center", anchor_y="center")

        if self.escape_pressed_time is not None:
            time_elapsed = time.time() - self.escape_pressed_time
            if time_elapsed >= HOLD_TO_QUIT_SECONDS:
                self.alive = False
                self.escape_pressed_time = None
            else:
                self.draw_timer_wheel(time_elapsed)



    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.escape_pressed_time = time.time()
                self.paused = True
            elif event.key == pygame.K_p:
                self.paused = not self.paused

            if self.paused:
                return
            
            if event.key == pygame.K_z:
                self.spawn_seek_agent()
            elif event.key == pygame.K_x:
                self.spawn_flee_agent()

            if event.key == pygame.K_SPACE:
                # self.player.fire()
                self.actor_group = pygame.sprite.Group()

            self.handle_cooldown_keys(event.key)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.escape_pressed_time = None
                self.paused = False

            if self.paused:
                return

            for cooldown_key in self.cooldown_keys.values():
                cooldown_key.on_key_release(event.key)



    def draw_timer_wheel(self, time_elapsed):
        center_x = self.window.width // 2
        center_y = self.window.height * 0.5
        radius = 100

        start_angle = 360
        end_angle = 360 - ((HOLD_TO_QUIT_SECONDS - time_elapsed) / HOLD_TO_QUIT_SECONDS) * 360

        # TODO: twine between colors as time elapses
        # arcade.draw_arc_filled(center_x, center_y, radius, radius, arcade.color.WHITE, end_angle, start_angle, 90)
        # arcade.draw_text(f"Hold <ESCAPE> to quit", center_x, center_y - radius, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center", anchor_y="center")
        pygame.draw.arc(APP_SCREEN, Colors.WHITE, (center_x - radius, center_y - radius, radius * 2, radius * 2), start_angle, end_angle, 90)
        font = pygame.font.SysFont(None, 20)
        text = font.render("Hold <ESCAPE> to quit", True, pygame.Color("WHITE_SMOKE"))
        text_rect = text.get_rect(center=(center_x, center_y - radius))
        APP_SCREEN.blit(text, text_rect)




    def handle_cooldown_keys(self, key: int = None):
        # NOTE: these can't be elif becuase this is also run in on_update() and it needs to process every one of these

        if self.cooldown_keys[KEY_UP].run(key=key):
            # self.player.change_speed_cap(y_delta=-1)
            self.player.acceleration.y += -1

        if self.cooldown_keys[KEY_DOWN].run(key=key):
            # self.player.change_speed_cap(y_delta=1)
            self.player.acceleration.y += 1

        if self.cooldown_keys[KEY_LEFT].run(key=key):
            # self.player.change_speed_cap(x_delta=-1)
            self.player.acceleration.x += -1

        if self.cooldown_keys[KEY_RIGHT].run(key=key):
            # self.player.change_speed_cap(x_delta=1)
            self.player.acceleration.x += 1


    def spawn_flee_agent(self): # SHRIMP
        agent = Agent(AgentType.Shrimp)
        agent.target = self.player
        self.actor_group.add(agent)

    def spawn_seek_agent(self): # CRAB
        agent = Agent(AgentType.Crab)
        agent.target = self.player
        self.actor_group.add(agent)

    def spawn_dot_agent(self): # DOT
        agent = Agent(AgentType.Dot)
        agent.target = self.player
        self.actor_group.add(agent)
