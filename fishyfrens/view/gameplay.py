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
from fishyfrens.config import *
from fishyfrens.app import App

from fishyfrens.level import level, create_levels, Storyline
from fishyfrens.audio import audio
from fishyfrens.view.camera import camera, ParallaxBackground

from fishyfrens.actor.agent import Agent, AgentType
from fishyfrens.actor.player import player, create_player


# TODO: move this to a better place
def create_vignette_surface():
    # file_name = 'vdonewhitehuge.png'
    file_name = 'v1cleanhuge.png'
    scale = 2
    surface = pygame.image.load(os.path.join(MY_DIR, 'resources', 'img', 'vignette', file_name)).convert_alpha()
    surface = pygame.transform.scale(surface, (surface.get_width() * scale, surface.get_height() * scale))
    surface.set_colorkey((255, 255, 255))
    return surface

vignette_surface = create_vignette_surface()


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
            KEY_SPACE: CooldownKey(pygame.K_SPACE, 3),
        }

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

        starting_level = App.get_instance().manifest_key_value('starting_level', 0) # TODO: find a way to set
        create_levels(storyline=Storyline.FREN_RESCUE, starting_level=starting_level)
        # TODO : this is a mess, fix the level class
        level().set_level(self, set_level=starting_level)

        audio().play_bg(1)
        self.start_time = time.time()
        # self.last_agent_spawn_time = time.time()
        # self.last_flee_agent_spawn_time = time.time()
        # self.last_seek_agent_spawn_time = time.time()

        self.paused = False
        self.escape_pressed_time = None
        self.alive = True

        if App.get_instance().manifest.get("fastswimmer", False) == True:
            logger.debug("CHEAT ENABLED - FAST SWIMMING MODE!")
            # self.player.top_speed = 60
            player().top_speed = 60
            global PLAYER_ACCELERATION
            PLAYER_ACCELERATION = 1.5

        # camera().target = self.player
        camera().target = player()
        self.actor_group = pygame.sprite.Group()


        for key in self.cooldown_keys.values():
            key.reset()

        # self.level_setup()


    def update(self):
        # if self.player.life <= 0 or self.alive is False:
        if player().life <= 0 or self.alive is False:
            App.get_instance().viewmanager.run_view("results")

        if self.paused:
            return


        # self.actor_group.update(player=self.player)
        self.actor_group.update()

        self.handle_cooldown_keys()
        # self.player.update()
        player().update()

        # if self.level == 1:
        #     self.level1()
        # elif self.level == 2:
        #     self.level2()
        self.level_agent_handler()

        # level functions must handle their own agent generation and collisions
        # self.handle_collisions()

        camera().update() # this should be done last ( now updates parallax background too)







    def draw(self):
        APP_SCREEN.fill( (23, 21, 25) )

        if level().depth_gradient:
            # NOTE: the minimun BG color has be be above zero because lerp_color is hacky and will overshoot
            # bg_color = lerp_color((40, 70, 140), (5, 30, 50), self.player.position.y / camera().playfield_height)
            bg_color = lerp_color((40, 70, 140), (5, 30, 50), camera().target_ratio_y)
        else:
            bg_color = (3, 32, 50)

        pygame.draw.rect(APP_SCREEN, bg_color, (-camera().offset.x, -camera().offset.y, camera().playfield_width, camera().playfield_height))

        # show pressed keys
        pressed_keys = []
        for key, cooldown_key in self.cooldown_keys.items():
            if cooldown_key.pressed:
                pressed_keys.append(key)

        for a in self.actor_group:
            a.draw()

        # self.player.draw()
        player().draw()

        # VIGNETTE
        if level().show_vignette:
            APP_SCREEN.blit(vignette_surface,
                            # (self.player.position.x - camera().offset.x - vignette_surface.get_width() // 2, self.player.position.y - camera().offset.y - vignette_surface.get_height() //2),
                            (player().position.x - camera().offset.x - vignette_surface.get_width() // 2, player().position.y - camera().offset.y - vignette_surface.get_height() //2),
                            special_flags=pygame.BLEND_RGBA_MULT)

        # self.player.draw_life_bar()
        player().draw_life_bar()

        camera().draw_effects()

        self.draw_effects()

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



    def draw_effects(self):
        # """ TODO: look into a damage vignette effect here: https://stackoverflow.com/questions/56333344/how-to-create-a-taken-damage-red-vignette-effect-in-pygame
        # """

        # fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # fade_surface.fill((0, 0, 0, 128))
        # APP_SCREEN.blit(fade_surface, (0, 0))
        # # draw a circle centered on player will full alpha
        # pygame.draw.circle(APP_SCREEN, (0,0,0,0), self.player.position, 100, 100)

        # TODO - toggle extra stats on screen
        # arcade.draw_text(f"Pressed keys: {pressed_keys}", SCREEN_WIDTH - 10, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, font_size=20, anchor_x="right")

        text(APP_SCREEN, f"Score: {self.score}", (SCREEN_WIDTH // 2, 20), font_size=40, color=arcade_color.YELLOW_ORANGE, center=True)

        if debug.DRAW_STATS:
            # fps = f"FPS: {App.get_instance().fps:.0f}"
            fps = f"FPS: {App.get_instance().clock.get_fps():.0f}"
            # speed = math.trunc(self.player.velocity.magnitude())
            # speed = math.ceil(self.player.velocity.magnitude())
            # round speed to nearest whole number
            # speed = round(self.player.velocity.magnitude(), 1)
            speed = round(player().velocity.magnitude(), 1)
            text(APP_SCREEN, f"speed: {speed}", (SCREEN_WIDTH // 2, 60), font_size=20, color=arcade_color.YELLOW_ORANGE, center=True)
            text(APP_SCREEN, fps, (SCREEN_WIDTH // 2, 80), font_size=20, color=arcade_color.YELLOW_ORANGE, center=True)
            text(APP_SCREEN, f"Level: {level().current_level}", (SCREEN_WIDTH // 2, 100), font_size=20, color=arcade_color.PIGGY_PINK, center=True)



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
            elif event.key == pygame.K_EQUALS:
                level().set_level(self, next_level=True)

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
            # self.player.acceleration.y += -PLAYER_ACCELERATION
            player().acceleration.y += -PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_DOWN].run(key=key):
            # self.player.acceleration.y += PLAYER_ACCELERATION
            player().acceleration.y += PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_LEFT].run(key=key):
            # self.player.acceleration.x += -PLAYER_ACCELERATION
            player().acceleration.x += -PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_RIGHT].run(key=key):
            # self.player.acceleration.x += PLAYER_ACCELERATION
            player().acceleration.x += PLAYER_ACCELERATION
        if self.cooldown_keys[KEY_SPACE].run(key=key):
            # self.player.boost()
            player().boost()




    def spawn_krill(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRILL)
        # agent.target = self.player
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)



    def spawn_fren(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FRENFISH)
        # agent.target = self.player
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)



    def spawn_fish(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FISH)
        # agent.target = self.player
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)



    def spawn_kraken(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRAKEN)
        # agent.target = self.player
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.actor_group.add(agent)




    def handle_collisions(self):
        # find all agents within the screen
        agents_within_proximity = pygame.sprite.Group()
        # for agent in self.actor_group:
        #     if agent.position.x - camera().offset.x < 100 \
        #     or agent.position.x - camera().offset.x > SCREEN_WIDTH - 100 \
        #         or agent.position.y - camera().offset.y < 100 \
        #             or agent.position.y - camera().offset.y > SCREEN_HEIGHT - 100:
        # for agent in self.actor_group:
        #     if agent.is_onscreen:
        #         visible_agents.add(agent)

        # TODO play around with these algorithms... set visible_onscreen to false for all agents we aren't calculating to visualise effectiveness

        for agent in self.actor_group:
            # distance from player to agent
            # distance = self.player.position.distance_to(agent.position)
            distance = player().position.distance_to(agent.position)
            if distance < 150: # this doesn't always work... HMMM... fucking arbitrary... # TODO
                agents_within_proximity.add(agent)

        # TODO print important performance metrics here
        # print(f"% of visible agents: {len(visible_agents) / len(self.actor_group)}")
        # logger.debug(f"visible agents: {len(agents_within_proximity)} / fps: {App.get_instance().clock.get_fps():.0f}")

        # collisions = pygame.sprite.spritecollide(self.player, self.actor_group, False, pygame.sprite.collide_mask)
        # collisions = pygame.sprite.spritecollide(self.player, agents_within_proximity, False, pygame.sprite.collide_mask)
        collisions = pygame.sprite.spritecollide(player(), agents_within_proximity, False, pygame.sprite.collide_mask)
        for agent in collisions:
            # agent.dead = True
            if agent.type == AgentType.KRILL:
                audio().dink()
                self.score += 1
                # self.stomach[AgentType.KRILL][agent.subtype] += 1
                self.stomach[AgentType.KRILL] += 1
                # self.player.adjust_life(13) # faster
                player().adjust_life(13) # faster
            elif agent.type == AgentType.FISH:
                audio().dink()
                self.score += 2
                # self.stomach[AgentType.FISH][agent.subtype] += 1
                self.stomach[AgentType.FISH] += 1
                # self.player.adjust_life(5) # more plentiful
                player().adjust_life(5) # more plentiful
            elif agent.type == AgentType.FRENFISH:
                continue
            elif agent.type == AgentType.KRAKEN:
                self.score -= 3
                # self.stomach[AgentType.KRAKEN][agent.subtype] += 1
                self.stomach[AgentType.KRAKEN] += 1
                # audio().oww( self.player.name )
                audio().oww( player().name )
                # self.player.adjust_life(-15)
                player().adjust_life(-15)

            # TODO: let's call a callback in order to do cool things before we destroy the agent.
            self.actor_group.remove(agent)
            del agent

        if self.score > level().LEVEL_SCORE_PROGRESSION[level().current_level]: # TODO: hard, coded... let's make a score list/dict or something
            level().set_level(self, next_level=True)
            # camera().resize() # TODO: not sure if I need this...





#####################################################
    def level_agent_handler(self):
        #####################################################
        #################  LEVEL ONE  #######################
        #####################################################
        if level().current_level == 0:
            if time.time() > level().last_krill_spawn_time + level().agent_spawn_interval:
                level().last_krill_spawn_time = time.time()
                self.spawn_krill()

            if time.time() > level().last_fish_spawn_time + level().agent_spawn_interval * 3: # 3:1 ratio krill to fish
                level().last_fish_spawn_time = time.time()
                self.spawn_fish()
        #####################################################
        #################  LEVEL TWO  #######################
        #####################################################
        elif level().current_level == 1:
            while len(self.actor_group) < level().max_agents:
                random_number = random.uniform(0, 1)

                if random_number < 0.5:
                    self.spawn_krill( level().hide_out_of_sight )
                else:
                    self.spawn_fish( level().hide_out_of_sight )

        #####################################################
        #################  LEVEL THREE  #####################
        #####################################################
        elif level().current_level == 2:
            while len(self.actor_group) < level().max_agents:
                random_number = random.uniform(0, 1)
                if random_number < 15/32:
                    # print("This branch runs with a 7/16 probability.")
                    self.spawn_krill( level().hide_out_of_sight )
                elif random_number < 15/32 + 16/32:
                    # print("This branch runs with a 8/16 (or 1/2) probability.")
                    self.spawn_fish( level().hide_out_of_sight )
                else:
                    # print("This branch runs with a 1/16 probability.")
                    self.spawn_kraken( level().hide_out_of_sight )



        # TODO - all levels have the same collision handler FOR NOW
        self.handle_collisions()


    def safeXY(self):
        # how far away from the edge of the playfield should agents be spawned
        SAFE_BUFFER = 100

        # return a random x,y coordinate that is not within the player's view
        while True: # TODO: this is a bad way to do this... but it works for now
            x = random.randint(SAFE_BUFFER, camera().playfield_width - SAFE_BUFFER)
            y = random.randint(SAFE_BUFFER, camera().playfield_height - SAFE_BUFFER)
            # if self.player.position.distance_to(pygame.Vector2(x, y)) > 200:
            if player().position.distance_to(pygame.Vector2(x, y)) > 200:
                return x, y
