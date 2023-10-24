import pygame

from gamelib.globals import *


def text(surface, text, position, font_name='Arial', font_size=36, color=(255, 255, 255)):
    """
    A helper function to draw text on a Pygame surface.

    :param surface: The Pygame surface to draw on
    :param text: The text to be displayed
    :param position: A tuple (x, y) representing the position to draw the text
    :param font_name: The name of the font to use
    :param font_size: The size of the font
    :param color: The color of the text
    """
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
