import time
import arcade

class FlashText:
    def __init__(self, text, x, y, font_size, color, flash=False, bold=False):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.flash = flash
        self.bold = bold
        self.show_text = True
    
    def draw(self):
        if self.flash:
            alpha = abs((time.time() % 2) - 1)
            color = self.color + (int(alpha * 255),)
        else:
            color = self.color
        arcade.draw_text(self.text, self.x, self.y, color, self.font_size, anchor_x="center", bold=self.bold)

    def update(self, delta_time):
        pass  # Any update logic for the text goes here




class SlideText:
    def __init__(self, text, start_x, start_y, end_x, end_y, font_size, color, slide_duration, mode, bold):
        self.text = text
        self.x = start_x
        self.y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.font_size = font_size
        self.color = color
        self.delta_x = (end_x - start_x) / slide_duration
        self.delta_y = (end_y - start_y) / slide_duration
        self.mode = mode
        self.bold = bold
        self.in_place = False

    def draw(self):
        arcade.draw_text(self.text, self.x, self.y, self.color, self.font_size, anchor_x="center", bold=self.bold)

    def update(self, delta_time):
        if not self.in_place:
            self.x += self.delta_x * delta_time
            self.y += self.delta_y * delta_time
            
            # Check if we've reached or exceeded the end point, and adjust if necessary.
            if (self.delta_x > 0 and self.x >= self.end_x) or (self.delta_x < 0 and self.x <= self.end_x):
                self.x = self.end_x
                
            if (self.delta_y > 0 and self.y >= self.end_y) or (self.delta_y < 0 and self.y <= self.end_y):
                self.y = self.end_y

            # Mark as in place if we've reached both end x and y positions
            if self.x == self.end_x and self.y == self.end_y:
                self.in_place = True
