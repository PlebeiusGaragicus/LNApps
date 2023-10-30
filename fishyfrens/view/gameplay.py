import os
import time
import random
# import math
import logging
logger = logging.getLogger()

import pygame

from gamelib.globals import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
# from gamelib import globals
from gamelib.colors import Colors, arcade_color
from gamelib.utils import lerp_color


# from gamelib.cooldown_keys import CooldownKey, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from gamelib.cooldown_keys import *
from gamelib.viewstate import View
from gamelib.text import text

from fishyfrens import debug
# from fishyfrens.config import *
from fishyfrens import config
from fishyfrens.app import App, MY_DIR

from fishyfrens.audio import AUDIO
from fishyfrens.level import MAX_LEVELS, LEVEL_SCORE_PROGRESSION
# from fishyfrens.view.camera import CAMERA
from fishyfrens.globals import CAMERA, LEVEL
from fishyfrens.parallax import ParallaxBackground

from fishyfrens.actor.agent import Agent, AgentType
from fishyfrens.actor.player import Player



# TODO: move this to a better place
def create_vignette_surface(radius, color=(0, 0, 0)):
    surface = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'vignette', 'vdonewhitehuge.png')).convert_alpha()
    # surface = pygame.transform.scale(surface, (radius, radius))
    surface.set_colorkey((255, 255, 255))
    return surface

