# file imports
from Carcassonne_Game.Tile import Tile, showImage

from pygameCarcassonneDir.pygameSettings import MEEPLE_LABEL_X, MEEPLE_LABEL_Y, MEEPLE_LABEL_SHIFT_X, MEEPLE_LABEL_SHIFT_Y
from pygameCarcassonneDir.pygameSettings import GRID_WINDOW_WIDTH, MENU_WIDTH, BLUE, WHITE, RED, GREEN, COFFEEBROWN, BROWN, MEEPLE_CHOICE_HIGHLIGHT
from pygameCarcassonneDir.pygameSettings import FONT_MEEPLE_IMAGE, FONT_MEEPLE_MENU, BLACK

from pygameCarcassonneDir.pygameFunctions import placeColourTile, get_clicked_X, get_clicked_Y, meepleCoordinates
from pygameCarcassonneDir.pygameLabel import Label


# packages
import pygame
import cv2

X_DEPTH = 20
Y_DEPTH = 40
WIDTH = HEIGHT = 104*2  # image scaled x2

XSHIFT = FONT_MEEPLE_IMAGE//4
YSHIFT = FONT_MEEPLE_IMAGE//2

ROTATE_DICT = {
        90:0,
        180:1,
        270:2
        }

MEEPLE_LOCATION_DICT_SCALED = {
    (0,1): [X_DEPTH - XSHIFT, HEIGHT//2 - YSHIFT],
    (0,2): [WIDTH//4 -XSHIFT, HEIGHT - Y_DEPTH - YSHIFT],
    (1,1): [WIDTH//2 - XSHIFT, Y_DEPTH - YSHIFT],
    (1,2): [WIDTH//4- XSHIFT, Y_DEPTH-YSHIFT],
    (2,1): [WIDTH - X_DEPTH - XSHIFT, HEIGHT//2 - YSHIFT],
    (2,2): [3*(WIDTH//4) - XSHIFT, Y_DEPTH-YSHIFT],
    (3,0): [3*(WIDTH//4) - XSHIFT, HEIGHT - Y_DEPTH - YSHIFT],
    (3,1): [WIDTH//2 - XSHIFT, HEIGHT - Y_DEPTH - YSHIFT],
    (3,2): [WIDTH//4 - XSHIFT, HEIGHT - Y_DEPTH - YSHIFT],
    (0,4): [WIDTH//2, HEIGHT//2],
    # exceptions
    0: [3*(WIDTH//4),Y_DEPTH - YSHIFT]
    }


FEATURE_DICT = {
    "C": "City",
    "R": "Road",
    "G": "Farm",
    "Monastery":"Monastery"
    }


class nextTile:
    
    def __init__(self, Carcassonne, displayScreen, RunInit = True):
        self.Carcassonne = Carcassonne
        self.nextTileIndex = self.Carcassonne.nextTileIndex()
        
        if self.nextTileIndex == -1: #no more tiles left
            RunInit = False
            
        self.Tile = Tile(self.nextTileIndex, RunInit)
        self.Meeple = None
        
        if RunInit:
            self.image_file = self.Tile.image
            self.image = pygame.image.load(self.image_file)
            self.Rotation = self.Tile.Rotation  # new rotation
            self.Rotated = 0  # previous rotations
            self.numberOfRotations = len(self.Tile.AvailableRotations)
            # increase image scale
            self.image = self.increaseScale(self.image, 2)
            self.width = self.image.get_rect().size[0]
            # location
            self.X = displayScreen.Total_Grid_Width + (displayScreen.Menu_Width - self.width)/2
            self.Y = 25
            # list of all possible coordinates
            self.possibleCoords = self.possibleCoordinates()   
            self.possibleCoordsMeeples = self.possibleCoordinatesMeeples() 
            
            # Meeple Info Label
            meepleRect = (0,0, 300, 160)
            self.meepleLabel = pygame.Surface(pygame.Rect(meepleRect).size)
            self.meepleLabel.set_alpha(165)
            pygame.draw.rect(self.meepleLabel, BROWN, self.meepleLabel.get_rect(), 10)
            # last move label
            moveRect = (0,0, 300, 125)
            self.moveLabel = pygame.Surface(pygame.Rect(moveRect).size)
            self.moveLabel.set_alpha(180)
            pygame.draw.rect(self.moveLabel, BROWN, self.moveLabel.get_rect(), 10)
            
            # rotation images and labels
            self.leftRotImage = pygame.image.load('pygame_images/left_rotate.png')
            self.rightRotImage = pygame.image.load('pygame_images/right_rotate.png')
            
    
    
    
    def resetImage(self):
        self.image = pygame.image.load(self.image_file)
        self.image = self.increaseScale(self.image, 2)
        self.Rotated = 0
    
    
    def increaseScale(self, image, ratio):
        new_width = int(ratio * (self.image.get_rect().size)[0])
        new_height = int(ratio * (self.image.get_rect().size)[1])
        scaledImage = pygame.transform.scale(image, (new_width, new_height))
        return scaledImage
    
    
    def rotate(self, rotation, newRotation):
        if newRotation:
            old_rotation = self.Rotation
            old_rotated = self.Rotated
            
            self.Rotation =  rotation
            self.Rotated = (self.Rotated + rotation) % 4
            
            # not all tiles can rotate or rotate more than once
            if self.Rotated < 0 or (self.Rotated+1 > self.numberOfRotations):
                self.Rotation = old_rotation
                self.Rotated = old_rotated
                
        # reverse rotation for displaying tile
        self.Tile.Rotate(90*self.Rotation)
        imageRotation = 360 - (90*self.Rotation)
        
        self.image = pygame.transform.rotate(self.image, imageRotation)
        self.possibleCoords = self.possibleCoordinates()  # update for new rotation
        self.possibleCoordsMeeples = self.possibleCoordinatesMeeples()
        self.Rotation = 0
        
        
    def showNextTile(self, displayScreen, rotation, newRotation):
        GAME_DISPLAY = displayScreen.pygameDisplay
        self.rotate(rotation, newRotation)
        image_width = (self.image.get_rect().size)[0]
        
        x1 = self.X - 25
        x2 = self.X + image_width + 25
        y1 = self.Y + 120
        
        left_color = right_color = BLACK
        
        # change colour if button clicked
        if newRotation:
            left_color = GREEN if rotation == -1 else BLACK 
            right_color = GREEN if rotation == 1 else BLACK 
        
        # arrows
        pygame.draw.polygon(GAME_DISPLAY, left_color, ((x1,y1), (x1,y1+32), (x1-25,y1+16)))
        pygame.draw.polygon(GAME_DISPLAY, right_color, ((x2,y1), (x2,y1+32), (x2+25,y1+16)))
        
        # image and rotation symbols
        GAME_DISPLAY.blit(self.leftRotImage, (self.X-60,self.Y+40))
        GAME_DISPLAY.blit(self.rightRotImage, (image_width+self.X+10,self.Y+40))
        GAME_DISPLAY.blit(self.image, (self.X,self.Y))
        
        
    
    def showInfos(self, displayScreen):
        """
        Return a list of possible Meeple Locations
        """
        GAME_DISPLAY = displayScreen.pygameDisplay
        Grid_Window_Width = displayScreen.Total_Grid_Width
        Grid_Window_Height = displayScreen.Total_Grid_Height
        Menu_Width = displayScreen.Menu_Width
        width = (self.meepleLabel.get_rect().size)[0]
        GAME_DISPLAY.blit(self.meepleLabel, (Grid_Window_Width + (Menu_Width - width)/2, 300))
        GAME_DISPLAY.blit(self.moveLabel, (Grid_Window_Width + (Menu_Width - width)/2, Grid_Window_Height - 340))
        
        
    def possibleCoordinates(self):
        """
        Return a list of all playable coordinates for the current tile
        """
        availableMoves = self.Carcassonne.availableMoves()
        
        coordinates = []
        
        for move in availableMoves:
            #print(f'(pygameNextTile) Move: {move}')
            if move.Rotation == (self.Rotated * 90):
                coordinates.append((move.X, move.Y))
        return coordinates


    def possibleCoordinatesMeeples(self):
        """
        Return a list of all playable coordinates for the current tile
        """
        availableMoves = self.Carcassonne.availableMoves()
        coordinates = []
        
        for move in availableMoves:
            MeepleInfo = move.MeepleInfo
            if MeepleInfo == self.Meeple:
                if move.Rotation == (self.Rotated * 90):
                    coordinates.append((move.X, move.Y))
        return coordinates



    def highlightPossibleMoves(self, displayScreen):
        """
        Highlight on the grid where the player can place the next tile
        """
        
        for X,Y in self.possibleCoords:
            # all possible moves
            placeColourTile(X, Y, displayScreen, BLUE)
        for X,Y in self.possibleCoordsMeeples:
            # possible moves for meeple choice
            placeColourTile(X, Y, displayScreen, GREEN)
    
    
    # representation of tile
    def __repr__(self):
        ShowImage = True
        if ShowImage:
            image = cv2.imread(self.image_file)
            if self.Rotated > 0:
                image = cv2.rotate(image, ROTATE_DICT[90 * self.Rotated])
            showImage(image)
                    
        String = "Tile Index:" + str(self.nextTileIndex) + ", Description:\n"
        String += "Rotation: " + str(self.Rotation) + "\n"
        return String
        
    
    def evaluate_click(self, mouse_pos, displayScreen):
        """
        Select a board position to place the tile
        """
        X, Y = get_clicked_X(mouse_pos, displayScreen), get_clicked_Y(mouse_pos, displayScreen)
        return X, Y
    
    
    def displayTextClickedTile(self, X,Y):
        """
        Give information on clicked game tile
        """
        tiles = self.Carcassonne.Board
        tile = tiles[X,Y]
        return tile.info
    
    
    def addMeepleLocations(self, location_key, Location, NumberKey, numberSelected, TileIndex):
        """
        Add meeples or meeple locations to tile
        """
        Feature = location_key[0]
        circleColour = WHITE
        background = None
        thickness = 2
        
        # change colour for selected meeple location
        if NumberKey == numberSelected:
            if NumberKey == 0:
                background = None
                self.Meeple = None
                thickness = 2
            else:
                background = MEEPLE_CHOICE_HIGHLIGHT
                circleColour = MEEPLE_CHOICE_HIGHLIGHT
                self.Meeple = location_key
                thickness = 0
        
        text = str(NumberKey)
        X,Y = meepleCoordinates(Location, Feature, MEEPLE_LOCATION_DICT_SCALED, TileIndex)
        
        # image label
        meepleLabelImage = Label(text, font_size=FONT_MEEPLE_IMAGE, background = background)
        pygame.draw.circle(self.image, circleColour, (X+7,Y+12), 16, thickness)
        self.image.blit(meepleLabelImage.text_surface, (X,Y))
    
    
    def pressSpaceInstruction(self):
        """
        Instruct user to press space to force AI to make move
        """
        text = "Press SPACEBAR (AI move)"
        spcaebarLabel = Label(text, font_size=FONT_MEEPLE_MENU, background = WHITE)
        self.meepleLabel.blit(spcaebarLabel.text_surface, (20, 70))
        
        
    def updateMeepleMenu(self, location_key, Location, NumberKey, numberSelected):
        
        Feature = location_key[0]
        background = background0 = WHITE
        
        # change colour for selected meeple location
        if (NumberKey == numberSelected):
            background = MEEPLE_CHOICE_HIGHLIGHT
        
        if (numberSelected == 0):
            background0 = MEEPLE_CHOICE_HIGHLIGHT
        
        # each label has a "No Meeple Option"
        text = "0. No Meeple"
        meepleInfoLabel = Label(text, font_size=FONT_MEEPLE_MENU, background = background0)
        self.meepleLabel.blit(meepleInfoLabel.text_surface, (MEEPLE_LABEL_X, MEEPLE_LABEL_Y - MEEPLE_LABEL_SHIFT_Y))
        
        # info label
        x = MEEPLE_LABEL_X
        y = MEEPLE_LABEL_Y
        
        # rows
        shiftY = MEEPLE_LABEL_SHIFT_Y * ((NumberKey-1) % 4)
        y += shiftY
        
        # next column
        shiftX = 0 if NumberKey < 5 else MEEPLE_LABEL_SHIFT_X
        x += shiftX
        
        # create label
        text = str(NumberKey) + ". " + str(FEATURE_DICT[Feature])
        meepleInfoLabel = Label(text, font_size=FONT_MEEPLE_MENU, background = background)
        self.meepleLabel.blit(meepleInfoLabel.text_surface, (x,y))
        
        
    def updateMoveLabel(self, Carcassonne, selectedMove, isStartOfGame):
        # check if any moves have been played yet
        move = selectedMove
        player = 3 - Carcassonne.playerSymbol
        
        # text
        title = "Last Move:"
        tile = " Tile: " + str(move[0]) +" - " + Tile(move[0]).tile_desc
        location = f' X: {move[1]}, Y: {move[2]}, Rotation: {move[3]}'
        meeple = " Meeple: None" if move[4] is None else f' Meeple: {FEATURE_DICT[move[4][0]]}'
        player = f' Player {player}'
        
        if isStartOfGame:
            player = " Game Starting Tile"
            
        moveLabel1 = Label(title, font_size=25, background = WHITE)
        moveLabel2 = Label(tile, font_size=20, background = None, foreground = WHITE)
        moveLabel3 = Label(location, font_size=20, background = None, foreground = WHITE)
        moveLabel4 = Label(meeple, font_size=20, background = None, foreground = WHITE)
        moveLabel5 = Label(player, font_size=20, background = None, foreground = WHITE)
        
        #self.meepleLabel.blit(meepleInfoLabel.text_surface, (x,y))
        
        self.moveLabel.blit(moveLabel1.text_surface, (15, 10))
        self.moveLabel.blit(moveLabel2.text_surface, (15, 35))
        self.moveLabel.blit(moveLabel3.text_surface, (15, 55))
        self.moveLabel.blit(moveLabel4.text_surface, (15, 75))
        self.moveLabel.blit(moveLabel5.text_surface, (15, 95))
        
        
            
            
        
        
        
        
        
        