import random as rd
import itertools as it

            
class TicTacToeState:
    """
    List of important attributes:
        self.p1 - player 1 (class 'Player')
        self.p2 - player 2 (class 'Player')   
        
        self.Board:
            A dictionary of all played tiles on the board. The keys are (x,y)
            coordinates of the tile, and the values are the tile (Tile class)
        
        self.BoardCities, BoardRoads, BoardMonasteries, BoardFarms:
            A dictionary for each of the 4 features* with the keys as the index
            of each feature, with values as the respective feature objects
            
            * Each of these features has their own designated class
            
        self.MonasteryOpenings:
            Dictionary containing (x,y) coordinates of available spaces 
            surrounding a monastery
            
        self.AvailableSpots:
            A set of (x,y) coordinates that surround all played tiles, ie all
            possible locations a tile could be placed
            
        self.Meeples:
            Available Meeple count for both players [P1, P2]. Both players 
            start with 7
            
        self.winner:
            Result at end of game. 1=P1 wins, 2=P2 wins, 0=Draw
            
        self.result:
            P1's Score - P2's Score at the end of the game
            
        self.Scores:
            Current scores and virtual scores at any point of the game
        
        self.playerSymbol:
            Indicates the current player
            
        self.isGameOver:
            Whether game is over or not
            
        self.TileQuantities:
            Count of each tile type (1 of tile 0, 3 of tile 1, etc.)
            
        self.TotalTiles:
            Number of tiles remaining
            
        self.UniqueTilesCount:
            Count of unique tiles left
            
        self.TileIndexList:
            List of tile types left in the game
            
        self.deck:
            Shuffled order of self.TileIndexList
    """
    
    def __init__(self, p1, p2, RunInit=True):
        
        # players
        self.p1 = p1
        self.p2 = p2
        self.name = "TicTacToe"
        
        #Initialialize variables        
        self.Board = {}
        self.MonasteryOpenings = {}
        self.AvailableSpots = set()
        self.AvailableSpots.add((0,0))
        self.AvailableSpots.add((0,1))
        self.AvailableSpots.add((0,2))
        self.AvailableSpots.add((1,0))
        self.AvailableSpots.add((1,1))
        self.AvailableSpots.add((1,2))
        self.AvailableSpots.add((2,0))
        self.AvailableSpots.add((2,1))
        self.AvailableSpots.add((2,2))
        #self.AvailableMoves = []
        self.winner = None
        self.result = None
        self.playerSymbol = 1
        self.isGameOver = False
        self.Turn = 0  # number of turns played
        # scores
        self.Scores = [0,0,0,0]  #P1, P2, P1 virtual, P2 virtual
        self.FeatureScores = [   # [City, Road, Monastery, City(Incomplete), Road(Incomplete), Monastery(Incomplete), Farms]
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
            ]
            
        
    
    def CloneState(self):
        """
        Clones the game state - quicker than using copy.deepcopy()
        """
        Clone = TicTacToeState(self.p1, self.p2, RunInit = False)
        Clone.Board = {k:v for k,v in self.Board.items()}
        Clone.AvailableSpots = set([x for x in self.AvailableSpots])
        Clone.winner = self.winner
        Clone.result = self.result
        Clone.playerSymbol = self.playerSymbol
        Clone.isGameOver = self.isGameOver   
        Clone.Turn = self.Turn
        Clone.Scores = [x for x in self.Scores]
        Clone.FeatureScores = [x[:] for x in self.FeatureScores]
        return Clone

    
    def reset(self):
        """
        Create a fresh game board
        """
        return TicTacToeState(self.p1, self.p2)
    

    def move(self, Move = None):
        """
        Place a move on the game board
        Inputs:
            - Move (a tuple):
                - X,Y: Position of tile on the board
        """
        # split up 'Move' object
        X,Y = Move[0], Move[1]
        
        self.AvailableSpots.remove((X,Y))
        self.Board[(X,Y)] = self.playerSymbol
        
        if self.Turn > 3:
            for surrounding in ((1,0),(0,1),(1,1),(1,-1)):
                if self.isWin(X,Y,surrounding[0], surrounding[1]):
                    self.winner = self.playerSymbol
                    self.isGameOver = True
                    if self.playerSymbol == 1:
                        self.result = 1
                    else:
                        self.result = -1
                    return      

        if len(self.AvailableSpots) == 0:
            self.result = 0
            self.winner = 0
            self.isGameOver = True
            return
        
        #Turn end routine
        self.playerSymbol = 3 - self.playerSymbol # switch turn
        self.Turn += 1  # increment turns


    def isWin(self,X,Y,h,v):
        line_count = 1
        i = 2
        th, tv = h, v
        while((X+th,Y+tv) in self.Board):
            if self.Board[(X+th,Y+tv)] == self.playerSymbol:
                line_count += 1
                th = th*i
                tv = tv*i
                i += 1
            else: break

        i = 2
        th, tv = h, v
        while((X-th,Y-tv) in self.Board):
            if self.Board[(X-th,Y-tv)] == self.playerSymbol:
                line_count += 1
                th = th*i
                tv = tv*i
                i += 1
            else: break

        if line_count >= 3:
            return True
        return False

    def availableMoves(self):
        return [AvailableMove(spot[0], spot[1]) for spot in self.AvailableSpots]
    
    def checkWinner(self):
        """
        Returns result
        """
        return self.result
    
    def getRandomMove(self):
        """
        Returns a random move from all possible moves
        """
        availableMoves = self.availableMoves()
        return rd.choice(availableMoves)
    
    def shuffle(self): #DUMMY. Called by MCTS agents
        return
    
    def __repr__(self):
        Str = ""
        for row in range(3):
            for column in range(3):
                x = (row, column)
                if x in self.Board:
                    Str += str(self.Board[x])
                else: Str += "."
            Str += "\n"
            
        return Str



class AvailableMove:
    """
    A class used to represent available moves.
    
    ...
    Attributes
    ----------
    X, Y : 
        X and Y coordinates of board position
    move :
        All information in one attributes
    """
    
    
    def __init__(self, X, Y):
    
        self.X = X
        self.Y = Y
        self.move = (X, Y)
        self.moveString = f'({X}, {Y})'
        
    def __repr__(self):
        String = "(X,Y): (" + str(self.X) + "," + str(self.Y) + ")"
        return String
        
             
            