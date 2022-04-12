from Carcassonne_Game.GameFeatures import Road


def roadConnections(self, PlayingTile, Surroundings, ClosingRoads, MeepleUpdate, MeepleKey):
    
    for i in range(len(PlayingTile.RoadOpenings)):
        RoadOpenings = PlayingTile.RoadOpenings[i]
        AddedMeeples = self.AddMeeple(MeepleUpdate, MeepleKey, "R", i)        
        OpeningsQuantity = len(RoadOpenings) 
        
        if OpeningsQuantity == 1:
            ClosingRoads = oneRoadConnection(self, PlayingTile, ClosingRoads, RoadOpenings, Surroundings, AddedMeeples)
        else:
            ClosingRoads = multipleRoadConnections(self, PlayingTile, ClosingRoads, RoadOpenings, OpeningsQuantity, Surroundings, AddedMeeples)
        
    return ClosingRoads

def oneRoadConnection(self, PlayingTile, ClosingRoads, RoadOpenings, Surroundings, AddedMeeples):

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
            
    return ClosingRoads
            
def multipleRoadConnections(self, PlayingTile, ClosingRoads, RoadOpenings, OpeningsQuantity, Surroundings, AddedMeeples):
    
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
                
    return ClosingRoads
    
def roadClosures(self, ClosingRoads):

    for ClosingRoadIndex in ClosingRoads:
        ClosingRoad = self.BoardRoads[ClosingRoadIndex]
        if ClosingRoad.Meeples[0] == 0 and ClosingRoad.Meeples[1] == 0:
            pass
        elif ClosingRoad.Meeples[0] > ClosingRoad.Meeples[1]:
            self.Scores[0] += ClosingRoad.Value
            self.FeatureScores[0][1] += ClosingRoad.Value
            #print(f'POINTS ADDED - Completed Road \nPlayer 1 - Points: +{ClosingRoad.Value} \n')
        elif ClosingRoad.Meeples[0] < ClosingRoad.Meeples[1]:
            self.Scores[1] += ClosingRoad.Value
            self.FeatureScores[1][1] += ClosingRoad.Value
            #print(f'POINTS ADDED - Completed Road \nPlayer 2 - Points: +{ClosingRoad.Value} \n')
        else:
            self.Scores[0] += ClosingRoad.Value
            self.FeatureScores[0][1] += ClosingRoad.Value
            self.Scores[1] += ClosingRoad.Value
            self.FeatureScores[1][1] += ClosingRoad.Value
            #print(f'POINTS ADDED - Completed Road \nPoints Shared - Points: +{ClosingRoad.Value} \n')
        ClosingRoad.Value = 0
        self.Meeples[0] += ClosingRoad.Meeples[0]
        self.Meeples[1] += ClosingRoad.Meeples[1]