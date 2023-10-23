import time
import logging
logger = logging.getLogger()

import arcade

from gamelib.menuaction import MenuAction
from grub.view.gameplay import GameplayView

from grub.app import GAME_WINDOW
from grub.config import AFK_TIMEOUT


class ResultsView( arcade.View ):
    def __init__(self, gameplay_view: arcade.View):
        super().__init__()
        self.afk_timeout = AFK_TIMEOUT # if None, then no timeout
        self.last_input = time.time()

        self.selected_menu_item = 0
        self.menu_actions = []

        self.menu_actions.append( MenuAction("Revive ($)", self.revive) )
        self.menu_actions.append( MenuAction("Give up", self.main_menu) )

        self.gameplay_view: GameplayView = gameplay_view


    def revive(self):
        logger.info("reviving player...!")
        # self.gameplay_view.player.alive = True
        # self.gameplay_view.player.life = 100
        self.gameplay_view.revive()
        self.window.show_view(self.gameplay_view)

    def main_menu(self):
        from grub.view.menu import MenuView
        next_view = MenuView()
        self.window.show_view(next_view)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)


    def on_update(self, delta_time):
        if self.afk_timeout is not None:    
            if time.time() > self.last_input + self.afk_timeout: # self-destruct in ten seconds if no input (user is AFK)
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                self.main_menu()



    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("GAME OVER", GAME_WINDOW.width // 2, GAME_WINDOW.height * 0.8, arcade.color.RED, font_size=90, anchor_x="center", bold=True)

        x = GAME_WINDOW.width * 0.1
        y = GAME_WINDOW.height // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade.color.YELLOW
                arcade.draw_text(">", x - 30, y - i * 50, color, font_size=30, anchor_x="left")
            else:
                color = arcade.color.AIR_FORCE_BLUE
            # TODO - go for a monospaced font here
            arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=30, anchor_x="left", font_name="/Users/myca/arcade-apps/template/resources/Andale Mono.ttf")


    def on_key_press(self, symbol: int, modifiers: int):
        self.last_input = time.time()

        if symbol == arcade.key.UP:
            if self.selected_menu_item > 0:
                self.selected_menu_item -= 1
        elif symbol == arcade.key.DOWN:
            if self.selected_menu_item < len(self.menu_actions) - 1:
                self.selected_menu_item += 1

        elif symbol == arcade.key.ENTER:
            self.menu_actions[self.selected_menu_item].action()

        elif symbol == arcade.key.ESCAPE:
            self.main_menu()
