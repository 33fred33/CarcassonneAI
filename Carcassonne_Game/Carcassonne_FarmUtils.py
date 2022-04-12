from Carcassonne_Game.GameFeatures import Farm

def farmConnections(self, PlayingTile, Surroundings, MeepleUpdate, MeepleKey):
    
    for i in range(len(PlayingTile.FarmOpenings)):
        FarmOpenings = PlayingTile.FarmOpenings[i]
        AddedMeeples = self.AddMeeple(MeepleUpdate, MeepleKey, "G", i) 
        OpeningsQuantity = len(FarmOpenings)      
        if OpeningsQuantity == 1:
            oneFarmConnection(self, PlayingTile, FarmOpenings, Surroundings, AddedMeeples, i)               
        else:
            multipleFarmConnections(self, PlayingTile, FarmOpenings, OpeningsQuantity, Surroundings, AddedMeeples,i)


def oneFarmConnection(self, PlayingTile, FarmOpenings, Surroundings, AddedMeeples, i):
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
            
            
def multipleFarmConnections(self, PlayingTile, FarmOpenings, OpeningsQuantity, Surroundings, AddedMeeples, i):
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
