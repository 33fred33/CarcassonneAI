#!/usr/bin/env python
"""
Created on Fri Feb  8 10:58:14 2019

@author: user
"""

import random as rd
import time
import sys
import csv  


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
        String = "City ID"+str(self.ID)+"Ptr"+str(self.Pointer)+"V"+str(self.Value)+"Ops"+str(self.Openings)+"Mps" + str(self.Meeples[0])+","+ str(self.Meeples[1])+"Clsd?",str(self.ClosedFlag)
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

class Cloister:
    def __init__(self, ID = None, Owner = None):
        if ID is not None:
            self.ID = ID
            self.Owner = Owner
            self.Value = 1
    
    def CloneCloister(self):
        Clone = Cloister()
        Clone.ID = self.ID
        Clone.Owner = self.Owner
        Clone.Value = self.Value
        return Clone
    
    def __repr__(self):
        String = "Cloister ID"+str(self.ID)+"Value"+str(self.Value)+"Owner"+str(self.Owner)
        return String
    
class Tile:
    def __init__(self,TileIndex,RunInit = "True"):              
        self.TileIndex = TileIndex
        self.TileCitiesIndex = [None,None,None,None]
        self.TileRoadsIndex = [None,None,None,None]
        self.TileFarmsIndex = [[None,None,None],[None,None,None],[None,None,None],[None,None,None]]
        self.Rotation = 0        
        if RunInit:
            #Tiles DB
            if TileIndex == 0:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,False,[0]
                self.CityValues = [2]
                self.CityOpenings = [[0,1,2,3]]                
                self.Properties = ["C","C","C","C"]
                self.AvailableMeepleLocs = {("C",0):(0,1)}
            elif TileIndex == 1:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[0,1,2]]
                self.FarmOpenings = [[(3,1)]] #(Side,Line)
                self.FarmRelatedCityIndex = [[1]] #Index in TileCitiesIndex variable in this tile
                self.Properties = ["C","C","C","G"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("G",0):(3,1)}
            elif TileIndex == 2:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [2]
                self.CityOpenings = [[0,1,2]]
                self.FarmOpenings = [[(3,1)]]
                self.FarmRelatedCityIndex = [[1]]
                self.Properties = ["C","C","C","G"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("G",0):(3,1)}
            elif TileIndex == 3:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[0,1,2]]
                self.RoadOpenings = [[3]]
                self.FarmOpenings = [[(3,0)],[(3,2)]]
                self.FarmRelatedCityIndex = [[1],[1]]
                self.Properties = ["C","C","C","R"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("R",0):(3,1),("G",0):(3,0),("G",1):(3,2)}
            elif TileIndex == 4:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [2]
                self.CityOpenings = [[0,1,2]]
                self.RoadOpenings = [[3]]
                self.FarmOpenings = [[(3,0)],[(3,2)]]
                self.FarmRelatedCityIndex = [[1],[1]]
                self.Properties = ["C","C","C","R"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("R",0):(3,1),("G",0):(3,0),("G",1):(3,2)}
            elif TileIndex == 5:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1,2]]
                self.FarmOpenings = [[(0,1),(3,1)]]
                self.FarmRelatedCityIndex = [[1]]
                self.Properties = ["G","C","C","G"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("G",0):(3,1)}
            elif TileIndex == 6:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [1,1]
                self.CityOpenings = [[1],[2]]
                self.FarmOpenings = [[(0,1),(3,1)]]
                self.FarmRelatedCityIndex = [[1,2]]
                self.Properties = ["G","C","C","G"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("C",1):(2,1),("G",0):(3,1)}
            elif TileIndex == 7:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [2]
                self.CityOpenings = [[1,2]]
                self.FarmOpenings = [[(0,1),(3,1)]]
                self.FarmRelatedCityIndex = [[1]]
                self.Properties = ["G","C","C","G"] 
                self.AvailableMeepleLocs = {("C",0):(1,1),("G",0):(3,1)}
            elif TileIndex == 8:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1,2]]
                self.RoadOpenings = [[0,3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(3,0)]]
                self.FarmRelatedCityIndex = [[],[1]]
                self.Properties = ["R","C","C","R"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(0,1),("G",0):(3,2),("G",1):(0,2)}
            elif TileIndex == 9:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [2]
                self.CityOpenings = [[1,2]]
                self.RoadOpenings = [[0,3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(3,0)]]
                self.FarmRelatedCityIndex = [[],[1]]
                self.Properties = ["R","C","C","R"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(0,1),("G",0):(3,2),("G",1):(0,2)}
            elif TileIndex == 10:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90]
                self.CityValues = [1]
                self.CityOpenings = [[0,2]]
                self.FarmOpenings = [[(1,1)],[(3,1)]]
                self.FarmRelatedCityIndex = [[0],[0]]
                self.Properties = ["C","G","C","G"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("G",0):(1,1),("G",1):(3,1)}
            elif TileIndex == 11:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90]
                self.CityValues = [1,1]
                self.CityOpenings = [[1],[3]]
                self.FarmOpenings = [[(0,1),(2,1)]]
                self.FarmRelatedCityIndex = [[1,3]]
                self.Properties = ["G","C","G","C"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("C",1):(3,1),("G",0):(0,1)}
            elif TileIndex == 12:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90]
                self.CityValues = [2]
                self.CityOpenings = [[0,2]]
                self.FarmOpenings = [[(1,1)],[(3,1)]]
                self.FarmRelatedCityIndex = [[0],[0]]
                self.Properties = ["C","G","C","G"]
                self.AvailableMeepleLocs = {("C",0):(0,1),("G",0):(1,1),("G",1):(3,1)}
            elif TileIndex == 13:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,False,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1]]
                self.FarmOpenings = [[(0,1),(2,1),(3,1)]]
                self.FarmRelatedCityIndex = [[1]]
                self.Properties = ["G","C","G","G"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("G",0):(3,1)}
            elif TileIndex == 14:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1]]
                self.RoadOpenings = [[0,3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(2,1),(3,0)]]
                self.FarmRelatedCityIndex = [[],[1]]
                self.Properties = ["R","C","G","R"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(0,1),("G",0):(3,2),("G",1):(2,1)}
            elif TileIndex == 15:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = True,False,True,True,[0,90,180,270]
                self.RoadOpenings = [[3]]
                self.FarmOpenings = [[(0,1),(1,1),(2,1),(3,0),(3,2)]]
                self.FarmRelatedCityIndex = [[]]
                self.Properties = ["G","G","G","R"]
                self.AvailableMeepleLocs = {("R",0):(3,1),("Cloister",0):(0,4),("G",0):(0,2)}
            elif TileIndex == 16:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1]]
                self.RoadOpenings = [[0,2]]
                self.FarmOpenings = [[(0,0),(2,2),(3,1)],[(0,2),(2,0)]]
                self.FarmRelatedCityIndex = [[],[1]]
                self.Properties = ["R","C","R","G"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(0,1),("G",0):(3,1),("G",1):(0,2)}
            elif TileIndex == 17:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1]]
                self.RoadOpenings = [[2,3]]
                self.FarmOpenings = [[(0,1),(2,0),(3,2)],[(2,2),(3,0)]]
                self.FarmRelatedCityIndex = [[1],[]]
                self.Properties = ["G","C","R","R"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(2,1),("G",0):(0,1),("G",1):(2,2)}
            elif TileIndex == 18:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,True,True,True,[0,90,180,270]
                self.CityValues = [1]
                self.CityOpenings = [[1]]
                self.RoadOpenings = [[0],[2],[3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(2,0)],[(2,2),(3,0)]]
                self.FarmRelatedCityIndex = [[],[1],[]]
                self.Properties = ["R","C","R","R"]
                self.AvailableMeepleLocs = {("C",0):(1,1),("R",0):(0,1),("R",1):(2,1),("R",2):(3,1),("G",0):(3,2),("G",1):(0,2),("G",2):(2,2)}
            elif TileIndex == 19:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,False,True,True,[0,90,180,270]
                self.RoadOpenings = [[0],[2],[3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(1,1),(2,0)],[(2,2),(3,0)]]
                self.FarmRelatedCityIndex = [[],[],[]]
                self.Properties = ["R","G","R","R"]
                self.AvailableMeepleLocs = {("R",0):(0,1),("R",1):(2,1),("R",2):(3,1),("G",0):(3,2),("G",1):(0,2),("G",2):(2,2)}
            elif TileIndex == 20:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = True,False,False,True,[0]
                self.FarmOpenings = [[(0,1),(1,1),(2,1),(3,1)]]
                self.FarmRelatedCityIndex = [[]]
                self.Properties = ["G","G","G","G"]
                self.AvailableMeepleLocs = {("Cloister",0):(0,4),("G",0):(0,2)}
            elif TileIndex == 21:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,False,True,True,[0,90,180,270]
                self.RoadOpenings = [[0,3]]
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(1,1),(2,1),(3,0)]]
                self.FarmRelatedCityIndex = [[],[]]
                self.Properties = ["R","G","G","R"]
                self.AvailableMeepleLocs = {("R",0):(0,1),("G",0):(3,2),("G",1):(2,1)}
            elif TileIndex == 22:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,False,True,True,[0,90]
                self.RoadOpenings = [[0,2]]
                self.FarmOpenings = [[(0,0),(2,2),(3,1)],[(0,2),(1,1),(2,0)]]
                self.FarmRelatedCityIndex = [[],[]]
                self.Properties = ["R","G","R","G"]
                self.AvailableMeepleLocs = {("R",0):(0,1),("G",0):(3,2),("G",1):(0,2)}
            elif TileIndex == 23:
                self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations = False,False,True,True,[0]
                self.RoadOpenings = [[0],[1],[2],[3]]  
                self.FarmOpenings = [[(0,0),(3,2)],[(0,2),(1,0)],[(1,2),(2,0)],[(2,2),(3,0)]]
                self.FarmRelatedCityIndex = [[],[],[],[]]
                self.Properties = ["R","R","R","R"]
                self.AvailableMeepleLocs = {("R",0):(0,1),("R",1):(1,1),("R",2):(2,1),("R",3):(3,1),("G",0):(3,2),("G",1):(0,2),("G",2):(1,2),("G",3):(2,2)}
        
    def CloneTile(self):
        Clone = Tile(self.TileIndex, RunInit = False)
        Clone.TileCitiesIndex = [x for x in self.TileCitiesIndex]
        Clone.TileRoadsIndex = [x for x in self.TileRoadsIndex]
        Clone.TileFarmsIndex = [[y for y in x] for x in self.TileFarmsIndex]
        Clone.HasCloister,Clone.HasCities,Clone.HasRoads,Clone.HasFarms,Clone.AvailableRotations = self.HasCloister,self.HasCities,self.HasRoads,self.HasFarms,self.AvailableRotations
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

    def PlayMe(self,NewRotation):
        if NewRotation != self.Rotation:
            NeededRotation = NewRotation - self.Rotation
            self.Rotation = NewRotation
            if NeededRotation < 0:
                NeededRotation += 360
            if NeededRotation == 90:
                NewOrder = [3,0,1,2]
                SideChange = 1
            elif NeededRotation == 180:
                NewOrder = [2,3,0,1]
                SideChange = 2
            elif NeededRotation == 270:
                NewOrder = [1,2,3,0]
                SideChange = 3
            self.Properties = [self.Properties[i] for i in NewOrder]
            self.AvailableMeepleLocs = {k:tuple([v[0]+SideChange if v[0]+SideChange < 4 else v[0]+SideChange-4,v[1]]) for k,v in self.AvailableMeepleLocs.items()}
            if self.HasCities:
                self.TileCitiesIndex = [self.TileCitiesIndex[i] for i in NewOrder]
                self.CityOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.CityOpenings]
            if self.HasRoads:
                self.TileRoadsIndex = [self.TileRoadsIndex[i] for i in NewOrder]
                self.RoadOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.RoadOpenings]
            if self.HasFarms:
                self.TileFarmsIndex =  [self.TileFarmsIndex[i] for i in NewOrder]
                self.FarmRelatedCityIndex =  [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in self.FarmRelatedCityIndex]
                self.FarmOpenings =  [[(x+SideChange,y) if x+SideChange < 4 else (x+SideChange-4,y) for (x,y) in k] for k in self.FarmOpenings]

    def __repr__(self):
        String = str(self.TileIndex) + str(self.Properties[0])+ str(self.Properties[1])+ str(self.Properties[2])+ str(self.Properties[3])+str(self.Rotation)+" TCI"+str(self.TileCitiesIndex)+" TRI"+str(self.TileRoadsIndex)+" TFI"+str(self.TileFarmsIndex)
        return String


