import time
import logging
logger = logging.getLogger()

import arcade

from gamelib.menuaction import MenuAction


from grub.app import GAME_WINDOW
from grub.config import AFK_TIMEOUT



class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.last_input = time.time()
        self.afk_timeout = AFK_TIMEOUT
        self.menu_actions = []

        self.selected_menu_item = 0

        self.menu_actions.append( MenuAction("Start Game", self.start_game) )
        self.menu_actions.append( MenuAction("Power-up", None) )
        self.menu_actions.append( MenuAction("Load Game", None) )
        self.menu_actions.append( MenuAction("Save Game", None) )
        self.menu_actions.append( MenuAction("Options", None) )
        self.menu_actions.append( MenuAction("Exit", arcade.close_window) )



    def start_game(self):
        from grub.view.gameplay import GameplayView
        next_view = GameplayView()
        self.window.show_view(next_view)



    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)



    def on_update(self, delta_time):
        if self.is_user_afk():
            arcade.exit() # TODO - maybe show a "you're afk" screen instead of just exiting the game? (like a screensaver or sample gameplay)



    def on_draw(self):
        arcade.start_render()

        x = GAME_WINDOW.width * 0.1
        y = GAME_WINDOW.height // 2
        for i, menu_item in enumerate(self.menu_actions):
            if i == self.selected_menu_item:
                color = arcade.color.YELLOW
                menu_item_size = 40
                arcade.draw_text(">", x - 40, y - i * 50, color, font_size=40, anchor_x="left")
            else:
                menu_item_size = 30
                color = arcade.color.AIR_FORCE_BLUE

            arcade.draw_text(menu_item.name, x, y - i * 50, color, font_size=menu_item_size, anchor_x="left")


    def on_key_press(self, symbol: int, modifiers: int):
        self.reset_afk_timer()

        if symbol == arcade.key.UP:
            if self.selected_menu_item > 0:
                self.selected_menu_item -= 1

        elif symbol == arcade.key.DOWN:
            if self.selected_menu_item < len(self.menu_actions) - 1:
                self.selected_menu_item += 1

        elif symbol == arcade.key.ENTER:
            logger.info("enter")
            # self.menu_actions[self.selected_menu_item].action()
            self.menu_actions[self.selected_menu_item].execute()

        elif symbol == arcade.key.ESCAPE:
            logger.info("escape")
            arcade.exit()


    def is_user_afk(self) -> bool:
        # self-destruct in ten seconds if no input (user is AFK)
        if self.afk_timeout > 0 and \
            time.time() > self.last_input + self.afk_timeout:
                logger.warning("AFK timeout reached, exiting game - user is AFK!")
                return True


    def reset_afk_timer(self):
        self.last_input = time.time()
