# file imports
from pygameCarcassonneDir.pygameSettings import BLACK, WHITE

# packages
import pygame

class Label():
    def __init__(self, text, X=0, Y=0, background=None, foreground=BLACK, font_name=None, font_size=25, isCircle=False):
        self.text = text
        self.X = X
        self.Y = Y
        self.background = background
        self.foreground = foreground
        
        # font
        self.font = pygame.font.Font(font_name, font_size)
        
        # text
        self.text_surface = self.font.render(self.text, True, self.foreground, self.background)
        self.text_rect = self.text_surface.get_rect(center=(X,Y))
        
    def draw(self, GAME_DISPLAY):
        GAME_DISPLAY.blit(self.text_surface, self.text_rect)
        
    def update(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.foreground)
        