class CarcassonneState:
    def __init__(self,RunInit = True):
        #rd.seed(1)
        #Never changing:
        self.MatchingSide = [2,3,0,1]
        self.MatchingLine = [2,1,0]
        #Initialialize variables        
        self.GameRecord = []
        self.Board = {} #Change to list
        self.BoardCities = {}
        self.BoardRoads = {}
        self.BoardCloisters = {}
        self.BoardFarms = {}
        self.CloisterOpenings = {}
        self.AvailableSpots = set()
        self.AvailableMoves = []
        self.Meeples = [7,7]
        
        if RunInit: 
            self.Winner = None
            self.Scores = [0,0,0,0] #P1, P2, P1 virtual, P2 virtual
            self.PlayerTurn = 1
            self.Terminal = False
            self.TileQuantities = [1,3,1,1,2,3,2,2,2,3,1,3,2,5,3,2,4,3,3,4,4,9,8,1]
            #self.TileQuantities = [0,0,3,0,0,0,0,3,0,0,0,0,3,0,3,0,4,0,0,0,0,2,0,0]
            self.TotalTiles = sum(self.TileQuantities)
            self.UniqueTilesCount = len(self.TileQuantities)
            self.AvailableTiles = [[Tile(i) for _ in range(self.TileQuantities[i])] for i in range(self.UniqueTilesCount)]
            self.TileIndexList = []
            for i in range(self.UniqueTilesCount):
                self.TileIndexList += [i for _ in range(self.TileQuantities[i])]
            self.MakeMove([16, 0, 0, 0, None])                
    
    def CloneState(self):
        Clone = CarcassonneState(RunInit = False)
        #Never changing variables are ignored
        Clone.GameRecord = [x for x in self.GameRecord]
        Clone.Board = {k:v.CloneTile() for k,v in self.Board.items()}
        Clone.BoardCities = {k:v.CloneCity() for k,v in self.BoardCities.items()}
        Clone.BoardRoads = {k:v.CloneRoad() for k,v in self.BoardRoads.items()}
        Clone.BoardCloisters = {k:v.CloneCloister() for k,v in self.BoardCloisters.items()}
        Clone.BoardFarms = {k:v.CloneFarm() for k,v in self.BoardFarms.items()}
        Clone.CloisterOpenings = {k:[x for x in v] for k,v in self.CloisterOpenings.items()}
        Clone.AvailableSpots = set([x for x in self.AvailableSpots])
        Clone.AvailableMoves = [x for x in self.AvailableMoves] #Not needed?
        Clone.Meeples = [x for x in self.Meeples]
        Clone.Winner = self.Winner
        
        Clone.Scores = [x for x in self.Scores]
        Clone.PlayerTurn = self.PlayerTurn
        Clone.Terminal = self.Terminal        
        Clone.TileQuantities = [x for x in self.TileQuantities]
        Clone.TotalTiles = self.TotalTiles
        Clone.UniqueTilesCount = self.UniqueTilesCount       
        Clone.AvailableTiles = [[x.CloneTile() for x in r] for r in self.AvailableTiles]    
        Clone.TileIndexList = [x for x in self.TileIndexList]
        return Clone
    
    def MakeMove(self,Move = None, SpeedMode = False):   
        if ShowLogs: print("Making Move:",Move)
        PlayingTileIndex, X, Y, Rotation, MeepleKey = Move[0], Move[1], Move[2], Move[3], Move[4]
        self.AvailableSpots.discard((X,Y))
        PlayingTile = self.AvailableTiles[PlayingTileIndex].pop(0)
        self.TileQuantities[PlayingTileIndex] -= 1
        self.TotalTiles -= 1
        self.TileIndexList.remove(PlayingTileIndex) 
        #Surroundings analysis
        Surroundings = [None,None,None,None]
        SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]
        if not SurroundingSpots[0] in self.Board:
            self.AvailableSpots.add(SurroundingSpots[0])
        else:
            Surroundings[0] = self.Board[SurroundingSpots[0]]
        if not SurroundingSpots[1] in self.Board:
            self.AvailableSpots.add(SurroundingSpots[1])
        else:
            Surroundings[1] = self.Board[SurroundingSpots[1]]
        if not SurroundingSpots[2] in self.Board:
            self.AvailableSpots.add(SurroundingSpots[2])
        else:
            Surroundings[2] = self.Board[SurroundingSpots[2]]
        if not SurroundingSpots[3] in self.Board:
            self.AvailableSpots.add(SurroundingSpots[3])
        else:
            Surroundings[3] = self.Board[SurroundingSpots[3]]
        PlayingTile.PlayMe(Rotation)
        self.Board[(X,Y)] = PlayingTile
        
        if MeepleKey is None:
            MeepleLoc = [0,0]
            MeepleUpdate = [0,0]
        else:
            MeepleLoc = PlayingTile.AvailableMeepleLocs[MeepleKey]
            if self.PlayerTurn == 0:
                MeepleUpdate = [1,0]
                self.Meeples[0] -= 1
            else:
                MeepleUpdate = [0,1]
                self.Meeples[1] -= 1
        
        #Cloister completeness check
        if (X,Y) in self.CloisterOpenings:
            for AffectedCloisterIndex in self.CloisterOpenings[(X,Y)]:
                AffectedCloister = self.BoardCloisters[AffectedCloisterIndex]
                AffectedCloister.Value += 1
                if AffectedCloister.Value == 9:
                    self.Meeples[AffectedCloister.Owner] += 1
                    self.Scores[AffectedCloister.Owner] += 9
                    AffectedCloister.Value = 0
            del self.CloisterOpenings[(X,Y)]
        #Cloister logic
        if MeepleKey is not None:
            if MeepleKey[0] == "Cloister":
                CompleteSurroundingSpots = SurroundingSpots + [(X-1,Y-1),(X+1,Y+1),(X+1,Y-1),(X-1,Y+1)]
                NextCloisterID = len(self.BoardCloisters)
                self.BoardCloisters[NextCloisterID] = Cloister(NextCloisterID,self.PlayerTurn)
                AffectedCloister = self.BoardCloisters[NextCloisterID]
                for Spot in CompleteSurroundingSpots:
                    if Spot in self.Board:
                        AffectedCloister.Value += 1
                        if AffectedCloister.Value == 9:
                            self.Meeples[AffectedCloister.Owner] += 1
                            self.Scores[AffectedCloister.Owner] += 9
                            AffectedCloister.Value = 0
                    else:
                        if Spot in self.CloisterOpenings:
                            self.CloisterOpenings[Spot].append(NextCloisterID)
                        else:
                            self.CloisterOpenings[Spot] = [NextCloisterID]

        #Cities update
        if PlayingTile.HasCities:
            ClosingCities = []
            for i in range(len(PlayingTile.CityOpenings)):
                CityOpenings = PlayingTile.CityOpenings[i]
                AddedMeeples = [0,0]
                if MeepleKey is not None:
                    if MeepleKey[0] == "C" and MeepleKey[1] == i:
                        AddedMeeples = MeepleUpdate
                OpeningsQuantity = len(CityOpenings)      
                if OpeningsQuantity == 1:
                    CitySide = CityOpenings[0]
                    if Surroundings[CitySide] is None:
                        NextCityIndex = len(self.BoardCities)
                        self.BoardCities[NextCityIndex] = City(NextCityIndex,1,1,AddedMeeples)
                        PlayingTile.TileCitiesIndex[CitySide] = NextCityIndex
                    else:
                        MatchingCityIndex = Surroundings[CitySide].TileCitiesIndex[self.MatchingSide[CitySide]]
                        while self.BoardCities[MatchingCityIndex].Pointer != self.BoardCities[MatchingCityIndex].ID:                            
                            MatchingCityIndex = self.BoardCities[MatchingCityIndex].Pointer
                        MatchingCity = self.BoardCities[MatchingCityIndex]
                        MatchingCity.Update(-1,1,AddedMeeples)
                        if MatchingCity.Openings == 0:
                            ClosingCities.append(MatchingCityIndex)
                        PlayingTile.TileCitiesIndex[CitySide] = MatchingCityIndex #Added for farms
                else:
                    ConnectedCities = []
                    for CitySide in CityOpenings:
                        if Surroundings[CitySide] is not None:
                            MatchingCityIndex = Surroundings[CitySide].TileCitiesIndex[self.MatchingSide[CitySide]]
                            while self.BoardCities[MatchingCityIndex].Pointer != self.BoardCities[MatchingCityIndex].ID:                            
                                MatchingCityIndex = self.BoardCities[MatchingCityIndex].Pointer
                            ConnectedCities.append([MatchingCityIndex,CitySide])
                    if ConnectedCities == []:
                        NextCityIndex = len(self.BoardCities)
                        self.BoardCities[NextCityIndex] = City(NextCityIndex,PlayingTile.CityValues[i],OpeningsQuantity,AddedMeeples)
                        for CitySide in CityOpenings:
                            PlayingTile.TileCitiesIndex[CitySide] = NextCityIndex
                    else:
                        OpeningsToAdd = OpeningsQuantity - len(ConnectedCities)
                        CombinedCityIndex = ConnectedCities[0][0]
                        AlreadyMatched = False
                        for MatchingCityIndex,CitySide in ConnectedCities:                            
                            if CombinedCityIndex == MatchingCityIndex:
                                if AlreadyMatched:
                                    self.BoardCities[CombinedCityIndex].Update(-1,0,[0,0])
                                else:
                                    self.BoardCities[CombinedCityIndex].Update(OpeningsToAdd-1,PlayingTile.CityValues[i],AddedMeeples)
                                    AlreadyMatched = True
                            else:
                                MatchingCity = self.BoardCities[MatchingCityIndex]
                                MatchingCity.Pointer = CombinedCityIndex
                                self.BoardCities[CombinedCityIndex].Update(MatchingCity.Openings-1,MatchingCity.Value,MatchingCity.Meeples)
                                MatchingCity.Openings = 0
                                MatchingCity.Value = 0
                                MatchingCity.Meeples = [0,0]
                        for CitySide in CityOpenings:
                            PlayingTile.TileCitiesIndex[CitySide] = CombinedCityIndex
                        if self.BoardCities[CombinedCityIndex].Openings == 0:
                            ClosingCities.append(CombinedCityIndex)
            #City closure
            for ClosingCityIndex in ClosingCities:
                ClosingCity = self.BoardCities[ClosingCityIndex]
                ClosingCity.ClosedFlag = True
                if ClosingCity.Meeples[0] == 0 and ClosingCity.Meeples[1] == 0:
                    pass
                elif ClosingCity.Meeples[0] > ClosingCity.Meeples[1]:
                    self.Scores[0] += 2*ClosingCity.Value
                elif ClosingCity.Meeples[0] < ClosingCity.Meeples[1]:
                    self.Scores[1] += 2*ClosingCity.Value
                else:
                    self.Scores[0] += 2*ClosingCity.Value
                    self.Scores[1] += 2*ClosingCity.Value
                ClosingCity.Value = 0
                self.Meeples[0] += ClosingCity.Meeples[0]
                self.Meeples[1] += ClosingCity.Meeples[1]
                
        #Roads update
        if PlayingTile.HasRoads:
            ClosingRoads = []
            for i in range(len(PlayingTile.RoadOpenings)):
                RoadOpenings = PlayingTile.RoadOpenings[i]
                AddedMeeples = [0,0]
                if MeepleKey is not None:
                    if MeepleKey[0] == "R" and MeepleKey[1] == i:
                        AddedMeeples = MeepleUpdate
                OpeningsQuantity = len(RoadOpenings)      
                if OpeningsQuantity == 1:
                    RoadSide = RoadOpenings[0]
                    if Surroundings[RoadSide] is None:
                        NextRoadIndex = len(self.BoardRoads)
                        self.BoardRoads[NextRoadIndex] = Road(NextRoadIndex,1,1,AddedMeeples)
                        PlayingTile.TileRoadsIndex[RoadSide] = NextRoadIndex
                    else:
                        MatchingRoadIndex = Surroundings[RoadSide].TileRoadsIndex[self.MatchingSide[RoadSide]]
                        while self.BoardRoads[MatchingRoadIndex].Pointer != self.BoardRoads[MatchingRoadIndex].ID:                            
                            MatchingRoadIndex = self.BoardRoads[MatchingRoadIndex].Pointer
                        MatchingRoad = self.BoardRoads[MatchingRoadIndex]
                        MatchingRoad.Update(-1,1,AddedMeeples)
                        if MatchingRoad.Openings == 0:
                            ClosingRoads.append(MatchingRoadIndex)                
                else:
                    ConnectedRoads = []
                    for RoadSide in RoadOpenings:
                        if Surroundings[RoadSide] is not None:
                            MatchingRoadIndex = Surroundings[RoadSide].TileRoadsIndex[self.MatchingSide[RoadSide]]
                            while self.BoardRoads[MatchingRoadIndex].Pointer != self.BoardRoads[MatchingRoadIndex].ID:                            
                                MatchingRoadIndex = self.BoardRoads[MatchingRoadIndex].Pointer
                            ConnectedRoads.append([MatchingRoadIndex,RoadSide])
                    if ConnectedRoads == []:
                        NextRoadIndex = len(self.BoardRoads)
                        self.BoardRoads[NextRoadIndex] = Road(NextRoadIndex,1,OpeningsQuantity,AddedMeeples)
                        for RoadSide in RoadOpenings:
                            PlayingTile.TileRoadsIndex[RoadSide] = NextRoadIndex
                    else:
                        OpeningsToAdd = OpeningsQuantity - len(ConnectedRoads)
                        CombinedRoadIndex = ConnectedRoads[0][0]
                        AlreadyMatched = False
                        for MatchingRoadIndex,RoadSide in ConnectedRoads:                            
                            if CombinedRoadIndex == MatchingRoadIndex:
                                if AlreadyMatched:
                                    self.BoardRoads[CombinedRoadIndex].Update(-1,0,[0,0])
                                else:
                                    self.BoardRoads[CombinedRoadIndex].Update(OpeningsToAdd-1,1,AddedMeeples)
                                    AlreadyMatched = True
                            else:
                                MatchingRoad = self.BoardRoads[MatchingRoadIndex]
                                MatchingRoad.Pointer = CombinedRoadIndex
                                self.BoardRoads[CombinedRoadIndex].Update(MatchingRoad.Openings-1,MatchingRoad.Value,MatchingRoad.Meeples)
                                MatchingRoad.Openings = 0
                                MatchingRoad.Value = 0
                                MatchingRoad.Meeples = [0,0]
                        for RoadSide in RoadOpenings:
                            PlayingTile.TileRoadsIndex[RoadSide] = CombinedRoadIndex
                        if self.BoardRoads[CombinedRoadIndex].Openings == 0:
                            ClosingRoads.append(CombinedRoadIndex)
            #Road closure
            for ClosingRoadIndex in ClosingRoads:
                ClosingRoad = self.BoardRoads[ClosingRoadIndex]
                if ClosingRoad.Meeples[0] == 0 and ClosingRoad.Meeples[1] == 0:
                    pass
                elif ClosingRoad.Meeples[0] > ClosingRoad.Meeples[1]:
                    self.Scores[0] += ClosingRoad.Value
                elif ClosingRoad.Meeples[0] < ClosingRoad.Meeples[1]:
                    self.Scores[1] += ClosingRoad.Value
                else:
                    self.Scores[0] += ClosingRoad.Value
                    self.Scores[1] += ClosingRoad.Value
                ClosingRoad.Value = 0
                self.Meeples[0] += ClosingRoad.Meeples[0]
                self.Meeples[1] += ClosingRoad.Meeples[1]
                
        #Farms update
        if PlayingTile.HasFarms:
            for i in range(len(PlayingTile.FarmOpenings)):
                FarmOpenings = PlayingTile.FarmOpenings[i]
                AddedMeeples = [0,0]
                if MeepleKey is not None:
                    if MeepleKey[0] == "G" and MeepleKey[1] == i:
                        AddedMeeples = MeepleUpdate
                OpeningsQuantity = len(FarmOpenings)      
                if OpeningsQuantity == 1:
                    FarmSide = FarmOpenings[0][0]
                    FarmLine = FarmOpenings[0][1]
                    if Surroundings[FarmSide] is None:
                        NextFarmIndex = len(self.BoardFarms)
                        self.BoardFarms[NextFarmIndex] = Farm(NextFarmIndex,AddedMeeples) #here
                        self.BoardFarms[NextFarmIndex].Update([PlayingTile.TileCitiesIndex[FRCI] for FRCI in PlayingTile.FarmRelatedCityIndex[i]],[0,0])
                        PlayingTile.TileFarmsIndex[FarmSide][FarmLine] = NextFarmIndex
                    else:
                        MatchingFarmIndex = Surroundings[FarmSide].TileFarmsIndex[self.MatchingSide[FarmSide]][self.MatchingLine[FarmLine]]
                        while self.BoardFarms[MatchingFarmIndex].Pointer != self.BoardFarms[MatchingFarmIndex].ID:                            
                            MatchingFarmIndex = self.BoardFarms[MatchingFarmIndex].Pointer
                        MatchingFarm = self.BoardFarms[MatchingFarmIndex]
                        MatchingFarm.Update([PlayingTile.TileCitiesIndex[FRCI] for FRCI in PlayingTile.FarmRelatedCityIndex[i]],AddedMeeples)              
                else:
                    ConnectedFarms = []
                    for (FarmSide,FarmLine) in FarmOpenings:
                        if Surroundings[FarmSide] is not None:
                            #if ShowLogs: print("FarmSide",FarmSide,"FarmLine",FarmLine,"Surroundings[FarmSide]",Surroundings[FarmSide])
                            MatchingFarmIndex = Surroundings[FarmSide].TileFarmsIndex[self.MatchingSide[FarmSide]][self.MatchingLine[FarmLine]]
                            while self.BoardFarms[MatchingFarmIndex].Pointer != self.BoardFarms[MatchingFarmIndex].ID:                            
                                MatchingFarmIndex = self.BoardFarms[MatchingFarmIndex].Pointer
                            ConnectedFarms.append([MatchingFarmIndex,FarmSide,FarmLine])
                    if ConnectedFarms == []:
                        NextFarmIndex = len(self.BoardFarms)
                        self.BoardFarms[NextFarmIndex] = Farm(NextFarmIndex,AddedMeeples)
                        #print(PlayingTile.FarmRelatedCityIndex[i],PlayingTile.TileCitiesIndex)
                        self.BoardFarms[NextFarmIndex].Update([PlayingTile.TileCitiesIndex[FRCI] for FRCI in PlayingTile.FarmRelatedCityIndex[i]],[0,0])
                        for (FarmSide,FarmLine) in FarmOpenings:
                            PlayingTile.TileFarmsIndex[FarmSide][FarmLine] = NextFarmIndex
                    else:
                        CombinedFarmIndex = ConnectedFarms[0][0]
                        AlreadyMatched = False
                        for MatchingFarmIndex,FarmSide,FarmLine in ConnectedFarms:                            
                            if CombinedFarmIndex == MatchingFarmIndex:
                                if not AlreadyMatched: 
                                    self.BoardFarms[CombinedFarmIndex].Update([PlayingTile.TileCitiesIndex[FRCI] for FRCI in PlayingTile.FarmRelatedCityIndex[i]],AddedMeeples)
                                    AlreadyMatched = True
                            else:
                                MatchingFarm = self.BoardFarms[MatchingFarmIndex]
                                MatchingFarm.Pointer = CombinedFarmIndex
                                self.BoardFarms[CombinedFarmIndex].Update(MatchingFarm.CityIndexes,MatchingFarm.Meeples)
                                MatchingFarm.Meeples = [0,0]
                        for FarmSide,FarmLine in FarmOpenings:
                            PlayingTile.TileFarmsIndex[FarmSide][FarmLine] = CombinedFarmIndex
        #print("BoardFarms:" , self.BoardFarms)
                
        #Virtual Scores calculation
        if not SpeedMode:
            self.Scores[2] = self.Scores[0]
            self.Scores[3] = self.Scores[1]
            self.Scores[2] += sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])        
            self.Scores[3] += sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])        
            self.Scores[2] += sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
            self.Scores[3] += sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])
            self.Scores[2] += sum([v.Value for k,v in self.BoardCloisters.items() if v.Owner == 0])
            self.Scores[3] += sum([v.Value for k,v in self.BoardCloisters.items() if v.Owner == 1])
            self.Scores[2] += 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
            self.Scores[3] += 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])
        #End game test
        if self.TotalTiles == 0:
            self.EndGameRoutine()  
        #Game record update
        if len(self.GameRecord) > 0: self.GameRecord[-1][4] = PlayingTileIndex            
        self.GameRecord.append([PlayingTileIndex
                                ,X
                                ,Y
                                ,Rotation
                                ,0
                                ,self.Meeples[0]
                                ,self.Meeples[1]
                                ,self.Scores[0]
                                ,self.Scores[1]
                                ,self.PlayerTurn + 1
                                ,MeepleLoc[0]
                                ,MeepleLoc[1]
                                ,self.Scores[2]
                                ,self.Scores[3]                        
                                ])
        #Turn end routine
        if ShowLogs: self.SaveGame()
        self.PlayerTurn = 1 - self.PlayerTurn
    
    def EndGameRoutine(self):
        self.Terminal = True
        self.Scores[2] = self.Scores[0]
        self.Scores[3] = self.Scores[1]
        self.Scores[2] += sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])        
        self.Scores[3] += sum([v.Value for k,v in self.BoardCities.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])        
        self.Scores[2] += sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
        self.Scores[3] += sum([v.Value for k,v in self.BoardRoads.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])
        self.Scores[2] += sum([v.Value for k,v in self.BoardCloisters.items() if v.Owner == 0])
        self.Scores[3] += sum([v.Value for k,v in self.BoardCloisters.items() if v.Owner == 1])
        self.Scores[2] += 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[0] >= v.Meeples[1] and v.Meeples[0] > 0])
        self.Scores[3] += 3*sum([len([x for x in v.CityIndexes if self.BoardCities[x].ClosedFlag]) for k,v in self.BoardFarms.items() if v.Pointer == v.ID and v.Meeples[1] >= v.Meeples[0] and v.Meeples[1] > 0])

        self.Scores[0] = self.Scores[2]
        self.Scores[1] = self.Scores[3]
        if self.Scores[0] > self.Scores[1]:
            self.Winner = 0 #P1 wins
        elif self.Scores[1] > self.Scores[0]:
            self.Winner = 1 #P2 wins
        else:
            self.Winner = 2 #Draw
        if ShowLogs: print("Game ended")       
               
    #Utility functions
    def IsMovePossible(self,Move):
        TileIndex, X, Y, Rotation = Move[0], Move[1], Move[2], Move[3]
        if TileIndex in self.TileIndexList and (X,Y) not in self.Board:
            Tile = self.AvailableTiles[TileIndex][-1]
            SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]
            if Rotation == 0:
                TileLeft,TileUp,TileRight,TileDown = 0,1,2,3
            elif Rotation == 90:
                TileLeft,TileUp,TileRight,TileDown = 3,0,1,2
            elif Rotation == 180:
                TileLeft,TileUp,TileRight,TileDown = 2,3,0,1
            elif Rotation == 270:
                TileLeft,TileUp,TileRight,TileDown = 1,2,3,0
            TestingTile = self.Board.get(SurroundingSpots[0])
            if TestingTile is not None:
                if TestingTile.Properties[2] != Tile.Properties[TileLeft]:
                    return False
            TestingTile = self.Board.get(SurroundingSpots[1])
            if TestingTile is not None:
                if TestingTile.Properties[3] != Tile.Properties[TileUp]:
                    return False
            TestingTile = self.Board.get(SurroundingSpots[2])
            if TestingTile is not None:
                if TestingTile.Properties[0] != Tile.Properties[TileRight]:
                    return False
            TestingTile = self.Board.get(SurroundingSpots[3])
            if TestingTile is not None:
                if TestingTile.Properties[1] != Tile.Properties[TileDown]:
                    return False
            return True
        else: return False
    
    def GetChanceOptions(self, GiveProbability = False):
        Tiles = []
        Probabilities = []
        NewList = [x for x in self.TileIndexList]
        for TileIndex in set(self.TileIndexList):
            if self.GetAvailableMoves(TileIndex,TilesOnly = True) == []: #too costly
                NewList = [x for x in NewList if x != TileIndex]
            else:
                Tiles.append(TileIndex)
        if NewList != []:
            for TileIndex in Tiles:
                if GiveProbability:
                    OccurrenciesCount = len([x for x in NewList if x == TileIndex])
                    Probability = OccurrenciesCount*1.0 / len(NewList)
                    #print(Probability, OccurrenciesCount, len(NewList))
                    Probabilities.append(Probability)  
        else:
            self.EndGameRoutine()
            #print("!!!")
        #print(Probabilities)
        return Tiles, Probabilities 
    
    def GetRandomChanceOption(self):
        TileIndex = rd.choice(self.TileIndexList)
        #Moves = self.GetAvailableMoves(TileIndex,TilesOnly = True)
        Moves = self.GetRandomMove(TileIndex)
        if Moves == []:
            TileArray = [x for x in self.TileIndexList]
            while Moves == []:
                TileArray = [x for x in TileArray if x!=TileIndex]
                if len(TileArray) > 0:
                    TileIndex =  rd.choice(TileArray)
                    #Moves = self.GetAvailableMoves(TileIndex,TilesOnly = True)
                    Moves = self.GetRandomMove(TileIndex)
                else:
                    self.EndGameRoutine()
                    TileIndex = None
                    #print("!!")
                    break
        return TileIndex
            
    def RandomGameToEnd(self, MyTile = None, RandomGames = 1, Output = "WinnerCount" ): #MyTile is a given tile (in case you already have one)
        WinnerCount = [0,0,0]
        for i in range(RandomGames):
            FromState = self.CloneState()
            while not FromState.Terminal:
                Move = FromState.GetRandomMove()
                if not Move == []:
                    FromState.MakeMove(Move, SpeedMode = True)
            #FromState.SaveGame()
            if Output ==  "WinnerCount":
                WinnerCount[FromState.Winner] += 1
            elif Output == "Difference":
                Diff = FromState.Scores[2] - FromState.Scores[3]
                if Diff > 0:
                    WinnerCount[0] += Diff
                else:
                    WinnerCount[1] -= Diff
            elif Output == "Scores":
                WinnerCount[0] += FromState.Scores[0]
                WinnerCount[1] += FromState.Scores[1]
        return WinnerCount
    
    def RAVERandomGameToEnd(self, MyTile = None, RandomGames = 1, Output = "WinnerCount", RAVEMoves = []): #RAVE whole
        #print("Turn",str(len(self.GameRecord)-1)," PlayerTurn",self.PlayerTurn)
        WinnerCount = [0,0,0]
        for i in range(RandomGames):
            FromState = self.CloneState()
            MoveList = []#RAVE
            MoveList.append([])#RAVE
            MoveList.append([])#RAVE
            while not FromState.Terminal:
                Move = FromState.GetRandomMove()
                if not Move == []:
                    MoveList[FromState.PlayerTurn].append(Move) #RAVE
                    FromState.MakeMove(Move, SpeedMode = True)
            #FromState.SaveGame()
            if Output ==  "WinnerCount":
                WinnerCount[FromState.Winner] += 1
            elif Output == "Difference":
                Diff = FromState.Scores[2] - FromState.Scores[3]
                if Diff > 0:
                    WinnerCount[0] += Diff
                else:
                    WinnerCount[1] -= Diff
                DumbSolution = [Diff,-Diff]
                #print("GameWinnerCount",WinnerCount)
                #print("Scores",FromState.Scores[0],FromState.Scores[1],FromState.Scores[2],FromState.Scores[3])
                for iPlayer in range(2):
                    for iMove in MoveList[iPlayer]:
                        #if str(iMove[:-1]) in RAVEMoves[iPlayer]:
                        if str(iMove) in RAVEMoves[iPlayer]:
                            #print("RAVE Match! Scores",FromState.Scores[2],FromState.Scores[3],"RAVEReward",DumbSolution[iPlayer])
                            #RAVEMoves[iPlayer][str(iMove[:-1])][0] += DumbSolution[iPlayer]
                            #RAVEMoves[iPlayer][str(iMove[:-1])][1] += 1
                            RAVEMoves[iPlayer][str(iMove)][0] += DumbSolution[iPlayer]
                            RAVEMoves[iPlayer][str(iMove)][1] += 1
                            #print("RAVEMoves",RAVEMoves)        
            elif Output == "Scores":
                WinnerCount[0] += FromState.Scores[0]
                WinnerCount[1] += FromState.Scores[1]
            
        #print("WinnerCount",WinnerCount)
        #print("RAVEMoves",RAVEMoves)
        return WinnerCount, RAVEMoves
    
    def GetRandomMove(self, TileIndex = None):
        TriedTiles = []
        TempAvailableMoves = []
        Looping = False
        while TempAvailableMoves == []:
            
            if TileIndex is None or Looping:
                Looping = True
                TilesLeftToChoose = [x for x in self.TileIndexList if x not in TriedTiles]
                #print("TilesLeftToChoose", TilesLeftToChoose)
                if TilesLeftToChoose == []:
                    self.EndGameRoutine()
                    return []
                else:
                    TileIndex = rd.choice(TilesLeftToChoose)                    
            TriedTiles.append(TileIndex)
            EvaluatedTile = self.AvailableTiles[TileIndex][0]
            RdSpots = [x for x in self.AvailableSpots]
            rd.shuffle(RdSpots)
            RdRotation = [x for x in EvaluatedTile.AvailableRotations]
            rd.shuffle(RdRotation)
            #print([x for x in EvaluatedTile.AvailableRotations], RdRotation)
            IsTileFitting = False
            
            for (X,Y) in RdSpots:
                SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]
                for Rotation in RdRotation:                
                    if Rotation == 0:
                        SideChange = 0
                        TileLeft,TileUp,TileRight,TileDown = 0,1,2,3
                    elif Rotation == 90:
                        SideChange = 1
                        TileLeft,TileUp,TileRight,TileDown = 3,0,1,2
                    elif Rotation == 180:
                        SideChange = 2
                        TileLeft,TileUp,TileRight,TileDown = 2,3,0,1
                    elif Rotation == 270:
                        SideChange = 3
                        TileLeft,TileUp,TileRight,TileDown = 1,2,3,0
                    while True:
                        TestingTile = self.Board.get(SurroundingSpots[0])
                        if TestingTile is not None:
                            if TestingTile.Properties[2] != EvaluatedTile.Properties[TileLeft]:
                                IsTileFitting = False
                                break
                        TestingTile = self.Board.get(SurroundingSpots[1])
                        if TestingTile is not None:
                            if TestingTile.Properties[3] != EvaluatedTile.Properties[TileUp]:
                                IsTileFitting = False
                                break
                        TestingTile = self.Board.get(SurroundingSpots[2])
                        if TestingTile is not None:
                            if TestingTile.Properties[0] != EvaluatedTile.Properties[TileRight]:
                                IsTileFitting = False
                                break
                        TestingTile = self.Board.get(SurroundingSpots[3])
                        if TestingTile is not None:
                            if TestingTile.Properties[1] != EvaluatedTile.Properties[TileDown]:
                                IsTileFitting = False
                                break
                        IsTileFitting = True
                        break                
                    if IsTileFitting:
                        TempAvailableMoves.append((TileIndex,X,Y,Rotation,None))
                        break
                if not TempAvailableMoves == []:
                    break
            if TempAvailableMoves == []:
                if not Looping:
                    return []
            else:
                if self.Meeples[self.PlayerTurn] > 0:                    
                    if EvaluatedTile.HasCities:
                        RotatedOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in EvaluatedTile.CityOpenings]
                        for i in range(len(RotatedOpenings)):
                            CityOpenings = RotatedOpenings[i]
                            MeepleFitting = True
                            for CitySide in CityOpenings:
                                if self.Board.get(SurroundingSpots[CitySide]) is None:
                                    pass
                                else:
                                    MatchingCityIndex = self.Board.get(SurroundingSpots[CitySide]).TileCitiesIndex[self.MatchingSide[CitySide]]
                                    while self.BoardCities[MatchingCityIndex].Pointer != self.BoardCities[MatchingCityIndex].ID:                            
                                        MatchingCityIndex = self.BoardCities[MatchingCityIndex].Pointer
                                    MatchingCity = self.BoardCities[MatchingCityIndex]
                                    if MatchingCity.Meeples[0] > 0 or MatchingCity.Meeples[1] > 0:
                                        MeepleFitting = False
                                        break
                            if MeepleFitting:
                                TempAvailableMoves.append((TileIndex,X,Y,Rotation,("C",i)))
                                
                    if EvaluatedTile.HasRoads:
                        RRotatedOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in EvaluatedTile.RoadOpenings]
                        for i in range(len(RRotatedOpenings)):
                            RoadOpenings = RRotatedOpenings[i]
                            MeepleFitting = True
                            for RoadSide in RoadOpenings:
                                if self.Board.get(SurroundingSpots[RoadSide]) is None:
                                    pass
                                else:
                                    MatchingRoadIndex = self.Board.get(SurroundingSpots[RoadSide]).TileRoadsIndex[self.MatchingSide[RoadSide]]
                                    #if ShowLogs: print(self.BoardRoads,"\n",MatchingRoadIndex,RoadSide,SurroundingSpots[RoadSide],X,Y,Rotation,"\n",self.Board.get(SurroundingSpots[RoadSide]))
                                    while self.BoardRoads[MatchingRoadIndex].Pointer != self.BoardRoads[MatchingRoadIndex].ID:                            
                                        MatchingRoadIndex = self.BoardRoads[MatchingRoadIndex].Pointer
                                    MatchingRoad = self.BoardRoads[MatchingRoadIndex]
                                    if MatchingRoad.Meeples[0] > 0 or MatchingRoad.Meeples[1] > 0:
                                        MeepleFitting = False
                                        break
                            if MeepleFitting:
                                TempAvailableMoves.append((TileIndex,X,Y,Rotation,("R",i)))
                                
                    if EvaluatedTile.HasCloister:
                        TempAvailableMoves.append((TileIndex,X,Y,Rotation,("Cloister",0)))
   
                    if EvaluatedTile.HasFarms:
                        RotatedOpenings =  [[(x+SideChange,y) if x+SideChange < 4 else (x+SideChange-4,y) for (x,y) in k] for k in EvaluatedTile.FarmOpenings]
                        for i in range(len(RotatedOpenings)):
                            FarmOpenings = RotatedOpenings[i]
                            MeepleFitting = True
                            for (FarmSide,FarmLine) in FarmOpenings:
                                if self.Board.get(SurroundingSpots[FarmSide]) is None:
                                    pass
                                else:
                                    MatchingFarmIndex = self.Board.get(SurroundingSpots[FarmSide]).TileFarmsIndex[self.MatchingSide[FarmSide]][self.MatchingLine[FarmLine]]
                                    while self.BoardFarms[MatchingFarmIndex].Pointer != self.BoardFarms[MatchingFarmIndex].ID:                            
                                        MatchingFarmIndex = self.BoardFarms[MatchingFarmIndex].Pointer
                                    MatchingFarm = self.BoardFarms[MatchingFarmIndex]
                                    if MatchingFarm.Meeples[0] > 0 or MatchingFarm.Meeples[1] > 0:
                                        MeepleFitting = False
                                        break
                            if MeepleFitting:
                                TempAvailableMoves.append((TileIndex,X,Y,Rotation,("G",i)))
                
            
        Move = rd.choice(TempAvailableMoves)
        #print(Move)
        return Move
    
    def GetAvailableMoves(self,TileIndex, TilesOnly = False):
        #if ShowLogs: print("Testing if tile",TileIndex,"has available moves, TO:",TilesOnly)
        IsTileFitting = False        
        TempAvailableMoves = []
        EvaluatedTile = self.AvailableTiles[TileIndex][0] 
        for (X,Y) in self.AvailableSpots:
            SurroundingSpots = [(X-1,Y),(X,Y+1),(X+1,Y),(X,Y-1)]
            for Rotation in EvaluatedTile.AvailableRotations:                
                if Rotation == 0:
                    SideChange = 0
                    TileLeft,TileUp,TileRight,TileDown = 0,1,2,3
                elif Rotation == 90:
                    SideChange = 1
                    TileLeft,TileUp,TileRight,TileDown = 3,0,1,2
                elif Rotation == 180:
                    SideChange = 2
                    TileLeft,TileUp,TileRight,TileDown = 2,3,0,1
                elif Rotation == 270:
                    SideChange = 3
                    TileLeft,TileUp,TileRight,TileDown = 1,2,3,0
                while True:
                    TestingTile = self.Board.get(SurroundingSpots[0])
                    if TestingTile is not None:
                        if TestingTile.Properties[2] != EvaluatedTile.Properties[TileLeft]:
                            IsTileFitting = False
                            break
                    TestingTile = self.Board.get(SurroundingSpots[1])
                    if TestingTile is not None:
                        if TestingTile.Properties[3] != EvaluatedTile.Properties[TileUp]:
                            IsTileFitting = False
                            break
                    TestingTile = self.Board.get(SurroundingSpots[2])
                    if TestingTile is not None:
                        if TestingTile.Properties[0] != EvaluatedTile.Properties[TileRight]:
                            IsTileFitting = False
                            break
                    TestingTile = self.Board.get(SurroundingSpots[3])
                    if TestingTile is not None:
                        if TestingTile.Properties[1] != EvaluatedTile.Properties[TileDown]:
                            IsTileFitting = False
                            break
                    IsTileFitting = True
                    break                
                if IsTileFitting:
                    TempAvailableMoves.append((TileIndex,X,Y,Rotation,None))
                    
                    if not TilesOnly:
                        if self.Meeples[self.PlayerTurn] > 0:
                            if EvaluatedTile.HasCities:
                                RotatedOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in EvaluatedTile.CityOpenings]
                                for i in range(len(RotatedOpenings)):
                                    CityOpenings = RotatedOpenings[i]
                                    MeepleFitting = True
                                    for CitySide in CityOpenings:
                                        if self.Board.get(SurroundingSpots[CitySide]) is None:
                                            pass
                                        else:
                                            MatchingCityIndex = self.Board.get(SurroundingSpots[CitySide]).TileCitiesIndex[self.MatchingSide[CitySide]]
                                            while self.BoardCities[MatchingCityIndex].Pointer != self.BoardCities[MatchingCityIndex].ID:                            
                                                MatchingCityIndex = self.BoardCities[MatchingCityIndex].Pointer
                                            MatchingCity = self.BoardCities[MatchingCityIndex]
                                            if MatchingCity.Meeples[0] > 0 or MatchingCity.Meeples[1] > 0:
                                                MeepleFitting = False
                                                break
                                    if MeepleFitting:
                                        TempAvailableMoves.append((TileIndex,X,Y,Rotation,("C",i)))
                                        
                            if EvaluatedTile.HasRoads:
                                RRotatedOpenings = [[i+SideChange if i+SideChange < 4 else i+SideChange-4 for i in k] for k in EvaluatedTile.RoadOpenings]
                                for i in range(len(RRotatedOpenings)):
                                    RoadOpenings = RRotatedOpenings[i]
                                    MeepleFitting = True
                                    for RoadSide in RoadOpenings:
                                        if self.Board.get(SurroundingSpots[RoadSide]) is None:
                                            pass
                                        else:
                                            MatchingRoadIndex = self.Board.get(SurroundingSpots[RoadSide]).TileRoadsIndex[self.MatchingSide[RoadSide]]
                                            #if ShowLogs: print(self.BoardRoads,"\n",MatchingRoadIndex,RoadSide,SurroundingSpots[RoadSide],X,Y,Rotation,"\n",self.Board.get(SurroundingSpots[RoadSide]))
                                            while self.BoardRoads[MatchingRoadIndex].Pointer != self.BoardRoads[MatchingRoadIndex].ID:                            
                                                MatchingRoadIndex = self.BoardRoads[MatchingRoadIndex].Pointer
                                            MatchingRoad = self.BoardRoads[MatchingRoadIndex]
                                            if MatchingRoad.Meeples[0] > 0 or MatchingRoad.Meeples[1] > 0:
                                                MeepleFitting = False
                                                break
                                    if MeepleFitting:
                                        TempAvailableMoves.append((TileIndex,X,Y,Rotation,("R",i)))
                                        
                            if EvaluatedTile.HasCloister:
                                TempAvailableMoves.append((TileIndex,X,Y,Rotation,("Cloister",0)))
                            #"""    
                            if EvaluatedTile.HasFarms:
                                RotatedOpenings =  [[(x+SideChange,y) if x+SideChange < 4 else (x+SideChange-4,y) for (x,y) in k] for k in EvaluatedTile.FarmOpenings]
                                for i in range(len(RotatedOpenings)):
                                    FarmOpenings = RotatedOpenings[i]
                                    MeepleFitting = True
                                    for (FarmSide,FarmLine) in FarmOpenings:
                                        if self.Board.get(SurroundingSpots[FarmSide]) is None:
                                            pass
                                        else:
                                            MatchingFarmIndex = self.Board.get(SurroundingSpots[FarmSide]).TileFarmsIndex[self.MatchingSide[FarmSide]][self.MatchingLine[FarmLine]]
                                            while self.BoardFarms[MatchingFarmIndex].Pointer != self.BoardFarms[MatchingFarmIndex].ID:                            
                                                MatchingFarmIndex = self.BoardFarms[MatchingFarmIndex].Pointer
                                            MatchingFarm = self.BoardFarms[MatchingFarmIndex]
                                            if MatchingFarm.Meeples[0] > 0 or MatchingFarm.Meeples[1] > 0:
                                                MeepleFitting = False
                                                break
                                    if MeepleFitting:
                                        TempAvailableMoves.append((TileIndex,X,Y,Rotation,("G",i)))
                            #"""
                                                    
        return TempAvailableMoves
    
    #def FastRandomGameToEnd
    
    def Collector_RandomGames(self, RandomGames = 1, SaveEvery = 5000):
        Numbers = []
        MeanNumbers = [[x,0,0,0,0,0,0,0,0] for x in range(72)]
        for i in range(RandomGames):
            FromState = self.CloneState()
            Turn = 0
            while not FromState.Terminal:
                Chances,_ = FromState.GetChanceOptions()
                Chance = rd.choice(Chances)
                Moves = FromState.GetAvailableMoves(Chance)
                if not Moves == []:
                    MeepleMovesCount = [x for x in Moves if x[4] is not None]
                    CityMeepleMovesCount = [x for x in MeepleMovesCount if x[4][0] == "C"]
                    RoadMeepleMovesCount = [x for x in MeepleMovesCount if x[4][0] == "R"]
                    FarmMeepleMovesCount = [x for x in MeepleMovesCount if x[4][0] == "G"]
                    CloisterMeepleMovesCount = [x for x in MeepleMovesCount if x[4][0] == "Cloister"]
                    Numbers.append([Turn, len(Chances), len(Moves), len(MeepleMovesCount), len(CityMeepleMovesCount), len(RoadMeepleMovesCount), len(FarmMeepleMovesCount), len(CloisterMeepleMovesCount)])
                    MeanNumbers[Turn][1] += 1
                    MeanNumbers[Turn][2] += len(Chances)
                    MeanNumbers[Turn][3] += len(Moves)
                    MeanNumbers[Turn][4] += len(MeepleMovesCount)
                    MeanNumbers[Turn][5] += len(CityMeepleMovesCount)
                    MeanNumbers[Turn][6] += len(RoadMeepleMovesCount)
                    MeanNumbers[Turn][7] += len(FarmMeepleMovesCount)
                    MeanNumbers[Turn][8] += len(CloisterMeepleMovesCount)
                    Move = rd.choice(Moves)
                    FromState.MakeMove(Move, SpeedMode = True)
                    Turn += 1
                else:
                    FromState.EndGameRoutine()
            if i == SaveEvery:
                print("Printing")
                with open('MeanNumbers.csv','w') as csvfile:
                    writer = csv.writer(csvfile,lineterminator='\n')
                    for Arrow in MeanNumbers:
                        writer.writerow([Arrow]) 
                #MeanNumbers = [[x,0,0,0,0,0,0,0,0] for x in range(72)]
        with open('MeanNumbers.csv','w') as csvfile:
            writer = csv.writer(csvfile,lineterminator='\n')
            for Arrow in MeanNumbers:
                writer.writerow([Arrow])
        #return WinnerCount
    
    def SaveGame(self,Name = "GameRecord", ID="", NextTileIndex = None):
        if len(self.GameRecord) > 0 and NextTileIndex is not None: self.GameRecord[-1][4] = NextTileIndex
        with open(str(Name)+str(ID)+'.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile,lineterminator='\n')#, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for Move in self.GameRecord:
                filewriter.writerow(Move)
    
    def __repr__(self):
        #Str = str(self.TileIndexList) + "\n" + str(self.Board) + "\n" + str(self.BoardCities) + "\n" + str(self.BoardRoads) + "\n" + str(self.BoardCloisters) + "\n" + str(self.BoardFarms)
        Str = str(self.TileIndexList)
        return Str

ShowLogs = False
Test = None
TotalGames = 1000
#if len(sys.argv) > 1:  
#    Test = int(sys.argv[1]) 
#    TotalGames = int(sys.argv[2])
#    print(Test)    
 
#rd.seed(1)
if Test == 1:
#Random Games Speed test
    CCN = CarcassonneState()
    print("Playing",TotalGames,"random games")
    ST = time.time()
    WinnerCount = CCN.RandomGameToEnd(RandomGames = TotalGames)
    ET = time.time()
    print("Games ended, time:", str(ET - ST))
    print("WinnerCount",WinnerCount)

elif Test == 2:
#Tile by tile test
    CCN = CarcassonneState()
    TileOrder = [13,5,11,16,18,6,5,13,0,6,11,13,13,16,13]
    GameID = ""
    Turn = 0
    for TileIndex in TileOrder:
        Moves = CCN.GetAvailableMoves(TileIndex)
        Turn += 1
        print(Turn)
        for M in Moves:
            print(M)
        Move = rd.choice(Moves)
        CCN.MakeMove(Move)
    CCN.SaveGame(ID = GameID)
     
elif Test == 3:
#Clone test
    CCN = CarcassonneState()
    Turns = 30
    TurnCount = 0
    while TurnCount < Turns:
        Moves = []
        while Moves == []:
            TileIndex = CCN.GetRandomChanceOption()
            Moves = CCN.GetAvailableMoves(TileIndex)
        Move = rd.choice(Moves)
        CCN.MakeMove(Move)
        TurnCount += 1
        #print(CCN.Board)
        #input("Input to continue")
    CCN.SaveGame(ID = "First30")
    CC = CCN.CloneState()
    Turns = 30
    TurnCount = 0
    while TurnCount < Turns:
        Moves = []
        while Moves == []:
            TileIndex = CC.GetRandomChanceOption()
            Moves = CC.GetAvailableMoves(TileIndex)
        Move = rd.choice(Moves)
        CC.MakeMove(Move)
        TurnCount += 1
    CC.SaveGame(ID = "Cont1")    
    Count = 0
    print("Playing",TotalGames,"random games from move",Turns)
    ST = time.time()
    while Count < TotalGames:
        #input("Input to continue")
        CC = CCN.CloneState()
        Count += 1
        CC.RandomGameToEnd()        
    CC.SaveGame()
    ET = time.time()
    print("Games ended, time:", str(ET - ST))

elif Test == 4:
#Move by move game
    CCN = CarcassonneState()
    while not CCN.Terminal:
        TileIndexes,Probabilities = CCN.GetChanceOptions(GiveProbability = True)
        for i in range(len(TileIndexes)):
            TileIndex,Prob = TileIndexes[i], Probabilities[i]
            print(i,":",TileIndex,"Prob:",Prob)
        SelectedIndex = int(input("Select Tile:"))
        SelectedTile = TileIndexes[SelectedIndex]
        Moves = CCN.GetAvailableMoves(SelectedTile)
        for i in range(len(Moves)):
            Move = Moves[i]
            print(i,":",Move)
        SelectedMove = int(input("Select Move:"))
        Move = Moves[SelectedMove]
        CCN.MakeMove(Move)
        CCN.SaveGame()

if Test == 5:
    CCN = CarcassonneState()
    print("Playing",TotalGames,"collector random games")
    ST = time.time()
    CCN.Collector_RandomGames(TotalGames, 5000)
    ET = time.time()
    print("Games ended, time:", str(ET - ST))
