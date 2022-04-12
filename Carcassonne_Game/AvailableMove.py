"""AvailableMove Class

The contents of this class is used by 'Carcassonne' to display
which moves are available at the current turn/state of the 
game.

    Typical usage example:
    
    moves = AvailableMove(TileIndex=1, X=2, Y=3, Rotation=90, MeepleInfo=(Feature='C',i=0))

"""


class AvailableMove:
    """
    A class used to represent available moves.
    
    'AvailableMove' objects are used in the Carcassonne.availableMoves() 
    method to contain all the factors of a playable move into one object.
    
    ...
    
    Attributes
    ----------
    TileIndex : 
        Index of tile (0-23)
    X, Y : 
        X and Y coordinates of board position
    Rotation : 
        Orientation of tile
    MeepleInfo : 
        The type of Game feature the Meeple is placed on.
        Index is needed if more than instance of same feature type on tile.
    move :
        All information in one attributes

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    
    
    def __init__(self, TileIndex, X, Y, Rotation, MeepleInfo = None):
    
        self.TileIndex = TileIndex
        self.X = X
        self.Y = Y
        self.Rotation = Rotation
        self.MeepleInfo = MeepleInfo
        self.move = (TileIndex, X, Y, Rotation, MeepleInfo)
        self.moveString = f'({TileIndex}, {X}, {Y}, {Rotation}, {MeepleInfo})'
        
    def __repr__(self):
        if self.MeepleInfo is not None:
            Location = self.MeepleInfo[0]
            LocationIndex = self.MeepleInfo[1]
            
            if Location == 'C':
                FullLocation = "City"
            elif Location == 'R':
                FullLocation = "Road"
            elif Location == "G":
                FullLocation = "Farm"
            else:
                FullLocation = "Monastery"
            
            MeepleString = ", Meeple Location: " + FullLocation + ", Location Index: " + str(LocationIndex)
            
        else:
            MeepleString = ""
        
        String = "TileIndex: " + str(self.TileIndex) + ", (X,Y): (" + str(self.X) + "," + str(self.Y) + "), Rotation: " + str(self.Rotation) + MeepleString
        return String
        