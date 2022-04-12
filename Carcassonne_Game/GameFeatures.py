"""
Create objects for each of the features in the game:
    - Monastery
    - Cities
    - Farms
    - Roads
"""
    

class Monastery:
    def __init__(self, ID = None, Owner = None):
        if ID is not None:
            self.ID = ID
            self.Owner = Owner
            self.Value = 1
    
    def CloneMonastery(self):
        Clone = Monastery()
        Clone.ID = self.ID
        Clone.Owner = self.Owner
        Clone.Value = self.Value
        return Clone
    
    def __repr__(self):
        String = "Monastery ID"+str(self.ID)+"Value"+str(self.Value)+"Owner"+str(self.Owner)
        return String 

        
    
class City:
    def __init__(self,ID = None, Value=None, Openings=None, Meeples=[0,0]):
        if ID is not None:
            self.ID = ID
            self.Pointer = ID
            self.Openings = Openings
            self.Value = Value
            self.Meeples = Meeples
            self.ClosedFlag = False
        
    def CloneCity(self):
        Clone = City()
        Clone.ID = self.ID
        Clone.Pointer = self.Pointer
        Clone.Openings = self.Openings
        Clone.Value = self.Value
        Clone.Meeples = [x for x in self.Meeples]
        Clone.ClosedFlag = self.ClosedFlag
        return Clone
        
    def Update(self, OpeningsChange = 0, ValueAdded = 0, MeeplesAdded = [0,0]):
        self.Openings += OpeningsChange
        self.Value += ValueAdded
        self.Meeples[1] += MeeplesAdded[1]
        self.Meeples[0] += MeeplesAdded[0]
        
    def __repr__(self):
        String = "City ID"+str(self.ID)+"Ptr"+str(self.Pointer)+"V"+str(self.Value)+"Ops"+str(self.Openings)+"Mps" + str(self.Meeples[0])+","+ str(self.Meeples[1])+"Clsd?"+str(self.ClosedFlag)
        return String
    

class Farm:
    def __init__(self,ID = None, Meeples=[0,0]):
        if ID is not None:
            self.ID = ID
            self.Pointer = ID
            self.CityIndexes = set()
            self.Meeples = Meeples
    
    def CloneFarm(self):
        Clone = Farm()
        Clone.ID = self.ID
        Clone.Pointer = self.Pointer
        Clone.CityIndexes = set([x for x in self.CityIndexes])
        Clone.Meeples = [x for x in self.Meeples]
        return Clone
    
    def Update(self, NewCityIndexes = [], MeeplesAdded = [0,0]):
        for CityIndex in NewCityIndexes:
            self.CityIndexes.add(CityIndex)
        self.Meeples[1] += MeeplesAdded[1]
        self.Meeples[0] += MeeplesAdded[0]
        
    def __repr__(self):
        String = "Farm ID"+str(self.ID)+"Ptr"+str(self.Pointer)+"CI"+str(self.CityIndexes)+"Mps" + str(self.Meeples[0])+","+ str(self.Meeples[1])
        return String
    

    
class Road:
    def __init__(self,ID = None, Value=None, Openings=None, Meeples=[0,0]):
        if ID is not None:
            self.ID = ID
            self.Pointer = ID
            self.Openings = Openings
            self.Value = Value
            self.Meeples = Meeples
    
    def CloneRoad(self):
        Clone = Road()
        Clone.ID = self.ID
        Clone.Pointer = self.Pointer
        Clone.Openings = self.Openings
        Clone.Value = self.Value
        Clone.Meeples = [x for x in self.Meeples]
        return Clone
    
    def Update(self, OpeningsChange = 0, ValueAdded = 0, MeeplesAdded = [0,0]):
        self.Openings += OpeningsChange
        self.Value += ValueAdded
        self.Meeples[1] += MeeplesAdded[1]
        self.Meeples[0] += MeeplesAdded[0]
        
    def __repr__(self):
        String = "Road ID"+str(self.ID)+"Ptr"+str(self.Pointer)+"V"+str(self.Value)+"Ops"+str(self.Openings)+"Mps" + str(self.Meeples[0])+","+ str(self.Meeples[1])
        return String