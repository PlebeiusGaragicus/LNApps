import os
import random

import pygame

# from gamelib.globals import MY_DIR
from grub.app import MY_DIR


class SoundMaster:
    def __init__(self):
        self.background_music = pygame.mixer.music.load( os.path.join(MY_DIR, 'resources', 'sounds', 'epic-background.wav') )
        # pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

        self.dink_effect = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'dink_short.wav') )
        self.oww_effect1 = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'oww1.wav') )
        self.oww_effect2 = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'oww2.wav') )
        self.oww_effect3 = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'oww3.wav') )

        self.you_died_effect = pygame.mixer.Sound( os.path.join(MY_DIR, 'resources', 'sounds', 'you_died.wav') )


    def dink(self):
        self.dink_effect.play()
    
    def oww(self):
        # 50 percent chance:
        r = random.randint(1, 3)
        if r == 1:
            self.oww_effect1.play()
        elif r == 2:
            self.oww_effect2.play()
        elif r == 3:
            self.oww_effect3.play()
    
    def you_died(self):
        self.you_died_effect.play()


AUDIO = SoundMaster()
