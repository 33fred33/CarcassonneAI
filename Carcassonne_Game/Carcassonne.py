import random as rd
import itertools as it

from Carcassonne_Game.Tile import Tile, ROTATION_DICT, SIDE_CHANGE_DICT, AvailableMove
from Carcassonne_Game.GameFeatures import Monastery

from Carcassonne_Game.Carcassonne_CityUtils import cityConnections, cityClosures
from Carcassonne_Game.Carcassonne_RoadUtils import roadConnections, roadClosures
from Carcassonne_Game.Carcassonne_FarmUtils import farmConnections


"""

In this script you will find the class for the game states of Carcassonne.
Every AI player is entitled to the information in this game state when deciding
to make the move.

However there are some rules that must be followed:
    1.  A player must only know the tile at the top of the deck. For any AIs 
        that use simulations of future states (e.g. MCTS), the deck must be 
        shuffled for tiles played after the top tile
    2.  Players are allowed to check which tiles are left. There are only 72
        tiles, so it would be common for players to know what tiles are left in 
        the deck based on which ones have been played
        



Orientation of the tile:
    Left:0 
    Top:1 
    Right:2
    Bottom:3
              
               1
    ----------------------
    |                    |
    |                    |
    |                    |
 0  |                    |  2
    |                    |
    |                    |
    |                    |
    ----------------------
              3

Left:0, Top:1, Right:2, Bottom:3

Dict of side comparison values - 
    For example, when checking if two tiles can be combined, the left side (0) of one tile 
    is compared against the right side (2) of the other tile to see if they are compatible

"""
SIDE_COMPARISON_DICT={
    2:0,
    3:1,
    0:2,
    1:3
    }


            
