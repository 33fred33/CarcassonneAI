import pygame

# pygame parameters

# colours
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

LIGHTGREEN = (0, 255, 0)
DARK_GREEN = (0,140,0)
COFFEEBROWN =((200,190,140))
BROWN = (92, 64, 51)

# game grid
GRID = [21,17] 
GRID_SIZE = 40
GRID_WINDOW_WIDTH = GRID[0]*GRID_SIZE
GRID_WINDOW_HEIGHT = GRID[1]*GRID_SIZE
GRID_BORDER = 80

# meeple size
MEEPLE_SIZE = 30

# menu width
MENU_WIDTH = 400

# window heigth
WINDOW_HEIGHT = GRID_WINDOW_HEIGHT
WINDOW_WIDTH =  GRID_WINDOW_WIDTH + MENU_WIDTH

# tile size (width=height)
TILE_WIDTH = 104

# meeple Info
MEEPLE_LABEL_X = 40
MEEPLE_LABEL_Y = 50
MEEPLE_LABEL_SHIFT_X = 100
MEEPLE_LABEL_SHIFT_Y = 25

# meeples
MEEPLE_CHOICE_HIGHLIGHT = RED

# font sizes
FONT_MEEPLE_IMAGE = 40
FONT_MEEPLE_MENU = 25


class displayScreen:
    def __init__(self, Grid, Grid_Size, Grid_border, Menu_Width, Meeple_Size):
        self.Grid = Grid
        self.Grid_Size = Grid_Size
        self.Grid_border = Grid_border
        self.Menu_Width = Menu_Width
        self.Meeple_Size = Meeple_Size
        
        # grid size
        self.Grid_Window_Width = Grid[0]*Grid_Size
        self.Grid_Window_Height = Grid[1]*Grid_Size
        
        # add grid border
        self.Total_Grid_Width = self.Grid_Window_Width + self.Grid_border
        self.Total_Grid_Height = self.Grid_Window_Height + self.Grid_border + 20
        
        # total height and width with border
        self.Window_Height = self.Total_Grid_Height
        self.Window_Width =  self.Total_Grid_Width + self.Menu_Width
    
        # display
        self.pygameDisplay = pygame.display.set_mode((self.Window_Width, self.Window_Height))
        
        
        
        
        
        
        
        
