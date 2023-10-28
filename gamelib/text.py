import pygame

from gamelib.globals import *


def text(surface: pygame.Surface, text, position, font_size=36, color=(255, 255, 255), center=False, font_name='Arial'):
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
    if center:
        text_rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, position)

#TODO can I do bold please?