class CarcassonneState:
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
    
    def __init__(self, p1, p2, RunInit=True, no_farms = False, no_monasteries = False):
        
        # players
        self.p1 = p1
        self.p2 = p2
        self.name = "Carcassonne"
        self.no_farms = no_farms
        self.no_monasteries = no_monasteries
        
        #Never changing:
        self.MatchingSide = [2,3,0,1]
        self.MatchingLine = [2,1,0]
        #Initialialize variables        
        self.Board = {}
        self.BoardCities = {}
        self.BoardRoads = {}
        self.BoardMonasteries = {}
        self.BoardFarms = {}
        self.MonasteryOpenings = {}
        self.AvailableSpots = set()
        self.AvailableSpots.add((0,0))  # first tile always placed in this position
        #self.AvailableMoves = []
        self.Meeples = [7,7]
        self.winner = None
        self.result = None
        self.playerSymbol = 2  # player 2 "plays" the first tile 
        self.isGameOver = False
        self.Turn = 0  # number of turns played
        # scores
        self.Scores = [0,0,0,0]  #P1, P2, P1 virtual, P2 virtual
        self.FeatureScores = [   # [City, Road, Monastery, City(Incomplete), Road(Incomplete), Monastery(Incomplete), Farms]
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
            ]
        
        
        
        if RunInit:
            # Number of tiles per TileIndex, i.e. 1 tile for 0th tile, 3 for 1st tile, etc.
            
            
            if self.no_monasteries:
                self.TileQuantities = [1,3,1,1,2,3,2,2,2,3,1,3,2,5,3,0,4,3,3,4,0,9,8,1]
                self.TileIndexList = [0, 1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 
                                    10, 11, 11, 11, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 
                                    16, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 19, 
                                    21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 
                                    22, 22, 22, 22, 22, 22, 23]
            else:
                self.TileQuantities = [1,3,1,1,2,3,2,2,2,3,1,3,2,5,3,2,4,3,3,4,4,9,8,1]
                self.TileIndexList = [0, 1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 
                                    10, 11, 11, 11, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 15, 
                                    15, 16, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 19, 
                                    20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 
                                    22, 22, 22, 22, 22, 22, 23]
            self.TotalTiles = sum(self.TileQuantities)
            self.UniqueTilesCount = len(self.TileQuantities)
                
            # create deck
            #self.deck = [x for x in self.TileIndexList]
            self.deck = self.TileIndexList.copy()
            rd.shuffle(self.deck)  # shuffle the deck
            
            # each game starts with the same tile (Tile16) being placed
            # PlayingTileIndex=16, X,Y = 0,0, Rotation=0, MeepleKey=None
            self.move([16, 0, 0, 0, None])
            
            # code for running tests by arranging the order of the first few tiles
            """
            index = self.deck.index(0)
            self.deck[index] = self.deck[0]
            self.deck[0] = 0
            
            index = self.deck.index(0)
            self.deck[index] = self.deck[1]
            self.deck[1] = 0
            
            index = self.deck.index(20)
            self.deck[index] = self.deck[2]
            self.deck[2] = 20
            """
            
            
        
    
    def CloneState(self):
        """
        Clones the game state - quicker than using copy.deepcopy()
        """
        #Clone = copy.deepcopy(self)
        Clone = CarcassonneState(self.p1, self.p2, RunInit = False, no_farms = self.no_farms, no_monasteries = self.no_monasteries)
        Clone.Board = {k:v.CloneTile() for k,v in self.Board.items()}
        Clone.BoardCities = {k:v.CloneCity() for k,v in self.BoardCities.items()}
        Clone.BoardRoads = {k:v.CloneRoad() for k,v in self.BoardRoads.items()}
        Clone.BoardMonasteries = {k:v.CloneMonastery() for k,v in self.BoardMonasteries.items()}
        Clone.BoardFarms = {k:v.CloneFarm() for k,v in self.BoardFarms.items()}
        Clone.MonasteryOpenings = {k:[x for x in v] for k,v in self.MonasteryOpenings.items()}
        Clone.AvailableSpots = set([x for x in self.AvailableSpots])
        #Clone.AvailableMoves = [x for x in self.AvailableMoves] #Not needed?
        Clone.Meeples = [x for x in self.Meeples]
        Clone.winner = self.winner
        Clone.result = self.result
        Clone.playerSymbol = self.playerSymbol
        Clone.isGameOver = self.isGameOver   
        Clone.Turn = self.Turn
        Clone.Scores = [x for x in self.Scores]
        Clone.FeatureScores = [x[:] for x in self.FeatureScores]
        Clone.TileQuantities = [x for x in self.TileQuantities]
        Clone.TotalTiles = self.TotalTiles
        Clone.UniqueTilesCount = self.UniqueTilesCount   
        Clone.TileIndexList = [x for x in self.TileIndexList]
        Clone.deck = [x for x in self.deck]
        return Clone

    
    def reset(self):
        """
        Create a fresh game board
        """
        return CarcassonneState(self.p1, self.p2)
    
    def shuffle(self):
        """
        Shuffles the deck - used for randomness in MCTS
        """
        rd.shuffle(self.deck)
    
    
    def AddMeeple(self, MeepleUpdate, MeepleKey, FeatureCharacter, i):
        """
        Add meeple to section of tile
        
        Inputs:
            - MeepleUpdate: [p1_Meeple, p2_Meeple] - List of Meeples (e.g [1,0] means P1 is adding a Meeple)
            - MeepleKey: Feature to which Meeple is added
            - FeatureCharacter: Possible Meeple Location
            - i: Possible feature index
        """
        AddedMeeples = [0,0]
        if MeepleKey is not None:
            # which feature the meeple is added to
                if MeepleKey[0] == FeatureCharacter and MeepleKey[1] == i:
                    AddedMeeples = MeepleUpdate
        return AddedMeeples
    
    
    def completeMonastery(self, AffectedMonastery):
        """
        Checks if the monastery is completed (completely surrounded)
        """
        AffectedMonastery.Value += 1
        # if monastery is complete
        if AffectedMonastery.Value == 9:
            self.Meeples[AffectedMonastery.Owner] += 1  # return meeple to player
            self.Scores[AffectedMonastery.Owner] += 9  # award points to player
            self.FeatureScores[AffectedMonastery.Owner][2] += 9 # update monastery feature score
            AffectedMonastery.Value = 0  
    
    
    def checkMonasteryCompleteness(self, X,Y, SurroundingSpots, MeepleUpdate, MeepleKey=None ):    
        """
        Monastery completeness check
        
        Inputs:
            - X,Y: tile coordinates of tile just played
            - SurroundingSpots: Coordinates of surrounding spots (left,right,above,below)
            - MeepleUpdate: [p1_Meeple, p2_Meeple] - List of Meeples (e.g [1,0] means P1 is adding a Meeple)
            - MeepleKey:Feature to which Meeple is added
        """
        # check if new tile is surrounding a monastery
        if (X,Y) in self.MonasteryOpenings:
            # check if monastery is completed
            [(self.completeMonastery(self.BoardMonasteries[AffectedMonasteryIndex]))  for AffectedMonasteryIndex in self.MonasteryOpenings[(X,Y)]]
            # spot is now filled, remove from possible locations
            del self.MonasteryOpenings[(X,Y)]  
            
        #Monastery logic
        if MeepleKey is not None:
            if MeepleKey[0] == "Monastery":
                # monastery surroundings include all 8 surrounding positions
                CompleteSurroundingSpots = SurroundingSpots + [(X-1,Y-1),(X+1,Y+1),(X+1,Y-1),(X-1,Y+1)]
                NextMonasteryID = len(self.BoardMonasteries)  # increment ID by 1
                
                self.BoardMonasteries[NextMonasteryID] = Monastery(NextMonasteryID,self.playerSymbol-1)
                AffectedMonastery = self.BoardMonasteries[NextMonasteryID]
                [self.monasterySurroundings(Spot, AffectedMonastery, NextMonasteryID) for Spot in CompleteSurroundingSpots]
                
    
    def monasterySurroundings(self, Spot, AffectedMonastery, NextMonasteryID):
        """
        Function for 'for loop'
        
        Inputs:
            - Spot: (X,Y)
            - AffectedMonastery: Monastery feature
            - NextMonasteryID: If Monastery is new, this will be its ID
        """
        if Spot in self.Board:
            self.completeMonastery(AffectedMonastery)
        elif Spot in self.MonasteryOpenings:
            self.MonasteryOpenings[Spot].append(NextMonasteryID)
        else:
            self.MonasteryOpenings[Spot] = [NextMonasteryID]
            
            
    def checkCityCompleteness(self, PlayingTile, Surroundings, MeepleUpdate, MeepleKey=None):
        """
        Check if city has been completed
        
        Inputs:
            - PlayingTile: Tile just played 
            - Surroundings: List of surrounding tiles (left,right,above,below)
            - MeepleUpdate: [p1_Meeple, p2_Meeple] - List of Meeples (e.g [1,0] means P1 is adding a Meeple)
            - MeepleKey:Feature to which Meeple is added
        """

        if PlayingTile.HasCities:
            ClosingCities = []  # initialize list of closing cities
            ClosingCities = cityConnections(self, PlayingTile, Surroundings, ClosingCities, MeepleUpdate, MeepleKey)
            cityClosures(self, ClosingCities)
                       
            
    def checkRoadCompleteness(self, PlayingTile, Surroundings, MeepleUpdate, MeepleKey=None):            
        """
        Check if road has been completed
            
        Inputs:
            - PlayingTile: Tile just played 
            - Surroundings: List of surrounding tiles (left,right,above,below)
            - MeepleUpdate: [p1_Meeple, p2_Meeple] - List of Meeples (e.g [1,0] means P1 is adding a Meeple)
            - MeepleKey:Feature to which Meeple is added
        """
        if PlayingTile.HasRoads:
            ClosingRoads = [] # initialize list of closing cities
            ClosingRoads = roadConnections(self, PlayingTile, Surroundings, ClosingRoads, MeepleUpdate, MeepleKey)
            roadClosures(self, ClosingRoads)
    
    
    def checkFarmCompleteness(self, PlayingTile, Surroundings, MeepleUpdate, MeepleKey):
        """
        Check if farm has been completed
        
        Inputs:
            - PlayingTile: Tile just played 
            - Surroundings: List of surrounding tiles (left,right,above,below)
            - MeepleUpdate: [p1_Meeple, p2_Meeple] - List of Meeples (e.g [1,0] means P1 is adding a Meeple)
            - MeepleKey:Feature to which Meeple is added
        """
        if PlayingTile.HasFarms:
            farmConnections(self, PlayingTile, Surroundings, MeepleUpdate, MeepleKey)
            
            
            
    def UpdateVirtualScores(self):
        """
        Update virtual scores
        """
        self.Scores[2] = self.Scores[0]
        self.Scores[3] = self.Scores[1]
        # cities
        cityP1 = sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])        
        cityP2 = sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])        
        self.Scores[2] += cityP1
        self.Scores[3] += cityP2
        if self.isGameOver:
            self.FeatureScores[0][3] += cityP1
            self.FeatureScores[1][3] += cityP2
            
        # roads
        roadP1 = sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
        roadP2 = sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])
        self.Scores[2] += roadP1
        self.Scores[3] += roadP2
        if self.isGameOver:
            self.FeatureScores[0][4] += roadP1
            self.FeatureScores[1][4] += roadP2
        
        # monasteries
        monP1 = sum([v.Value for k,v in self.BoardMonasteries.items() if v.Owner == 0])
        monP2 = sum([v.Value for k,v in self.BoardMonasteries.items() if v.Owner == 1])
        self.Scores[2] += monP1
        self.Scores[3] += monP2
        if self.isGameOver:
            self.FeatureScores[0][5] += monP1
            self.FeatureScores[1][5] += monP2
        
        # farms
        farmP1 = 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
        farmP2 = 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])
        self.Scores[2] += farmP1
        self.Scores[3] += farmP2
        if self.isGameOver:
            self.FeatureScores[0][6] += farmP1
            self.FeatureScores[1][6] += farmP2
        #print(f'VIRTUAL POINTS: \nPlayer1: {self.Scores[2]}, Player2: {self.Scores[3]} \n')
        
    
    def nextTileIndex(self):
        """
        Returns index of next tile from the deck
        """
        if len(self.deck) == 0:
            index = -1
        else:
            index = self.deck[0]
        return index

    

    def move(self, Move = None):
        """
        Place a tile on the game board
        
        Inputs:
            - Move (a tuple):
                - PlayingTileIndex: Index of tile being played
                - X,Y: Position of tile on the board
                - Rotation: Rotation of tile
                - MeepleKey
        """
        # split up 'Move' object
        PlayingTileIndex = Move[0]
        X,Y = Move[1], Move[2]
        Rotation = Move[3]
        MeepleKey = Move[4]
        
        # fix for when the game chooses a tile after the end of game
        if PlayingTileIndex == -1:
            self.EndGameRoutine()
            return
        
        # remove played tile from list of remaining tiles
        self.AvailableSpots.remove((X,Y)) # position of placed tile is no longer available
        PlayingTile = Tile(PlayingTileIndex)
        self.deck.remove(PlayingTileIndex) # remove from deck
        self.TileQuantities[PlayingTileIndex] -= 1
        self.TotalTiles -= 1
        self.TileIndexList.remove(PlayingTileIndex) 
        
        #Surroundings analysis
        Surroundings = [None,None,None,None]  # initialization
        SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]  # left, above, right, below
        
        # check if there is a tile touching the newly placed tile
        for i in range(4):
            if not SurroundingSpots[i] in self.Board:
                self.AvailableSpots.add(SurroundingSpots[i])
            else:
                Surroundings[i] = self.Board[SurroundingSpots[i]]
        
        # add meeple info if one is played
        if not(MeepleKey is None):
            MeepleLocation = PlayingTile.AvailableMeepleLocs[MeepleKey]
            PlayingTile.Meeple = [MeepleKey[0], MeepleLocation, self.playerSymbol]
            
        # rotate tile to rotation specified and place tile on board
        PlayingTile.Rotate(Rotation)
        
        self.Board[(X,Y)] = PlayingTile  # add to board
        if MeepleKey is None:
            MeepleLoc = [0,0]
            MeepleUpdate = [0,0]
        else:
            player = self.playerSymbol - 1
            MeepleUpdate = [0,0]
            MeepleUpdate[player] += 1
            self.Meeples[player] -= 1
            
       
        # run logic for each of the game features
        # with new move, it is important to check if any features have been completed
        self.checkMonasteryCompleteness(X,Y,SurroundingSpots, MeepleUpdate, MeepleKey)
        self.checkCityCompleteness(PlayingTile, Surroundings, MeepleUpdate, MeepleKey)
        self.checkRoadCompleteness(PlayingTile, Surroundings, MeepleUpdate, MeepleKey)
        self.checkFarmCompleteness(PlayingTile, Surroundings, MeepleUpdate, MeepleKey)
        
        # update virtual scores
        self.UpdateVirtualScores()
        # check if game is over
        if self.TotalTiles == 0:
            self.EndGameRoutine()
            return
        
        #Turn end routine
        self.playerSymbol = 3 - self.playerSymbol # switch turn
        self.Turn += 1  # increment turns
    
    
    
    def EndGameRoutine(self):
        """
        Logic to handle when game is finished
        Declares self.winner and self.result
        """
        
        # game is finished
        self.isGameOver = True  
        self.UpdateVirtualScores()
        
        # final scores
        self.Scores[0] = self.Scores[2]
        self.Scores[1] = self.Scores[3]
        
        # declare winner
        if self.Scores[0] > self.Scores[1]:
            self.winner = 1 #P1 wins
        elif self.Scores[1] > self.Scores[0]:
            self.winner = 2 #P2 wins
        else:
            self.winner = 0 #Draw       
            
        self.result = self.Scores[2] - self.Scores[3]
        
    

    def doesTileFit(self, EvaluatedTile, Rotation, SurroundingSpots):
        """
        Checks if the tile ('EvaluatedTile') can be placed with this 'Rotation' 
        and based on 'SurroundingSpots'
        """
        # change values for each rotation value
        SideChange = SIDE_CHANGE_DICT[Rotation]
        R = ROTATION_DICT[Rotation]
        TileLeft,TileUp,TileRight,TileDown = R[0],R[1],R[2],R[3]
        Sides = [TileLeft,TileUp,TileRight,TileDown]
                
        # assume tile fits, need to check if tile does not fit
        IsTileFitting = True
        while True:
            for i in range(4):
                TestingTile = self.Board.get(SurroundingSpots[i])
                if TestingTile is not None:
                    if TestingTile.Properties[(i+2)%4] != EvaluatedTile.Properties[Sides[i]]:
                        IsTileFitting = False
                        break
            break
        return IsTileFitting, SideChange
    
    
    
    def movesWithMeeples(self, EvaluatedTile, HasFeature, Openings, 
                         Feature, SideChange, SurroundingSpots, 
                         TempAvailableMoves,TileIndex,X,Y,Rotation):
        """
        Checks which moves are available if the player has Meeples remaining.
        """
        # check if this feature exists in this tile
        if HasFeature:
            if Feature == "G": 
                RotatedOpenings = [[(x+SideChange,y) if x+SideChange < 4 else (x+SideChange-4,y) for (x,y) in k] for k in Openings]
            else:
                RotatedOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in Openings]
            
            for i in range(len(RotatedOpenings)):
                Openings = RotatedOpenings[i]
                MeepleFitting = True
            
                if Feature == "G":                    
                    for (FarmSide,FarmLine) in Openings:
                        if self.Board.get(SurroundingSpots[FarmSide]) is None:
                            pass
                        else:
                            MatchingFeature = self.matchingFeature(EvaluatedTile, self.BoardFarms, Feature, SurroundingSpots, FarmSide, FarmLine)
                            if MatchingFeature.Meeples[0] > 0 or MatchingFeature.Meeples[1] > 0:
                                MeepleFitting = False
                                break    
                else:
                    for Side in Openings:
                        if self.Board.get(SurroundingSpots[Side]) is None:
                            pass
                        else:
                            if Feature == "R":
                                BoardFeature = self.BoardRoads
                            elif Feature == "C":
                                BoardFeature = self.BoardCities
                            MatchingFeature = self.matchingFeature(EvaluatedTile, BoardFeature, Feature, SurroundingSpots, Side)
                            if MatchingFeature.Meeples[0] > 0 or MatchingFeature.Meeples[1] > 0:
                                MeepleFitting = False
                                break
                if MeepleFitting:
                    TempAvailableMoves.append( AvailableMove(TileIndex,X,Y,Rotation,(Feature,i)) )
                                        
        return TempAvailableMoves
                                
                            
    def matchingFeature(self, EvaluatedTile, BoardFeature, Feature, SurroundingSpots, Side, FarmLine = None):
        # cities
        if Feature == "C":
            MatchingIndex = self.Board.get(SurroundingSpots[Side]).TileCitiesIndex[self.MatchingSide[Side]]
        #roads 
        elif Feature == "R":
            MatchingIndex = self.Board.get(SurroundingSpots[Side]).TileRoadsIndex[self.MatchingSide[Side]]
        # farms
        else:
            MatchingIndex = self.Board.get(SurroundingSpots[Side]).TileFarmsIndex[self.MatchingSide[Side]][self.MatchingLine[FarmLine]]
        
        while BoardFeature[MatchingIndex].Pointer != BoardFeature[MatchingIndex].ID:                            
                MatchingIndex = BoardFeature[MatchingIndex].Pointer
        MatchingFeature = BoardFeature[MatchingIndex]    
        
        return MatchingFeature
    
    
    
        
    def availableMoves(self, TilesOnly = False, TileIndexOther = None):
        """
        Create a list of all available moves based on the Tile the player just 
        flipped.
        """
        
        # if game is over, return empty list
        if self.isGameOver:
            return []
        
        # tile is the next tile in the deck
        TileIndex = self.nextTileIndex() if TileIndexOther is None else TileIndexOther
        if TileIndex == -1:
            print(f'\n\n\n(Carcassonne.availableMoves)  No Moves!!  -  TileIndex: {TileIndex}  -  isGameOver: {self.isGameOver}  -  Deck Length: {len(self.deck)}  -  Game Turn: {self.Turn} \n\n\n')
            return [AvailableMove(-1,0,0,0,None)]  # game over
            
        # get the tile matching the index
        EvaluatedTile = Tile(TileIndex)
        
        allAvailableMoves = [(self.availableMovesForSpotRotations(Spot, Rotation, EvaluatedTile, TileIndex, TilesOnly)) 
                             for Spot in self.AvailableSpots for Rotation in EvaluatedTile.AvailableRotations] 
         
        allAvailableMoves = list(it.chain.from_iterable(allAvailableMoves))
        
        # check there are available moves
        amountMoves = len(allAvailableMoves)
        if amountMoves == 0:
            if TileIndexOther is not None:
                return []
            self.discardTile(TileIndex)
            allAvailableMoves = self.availableMoves()
        
        # list of all moves
        return allAvailableMoves
    
    
    def discardTile(self, TileIndex):
        """
        If there are no possible moves for a tile, then it should be discarded
        
        Input:
            - TileIndex: Index of tile to be removed
        """
        # discard tile
        self.deck.remove(TileIndex) # remove from deck
        self.TileQuantities[TileIndex] -= 1
        self.TotalTiles -= 1
        self.TileIndexList.remove(TileIndex)
    
    
    def availableMovesForSpotRotations(self, Spot, Rotation, EvaluatedTile, TileIndex, TilesOnly):
        """
        Checks available moves for each rotation
        """
        
        # X and Y values of possible spot
        X=Spot[0]
        Y=Spot[1]
        SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]
        availableMoves =  []
        
        IsTileFitting, SideChange = self.doesTileFit(EvaluatedTile, Rotation, SurroundingSpots)
        #TempAvailableMoves = []
        if IsTileFitting:            
            # add the possible move of adding the tile and placing no meeple
            availableMoves.append(AvailableMove(TileIndex,X,Y,Rotation,None))
            
            
            # now check for possible moves with adding meeples
            if not TilesOnly:
                    # check if current player has any meeples left
                    if self.Meeples[self.playerSymbol-1] > 0:
                        
                        # check which features have to be checked for
                        if EvaluatedTile.HasCities:
                            availableMoves = self.movesWithMeeples(EvaluatedTile, EvaluatedTile.HasCities, 
                                                                    EvaluatedTile.CityOpenings, "C", 
                                                                    SideChange, SurroundingSpots,availableMoves,
                                                                    TileIndex,X,Y,Rotation)
                        if EvaluatedTile.HasRoads:
                            availableMoves = self.movesWithMeeples(EvaluatedTile, EvaluatedTile.HasRoads, 
                                                                    EvaluatedTile.RoadOpenings, "R", 
                                                                    SideChange, SurroundingSpots,availableMoves,
                                                                    TileIndex,X,Y,Rotation)
                        if EvaluatedTile.HasFarms and not self.no_farms:
                            availableMoves = self.movesWithMeeples(EvaluatedTile, EvaluatedTile.HasFarms, 
                                                                    EvaluatedTile.FarmOpenings, "G", 
                                                                    SideChange, SurroundingSpots,availableMoves,
                                                                    TileIndex,X,Y,Rotation)
                        # monastery options
                        if EvaluatedTile.HasMonastery:
                            availableMoves.append( AvailableMove(TileIndex,X,Y,Rotation,("Monastery",0)) )
            #print(f'(Carcassonne.availableMovesForRotation) Available Moves: {availableMoves}')
        
        return availableMoves 
    
    
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
    
    
    def __repr__(self):
        #Str = str(self.TileIndexList) + "\n" + str(self.Board) + "\n" + str(self.BoardCities) + "\n" + str(self.BoardRoads) + "\n" + str(self.BoardMonasteries) + "\n" + str(self.BoardFarms)
        Str = str(self.TileIndexList)
        return Str


             
            