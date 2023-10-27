import time
import random
import logging
logger = logging.getLogger()

import pygame

from gamelib.colors import Colors, arcade_color
from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from gamelib.cooldown_keys import CooldownKey, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from gamelib.viewstate import View
from gamelib.text import text

from fishyfrens import debug
from fishyfrens.config import *
from fishyfrens.app import App
from fishyfrens.actor.player import Player
from fishyfrens.actor.agent import Agent, AgentType
from fishyfrens.view.camera import CAMERA
from fishyfrens.audio import AUDIO



class GameplayView(View):
    def __init__(self):
        super().__init__()

        # NOTE: put static things here that don't need to be reset when the game is reset
        self.cooldown_keys: dict[CooldownKey] = {
            # TODO - allow multiple keys or 'input methods' for each action
            # cross playform baby!!!
            # KEY_UP: CooldownKey(pygame.K_w, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_DOWN: CooldownKey(pygame.K_s, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_LEFT: CooldownKey(pygame.K_a, COOLDOWN_DIRECTIONAL_SECONDS),
            # KEY_RIGHT: CooldownKey(pygame.K_d, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_UP: CooldownKey(pygame.K_UP, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_DOWN: CooldownKey(pygame.K_DOWN, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_LEFT: CooldownKey(pygame.K_LEFT, COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_RIGHT: CooldownKey(pygame.K_RIGHT, COOLDOWN_DIRECTIONAL_SECONDS),
        }

        self.score = 0
        self.level = App.get_instance().manifest_key_value('starting_level', 1)


    def setup(self):
        # NOTE: This is called when the view is switched to, so it's a good place to reset things
        # we can also use this to setup the view the first time it's run instead of in __init__()

        self.start_time = time.time()
        self.last_agent_spawn_time = time.time()
        self.last_flee_agent_spawn_time = time.time()
        self.last_seek_agent_spawn_time = time.time()

        self.paused = False
        self.escape_pressed_time = None
        self.alive = True

        self.player: Player = Player()
        CAMERA.target = self.player
        self.actor_group = pygame.sprite.Group()

        for key in self.cooldown_keys.values():
            key.reset()


    def update(self):
        if self.player.life <= 0 or self.alive is False:
            App.get_instance().viewmanager.run_view("results")

        if self.paused:
            return


        # self.actor_group.update(player=self.player)
        self.actor_group.update()


        self.handle_cooldown_keys()
        self.player.update()


        if self.level == 1:
            self.level1()
        elif self.level == 2:
            self.level2()

        # self.handle_collisions() # level functions must handle their own agent generation and collisions

        CAMERA.update() # this should be done last




    def draw(self):
        APP_SCREEN.fill( (3, 32, 50) ) # (3, 192, 60) DARK_PASTEL_GREEN

        self.draw_playfield_boarder()

        # show pressed keys
        pressed_keys = []
        for key, cooldown_key in self.cooldown_keys.items():
            if cooldown_key.pressed:
                pressed_keys.append(key)

        # TODO - toggle extra stats on screen
        # arcade.draw_text(f"Pressed keys: {pressed_keys}", SCREEN_WIDTH - 10, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, font_size=20, anchor_x="right")

        for a in self.actor_group:
            a.draw()

        self.player.draw()
        text(APP_SCREEN, f"Score: {self.score}", (SCREEN_WIDTH // 2, 20), font_size=40, color=arcade_color.YELLOW_ORANGE, center=True)

        if self.paused:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 128))
            APP_SCREEN.blit(fade_surface, (0, 0))
            text(APP_SCREEN, "PAUSED", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3), color=arcade_color.YELLOW_ROSE, font_size=100, center=True)

        if self.escape_pressed_time is not None:
            time_elapsed = time.time() - self.escape_pressed_time
            if time_elapsed >= HOLD_TO_QUIT_SECONDS:
                # self.alive = False
                # self.escape_pressed_time = None
                App.get_instance().viewmanager.run_view("main_menu")
            else:
                self.draw_timer_wheel(time_elapsed)


    def draw_playfield_boarder(self):
        # draw a line from 0,0 to 0, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        pygame.draw.line(APP_SCREEN, Colors.MAGENTA, _start, _end, BORDER_WIDTH)

        # draw a line from 0,0 to screen width, 0 using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        pygame.draw.line(APP_SCREEN, Colors.MAGENTA, _start, _end, BORDER_WIDTH)

        # draw a line from screen width, 0 to screen width, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        pygame.draw.line(APP_SCREEN, Colors.MAGENTA, _start, _end, BORDER_WIDTH)

        # draw a line from 0, screen height to screen width, screen height using pygame
        _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        pygame.draw.line(APP_SCREEN, Colors.MAGENTA, _start, _end, BORDER_WIDTH)



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
            elif event.key == pygame.K_m:
                # global DRAW_MASKS
                debug.DRAW_MASKS = not debug.DRAW_MASKS
            elif event.key == pygame.K_v:
                # global DRAW_VECTORS
                debug.DRAW_VECTORS = not debug.DRAW_VECTORS
            elif event.key == pygame.K_r:
                # global DRAW_RECTS
                debug.DRAW_RECTS = not debug.DRAW_RECTS

            if event.key == pygame.K_SPACE:
                # self.player.fire()
                self.actor_group = pygame.sprite.Group()

            self.handle_cooldown_keys(event.key)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.escape_pressed_time = None
                self.paused = False

            if self.paused:
                return

            for cooldown_key in self.cooldown_keys.values():
                cooldown_key.on_key_release(event.key)



    def draw_timer_wheel(self, time_elapsed):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT * 0.5
        radius = 100

        start_angle = 360
        end_angle = 360 - ((HOLD_TO_QUIT_SECONDS - time_elapsed) / HOLD_TO_QUIT_SECONDS) * 360

        # TODO: twine between colors as time elapses
        # arcade.draw_arc_filled(center_x, center_y, radius, radius, arcade.color.WHITE, end_angle, start_angle, 90)
        # arcade.draw_text(f"Hold <ESCAPE> to quit", center_x, center_y - radius, arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center", anchor_y="center")
        # pygame.draw.arc(APP_SCREEN, Colors.WHITE, (center_x - radius, center_y - radius, radius * 2, radius * 2), start_angle, end_angle, 90)
        font = pygame.font.SysFont(None, 70)
        text = font.render("Hold <ESCAPE> to quit", True, arcade_color.WHITE_SMOKE)
        text_rect = text.get_rect(center=(center_x, center_y - radius))
        APP_SCREEN.blit(text, text_rect)
        pygame.draw.arc(APP_SCREEN, Colors.RED, (center_x - radius, center_y - radius, radius * 2, radius * 2), start_angle, end_angle, 90)



    def handle_cooldown_keys(self, key: int = None):
        # NOTE: these can't be elif becuase this is also run in on_update() and it needs to process every one of these

        if self.cooldown_keys[KEY_UP].run(key=key):
            self.player.acceleration.y += -PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_DOWN].run(key=key):
            self.player.acceleration.y += PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_LEFT].run(key=key):
            self.player.acceleration.x += -PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_RIGHT].run(key=key):
            self.player.acceleration.x += PLAYER_ACCELERATION



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


    def handle_collisions(self):
        collisions = pygame.sprite.spritecollide(self.player, self.actor_group, False, pygame.sprite.collide_mask)
        for agent in collisions:
            # logger.info("Player collided with agent")
            # agent.dead = True
            if agent.type == AgentType.Dot:
                AUDIO.dink()
                self.score += 1
                self.player.adjust_life(6)
            elif agent.type == AgentType.Shrimp:
                AUDIO.dink()
                self.score += 2
                self.player.adjust_life(14)
            elif agent.type == AgentType.Crab:
                self.score -= 3
                AUDIO.oww()
                self.player.adjust_life(-10)

            # TODO: let's call a callback in order to do cool things before we destroy the agent.
            self.actor_group.remove(agent)
            del agent


    def level1(self):
        # LIFE_SUCK_RATE = 1
        # AGENT_SPAWN_INTERVAL_SECONDS = 0.05
        # MAX_AGENTS = 1200
        while len(self.actor_group) < MAX_AGENTS:
            if random.randint(1, 100) <= 5: # 5% chance:
                self.spawn_seek_agent()
            else:
                if random.randint(1, 100) <= 50: # 50% chance:
                    self.spawn_flee_agent()
                else:
                    self.spawn_dot_agent()
        

        self.handle_collisions()


    def level2(self):
        global AGENT_SPAWN_INTERVAL_SECONDS
        AGENT_SPAWN_INTERVAL_SECONDS = 1.4
        global LIFE_SUCK_RATE
        LIFE_SUCK_RATE = 5
        global MAX_AGENTS
        MAX_AGENTS = 2000

        if time.time() > self.last_flee_agent_spawn_time + AGENT_SPAWN_INTERVAL_SECONDS:
            self.last_flee_agent_spawn_time = time.time()
            self.spawn_flee_agent()

        if time.time() > self.last_seek_agent_spawn_time + AGENT_SPAWN_INTERVAL_SECONDS * 10:
            self.last_seek_agent_spawn_time = time.time()
            self.spawn_seek_agent()

        self.handle_collisions()