vignette_surface = create_vignette_surface(1500, (25, 90, 90))


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
            KEY_UP: CooldownKey(pygame.K_UP, config.COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_DOWN: CooldownKey(pygame.K_DOWN, config.COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_LEFT: CooldownKey(pygame.K_LEFT, config.COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_RIGHT: CooldownKey(pygame.K_RIGHT, config.COOLDOWN_DIRECTIONAL_SECONDS),
            KEY_SPACE: CooldownKey(pygame.K_SPACE, 3),
        }


        # self.show_vignette = None # must be set in level_setup()
        # self.level = App.get_instance().manifest_key_value('starting_level', 0) # TODO: find a way to set
        self.score = 0
        # TODO: good enough for now, but please refactor this
        self.stomach = {
            AgentType.KRILL: 0,
            AgentType.FISH: 0,
            AgentType.FRENFISH: 0,
            AgentType.KRAKEN: 0,
        }


    def setup(self):
        # NOTE: This is called when the view is switched to, so it's a good place to reset things
        # we can also use this to setup the view the first time it's run instead of in __init__()

        AUDIO.play_bg(1)
        self.start_time = time.time()
        self.last_agent_spawn_time = time.time()
        self.last_flee_agent_spawn_time = time.time()
        self.last_seek_agent_spawn_time = time.time()

        self.paused = False
        self.escape_pressed_time = None
        self.alive = True

        # self.player: Player = Player(name="myca")
        self.player: Player = Player(name="charlie")

        if App.get_instance().manifest.get("fastswimmer", False) == True:
            logger.debug("CHEAT ENABLED - FAST SWIMMING MODE!")
            self.player.top_speed = 60
            global PLAYER_ACCELERATION
            PLAYER_ACCELERATION = 1.5

        CAMERA.target = self.player
        self.actor_group = pygame.sprite.Group()

        # TODO: Performance is not acceptable on arcade
        # self.parallax_background = ParallaxBackground(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, 0.5)
        # self.parallax_background = ParallaxBackground()

        for key in self.cooldown_keys.values():
            key.reset()

        # self.level_setup()


    def update(self):
        if self.player.life <= 0 or self.alive is False:
            App.get_instance().viewmanager.run_view("results")

        if self.paused:
            return


        # self.actor_group.update(player=self.player)
        self.actor_group.update()

        self.handle_cooldown_keys()
        self.player.update()

        # if self.level == 1:
        #     self.level1()
        # elif self.level == 2:
        #     self.level2()
        self.level_agent_handler()

        # self.handle_collisions() # level functions must handle their own agent generation and collisions

        CAMERA.update() # this should be done last

        # self.parallax_background.update()






    def draw(self):
        # APP_SCREEN.fill( (3, 32, 50) )

        bg_color = lerp_color((40, 70, 140), (0, 30, 50), self.player.position.y / config.PLAYFIELD_HEIGHT)
        APP_SCREEN.fill( bg_color ) # (3, 192, 60) DARK_PASTEL_GREEN

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

        # VIGNETTE
        if LEVEL.show_vignette:
            APP_SCREEN.blit(vignette_surface, (self.player.position.x - CAMERA.offset.x - vignette_surface.get_width() // 2, self.player.position.y - CAMERA.offset.y - vignette_surface.get_height() //2), special_flags=pygame.BLEND_RGBA_MULT)

        self.player.draw_life_bar()
        text(APP_SCREEN, f"Score: {self.score}", (SCREEN_WIDTH // 2, 20), font_size=40, color=arcade_color.YELLOW_ORANGE, center=True)

        # self.parallax_background.draw()

        # vignette_surface = create_vignette_surface(300)


        # self.draw_effects()

        if debug.DRAW_STATS:
            # fps = f"FPS: {App.get_instance().fps:.0f}"
            fps = f"FPS: {App.get_instance().clock.get_fps():.0f}"
            # speed = math.trunc(self.player.velocity.magnitude())
            # speed = math.ceil(self.player.velocity.magnitude())
            # round speed to nearest whole number
            speed = round(self.player.velocity.magnitude(), 1)
            text(APP_SCREEN, f"speed: {speed}", (SCREEN_WIDTH // 2, 60), font_size=20, color=arcade_color.YELLOW_ORANGE, center=True)
            text(APP_SCREEN, fps, (SCREEN_WIDTH // 2, 80), font_size=20, color=arcade_color.YELLOW_ORANGE, center=True)
            text(APP_SCREEN, f"Level: {LEVEL.current_level}", (SCREEN_WIDTH // 2, 100), font_size=20, color=arcade_color.PIGGY_PINK, center=True)

        if self.paused:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 128))
            APP_SCREEN.blit(fade_surface, (0, 0))
            text(APP_SCREEN, "PAUSED", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3), color=arcade_color.YELLOW_ROSE, font_size=100, center=True)

        if self.escape_pressed_time is not None:
            time_elapsed = time.time() - self.escape_pressed_time
            if time_elapsed >= config.HOLD_TO_QUIT_SECONDS:
                # self.alive = False
                # self.escape_pressed_time = None
                App.get_instance().viewmanager.run_view("main_menu")
            else:
                self.draw_timer_wheel(time_elapsed)

    def draw_effects(self):
        """ TODO: look into a damage vignette effect here: https://stackoverflow.com/questions/56333344/how-to-create-a-taken-damage-red-vignette-effect-in-pygame
        """

        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, 128))
        APP_SCREEN.blit(fade_surface, (0, 0))
        # draw a circle centered on player will full alpha
        pygame.draw.circle(APP_SCREEN, (0,0,0,0), self.player.position, 100, 100)



    def draw_playfield_boarder(self):
        # draw a line from 0,0 to 0, screen height using pygame
        # LEFT BOUNDARY
        # _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        # _end = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        # pygame.draw.line(APP_SCREEN, arcade_color.COOL_BLACK, _start, _end, BORDER_WIDTH)
        pygame.draw.rect(APP_SCREEN, arcade_color.BLACK, (0, 0, -int(CAMERA.offset.x), SCREEN_HEIGHT), int(-CAMERA.offset.x))

        # draw a line from 0,0 to screen width, 0 using pygame
        # TOP BOUNDARY
        # _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y)
        # _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        # pygame.draw.line(APP_SCREEN, arcade_color.COOL_BLACK, _start, _end, BORDER_WIDTH)
        pygame.draw.rect(APP_SCREEN, arcade_color.BLACK, (-CAMERA.offset.x, 0, CAMERA.offset.x + SCREEN_WIDTH, -int(CAMERA.offset.y)), int(-CAMERA.offset.y))

        # draw a line from screen width, 0 to screen width, screen height using pygame
        # RIGHT BOUNDARY
        # _start = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y)
        # _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        # pygame.draw.line(APP_SCREEN, arcade_color.COOL_BLACK, _start, _end, BORDER_WIDTH)
        pygame.draw.rect(APP_SCREEN, arcade_color.RED, (-CAMERA.offset.x + config.PLAYFIELD_WIDTH, 0, -CAMERA.offset.x + config.PLAYFIELD_WIDTH, SCREEN_HEIGHT), CAMERA.camera_overpan_x)

        # draw a line from 0, screen height to screen width, screen height using pygame
        # BOTTOM BOUNDARY
        # _start = pygame.Vector2(-CAMERA.offset.x, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        # _end = pygame.Vector2(-CAMERA.offset.x + PLAYFIELD_WIDTH, -CAMERA.offset.y + PLAYFIELD_HEIGHT)
        # pygame.draw.line(APP_SCREEN, arcade_color.COOL_BLACK, _start, _end, BORDER_WIDTH)
        # draw a rect from 0,0 to screen width, screen height using pygame
        # TODO: these numbers aren't right... but it works for now (it's overdrawing off the screen)
        pygame.draw.rect(APP_SCREEN, arcade_color.BLACK, (-CAMERA.offset.x, -CAMERA.offset.y + config.PLAYFIELD_HEIGHT, CAMERA.offset.x + SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_WIDTH)



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.escape_pressed_time = time.time()
                self.paused = True
            elif event.key == pygame.K_p:
                self.paused = not self.paused

            if self.paused:
                return

            # speed bost! # NOTE: now a cooldown key
            # if event.key == pygame.K_SPACE:
            #     #TODO this makes the player jump too rapidly
            #     # self.player.velocity += self.player.velocity * 0.001
            #     # self.player.acceleration *= 2
            #     self.player.boost()
            #     logger.debug("BOOST!")


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
            elif event.key == pygame.K_b:
                debug.DRAW_STATS = not debug.DRAW_STATS
            elif event.key == pygame.K_k:
                self.player.life = 0 # TODO: call player.kill?
            elif event.key == pygame.K_RIGHTBRACKET:
                config.PLAYFIELD_WIDTH += 100
                config.PLAYFIELD_HEIGHT += 100
            elif event.key == pygame.K_LEFTBRACKET:
                config.PLAYFIELD_WIDTH -= 100
                config.PLAYFIELD_HEIGHT -= 100

            if event.key == pygame.K_l: # kill all agents
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
        end_angle = 360 - ((config.HOLD_TO_QUIT_SECONDS - time_elapsed) / config.HOLD_TO_QUIT_SECONDS) * 360

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
        if self.cooldown_keys[KEY_SPACE].run(key=key):
            self.player.boost()




    def spawn_krill(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRILL)
        agent.target = self.player
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)


    def spawn_fren(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FRENFISH)
        agent.target = self.player
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)


    def spawn_fish(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FISH)
        agent.target = self.player
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)


    def spawn_kraken(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRAKEN)
        agent.target = self.player
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)



    def handle_collisions(self):
        # find all agents within the screen
        agents_within_proximity = pygame.sprite.Group()
        # for agent in self.actor_group:
        #     if agent.position.x - CAMERA.offset.x < 100 \
        #     or agent.position.x - CAMERA.offset.x > SCREEN_WIDTH - 100 \
        #         or agent.position.y - CAMERA.offset.y < 100 \
        #             or agent.position.y - CAMERA.offset.y > SCREEN_HEIGHT - 100:
        # for agent in self.actor_group:
        #     if agent.is_onscreen:
        #         visible_agents.add(agent)

        # TODO play around with these algorithms... set visible_onscreen to false for all agents we aren't calculating to visualise effectiveness

        for agent in self.actor_group:
            # distance from player to agent
            distance = self.player.position.distance_to(agent.position)
            if distance < 150: # this doesn't always work... HMMM... fucking arbitrary... # TODO
                agents_within_proximity.add(agent)

        # TODO print important performance metrics here
        # print(f"% of visible agents: {len(visible_agents) / len(self.actor_group)}")
        # logger.debug(f"visible agents: {len(agents_within_proximity)} / fps: {App.get_instance().clock.get_fps():.0f}")

        # collisions = pygame.sprite.spritecollide(self.player, self.actor_group, False, pygame.sprite.collide_mask)
        collisions = pygame.sprite.spritecollide(self.player, agents_within_proximity, False, pygame.sprite.collide_mask)
        for agent in collisions:
            # agent.dead = True
            if agent.type == AgentType.KRILL:
                AUDIO.dink()
                self.score += 1
                # self.stomach[AgentType.KRILL][agent.subtype] += 1
                self.stomach[AgentType.KRILL] += 1
                self.player.adjust_life(13) # faster
            elif agent.type == AgentType.FISH:
                AUDIO.dink()
                self.score += 2
                # self.stomach[AgentType.FISH][agent.subtype] += 1
                self.stomach[AgentType.FISH] += 1
                self.player.adjust_life(5) # more plentiful
            elif agent.type == AgentType.FRENFISH:
                continue
            elif agent.type == AgentType.KRAKEN:
                self.score -= 3
                # self.stomach[AgentType.KRAKEN][agent.subtype] += 1
                self.stomach[AgentType.KRAKEN] += 1
                AUDIO.oww( self.player.name )
                self.player.adjust_life(-15)

            # TODO: let's call a callback in order to do cool things before we destroy the agent.
            self.actor_group.remove(agent)
            del agent

        if self.score > LEVEL_SCORE_PROGRESSION[LEVEL.current_level]: # TODO: hard, coded... let's make a score list/dict or something
            LEVEL.next_level(self)
            CAMERA.resize()


    # def next_level(self):
    #     self.level += 1
    #     logger.debug(f"level: {self.level}")

    #     if self.level > MAX_LEVELS:
    #         raise NotImplementedError("YOU WIN THE GAME!!!")
    #     else:
    #         self.level_setup()


    # def level_setup(self):
    #     # NOTE: level zero is the first level!
    #     if self.level == 0:
    #         # TODO: add a marquee to the queue.  This way we can explain gameplay/level to player
    #         # TODO: trigger a "yay sound effect"
    #         self.show_vignette = False
    #         global LIFE_SUCK_RATE
    #         LIFE_SUCK_RATE = 0
    #         global AGENT_SPAWN_INTERVAL_SECONDS
    #         # global MAX_AGENTS
    #         # MAX_AGENTS = 1200
    #         self.hide_out_of_sight = False
    #     elif self.level == 1:
    #         # self.show_vignette = True
    #         self.show_vignette = False
    #         self.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

    #         # TODO: CHANGE THE SIZE OF THE PLAYFIELD... EVERYTHING!!

    #         global AGENT_SPAWN_INTERVAL_SECONDS
    #         AGENT_SPAWN_INTERVAL_SECONDS = 1.4
    #         global LIFE_SUCK_RATE
    #         LIFE_SUCK_RATE = 5
    #         global MAX_AGENTS
    #         MAX_AGENTS = 2000
    #     else:
    #         raise NotImplementedError(f"Level {self.level} not implemented")



#####################################################
    def level_agent_handler(self):
        #####################################################
        #################  LEVEL ONE  #######################
        #####################################################
        if LEVEL.current_level == 0:
            while len(self.actor_group) < LEVEL.max_agents:
                random_number = random.uniform(0, 1)
                if random_number < 15/32:
                    # print("This branch runs with a 7/16 probability.")
                    self.spawn_krill( LEVEL.hide_out_of_sight )
                elif random_number < 15/32 + 16/32:
                    # print("This branch runs with a 8/16 (or 1/2) probability.")
                    self.spawn_fish( LEVEL.hide_out_of_sight )
                else:
                    # print("This branch runs with a 1/16 probability.")
                    self.spawn_kraken( LEVEL.hide_out_of_sight )
        #####################################################
        #################  LEVEL TWO  #######################
        #####################################################
        elif LEVEL.current_level == 1:
            if time.time() > LEVEL.last_krill_spawn_time + LEVEL.agent_spawn_interval:
                LEVEL.last_krill_spawn_time = time.time()
                self.spawn_krill()

            if time.time() > LEVEL.last_fish_spawn_time + LEVEL.agent_spawn_interval * 3: # 3:1 ratio krill to fish
                LEVEL.last_fish_spawn_time = time.time()
                self.spawn_fish()



        # TODO - all levels have the same collision handler FOR NOW
        self.handle_collisions()
