"""
The Tile class will store information and properties of each of the tiles 
available in Carcassonne
"""
import cv2
from Carcassonne_Game.Tile_dict import TILE_DESC_DICT, HAS_NOT_FARM, FARM_OPENINGS_DICT, FARM_CITY_INDEX_DICT, HAS_CITY, CITY_OPENINGS_DICT, IS_DOUBLE, HAS_ROAD, ROAD_OPENINGS_DICT, HAS_MONASTERY, NO_ROTATIONS, ONE_ROTATION, TILE_PROPERTIES_DICT, MEEPLE_LOC_DICT
            

def showImage(frame):
    cv2.imshow("Image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


ROTATION_DICT = {
        0:[0,1,2,3],
        90:[3,0,1,2],
        180:[2,3,0,1],
        270:[1,2,3,0]
        }
    
SIDE_CHANGE_DICT = {
        0:0,
        90:1,
        180:2,
        270:3
        }

ROTATE_DICT = {
        90:0,
        180:1,
        270:2
        }


class Tile:
    def __init__(self, TileIndex, RunInit = True):
        
        # initialize parameters
        self.TileIndex = TileIndex
        self.TileCitiesIndex = [None,None,None,None]
        self.TileRoadsIndex = [None,None,None,None]
        self.TileFarmsIndex = [[None,None,None],[None,None,None],[None,None,None],[None,None,None]]
        self.Rotation = 0
        self.Meeple = None  # [MeepleFeature, (MeepleLocation), PlayerNumber]
        
        # image location
        self.image = "images/" + str(self.TileIndex) + ".png"
        
        # description of tile
        if self.TileIndex == -1:  # no more cards left
            self.tile_desc = ""
            RunInit = False  # fail safe
        else:
            self.tile_desc = TILE_DESC_DICT[self.TileIndex]        
        
        if RunInit:
            # farms
            self.HasFarms = False
            if self.TileIndex not in HAS_NOT_FARM:
                self.HasFarms = True
                self.FarmOpenings = FARM_OPENINGS_DICT[self.TileIndex]
                self.FarmRelatedCityIndex = FARM_CITY_INDEX_DICT[self.TileIndex]                
                
            # cities
            self.HasCities = False
            if self.TileIndex in HAS_CITY:
                self.HasCities = True
                self.CityOpenings = CITY_OPENINGS_DICT[self.TileIndex]
                self.CityValues = 2 if self.TileIndex in IS_DOUBLE else 1                
            
            # roads
            self.HasRoads = False
            if self.TileIndex in HAS_ROAD:
                self.HasRoads = True      
                self.RoadOpenings = ROAD_OPENINGS_DICT[self.TileIndex]
                
            # monastery
            self.HasMonastery = False
            if self.TileIndex in HAS_MONASTERY:
                self.HasMonastery = True         
                
            # rotations available
            if self.TileIndex in NO_ROTATIONS:
                self.AvailableRotations = [0]
            elif self.TileIndex in ONE_ROTATION: 
                self.AvailableRotations = [0,90]
            else:
                self.AvailableRotations = [0,90,180,270]             
            # properties + meeple locations
            self.Properties = TILE_PROPERTIES_DICT[self.TileIndex]
            self.AvailableMeepleLocs = MEEPLE_LOC_DICT[self.TileIndex]
            
            # string of information
            self.info = self.TileInfo()
        
    
    def TileInfo(self):
        return "Tile Index:" + str(self.TileIndex) + " Properties: " + str(self.Properties) + " Rotation: " + str(self.Rotation) + " Meeple: " + str(self.Meeple)
        
        
    # copy the tile
    def CloneTile(self):
        Clone = Tile(self.TileIndex, RunInit = False)
        Clone.TileCitiesIndex = [x for x in self.TileCitiesIndex]
        Clone.TileRoadsIndex = [x for x in self.TileRoadsIndex]
        Clone.TileFarmsIndex = [[y for y in x] for x in self.TileFarmsIndex]
        Clone.HasMonastery,Clone.HasCities,Clone.HasRoads,Clone.HasFarms,Clone.AvailableRotations = self.HasMonastery,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations
        if self.HasCities:
            Clone.CityValues = self.CityValues
            Clone.CityOpenings = [[x for x in k] for k in self.CityOpenings]
        if self.HasRoads:
            Clone.RoadOpenings = [[x for x in k] for k in self.RoadOpenings]
        if self.HasFarms:
            Clone.FarmOpenings = [[x for x in k] for k in self.FarmOpenings]
            Clone.FarmRelatedCityIndex = [[x for x in k] for k in self.FarmRelatedCityIndex]
        Clone.Properties = [x for x in self.Properties]
        Clone.AvailableMeepleLocs = {k:v for k,v in self.AvailableMeepleLocs.items()}
        return Clone

    
    # rotate the tile
    def Rotate(self, NewRotation):
        if NewRotation != self.Rotation:
            NeededRotation = (NewRotation - self.Rotation) % 360 # modulo 360
            self.Rotation = NewRotation
            
            # number of rotations
            SideChange = SIDE_CHANGE_DICT[NeededRotation]
            
            # change orientation of rotated tile
            CurrentOrder = [0,1,2,3]
            NewOrder = CurrentOrder[-SideChange:] + CurrentOrder[:-SideChange]
            
            # rearrange tile properties ('R','C','G')
            self.Properties = [self.Properties[i] for i in NewOrder]
            
            # meeple locations
            self.AvailableMeepleLocs = {k:tuple([v[0]+SideChange if v[0]+SideChange < 4 else v[0]+SideChange-4,v[1]]) for k,v in self.AvailableMeepleLocs.items()}
            
            # cities
            if self.HasCities:
                self.TileCitiesIndex = [self.TileCitiesIndex[i] for i in NewOrder]
                self.CityOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.CityOpenings]
            
            # roads
            if self.HasRoads:
                self.TileRoadsIndex = [self.TileRoadsIndex[i] for i in NewOrder]
                self.RoadOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.RoadOpenings]
            
            # farms
            if self.HasFarms:
                self.TileFarmsIndex =  [self.TileFarmsIndex[i] for i in NewOrder]
                self.FarmRelatedCityIndex =  [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.FarmRelatedCityIndex]
                self.FarmOpenings =  [[(x+SideChange,y) if x+SideChange < 4 else (x+SideChange-4,y) for (x,y) in k] for k in self.FarmOpenings]
                
            # update info
            self.info = self.TileInfo()            
            
    
    # representation of tile
    def __repr__(self):
        ShowImage = False
        """
        if ShowImage:
            image = cv2.imread(self.image)
            if ((self.Rotation % 360) > 0):
                image = cv2.rotate(image, ROTATE_DICT[self.Rotation])
            showImage(image)
        """            
        String = "Tile Index:" + str(self.TileIndex) + ", Description: " + str(self.tile_desc) + "\n"
        String += "Properties: " + str(self.Properties) + "\n"
        String += "Rotation: " + str(self.Rotation) + "\n"
        String += "Tile City Index: "+str(self.TileCitiesIndex)+"\nTile Road Index: "+str(self.TileRoadsIndex)+"\nTile Farm Index: "+str(self.TileFarmsIndex)
        return String      
    
    
##############################################################################
##############################################################################
##############################################################################



class AvailableMove:
    """
    'AvailableMove' objects are used in the Carcassonne.availableMoves() 
    method to contain all the factors of a playable move into one object
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