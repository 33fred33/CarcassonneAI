#!/usr/bin/env python
"""
Created on Tue Feb 26 12:12:45 2019

@author: user
"""

import sys
import time
import random as rd
import MCTS_Chances
import Carcassonne
import Expectimax
import csv
import datetime
#import statistics as sts
#import os

#ID,NumberOfGames,SwitchingSides,RandomSeedStart,P1,P1Params,P2,P2Params,
#Ex: 1,100,T,0,Random,,Random,
#MCTS: RolloutGames,Iterations,Maxtime,ExplorationParameter,LeafParal,RootParal,RAVE,RAVEk
#Ex: 100,500,60,3,F,F,F,10
#Expectimax,Star: Depth
#Ex: 2

ShowLogs = False
StepSaving = False
GameSaving = False
LogsAfterEachGame = True

#P1 = "Human"
#P1 = "MCTS"
#P1 = "Expectimax" 
#P1 = "Star1"
#P1 = "Star2"
#P1 = "Star25"
P1 = "Random"

#P2 = "Human"
#P2 = "MCTS"
#P2 = "Expectimax"
#P2 = "Star1"
#P2 = "Star2"
#P2 = "Star25"
P2 = "Random"

ID = "Test1"
AddToSeed = 0
NumberOfGames = 10
SwitchingSides = True
Now = datetime.datetime.now()
Date = str(Now.hour) + "h" + str(Now.minute) + " " + str(Now.day) + "-" + str(Now.month) + "-" + str(Now.year)
#Path = "Historical Game Records\ "
Path = ""

TileSequence = [10,23,21,22,7,11,8,22]
#TileSequence = [21,13,10,14,14,22,21,16]
FollowTileSequence = True

#MCTS Params [p1, p2]
RolloutGames = [200,200]
Iterations = [500,500]
MaxTime = [60,60] 
ExplorationParameter = [3,3]
RAVEk = [10 , 10]
LeafParal = [False, False]
RootParal = [False, False]
RAVE = [False,False]

#Expectimax Params [p1, p2]
MaxDepth = [2,2]


#Random seed
#rd.seed(1)

def GenerateFileName(ID = "", P1 = "", P2 = "", Date = ""):
    #FileName = ID + " " + Date + " P1 " + P1 + " P2 " + P2
    FileName = ID + " " + Date# + " P1 " + P1 + " P2 " + P2
    return FileName

def HumanTurn(GameState, Chance = None):
    Moves = GameState.GetAvailableMoves(Chance)
    Ologs = " Actions " + str(len(Moves))
    for i in range(len(Moves)):
        Move = Moves[i]
        print(i, ":  ", Move)
    SelectedIndex = int(input("Select Move by index:"))
    Move = Moves[SelectedIndex]
    return Ologs, Move

def MCTSTurn(GameState, Player, Chance = None):
    #print(MaxTime, Iterations, ExplorationParameter, RolloutGames, LeafParal, RootParal, RAVE, RAVEk)
    Ologs, Move = MCTS_Chances.MCTS(GameState, Chance, MaxTime[Player], Iterations[Player], ExplorationParameter[Player], RolloutGames[Player], LeafParal[Player], RootParal[Player], RAVE[Player], RAVEk[Player])
    return Ologs, Move

def ExpectimaxTurn(GameState, Player, Chance = None):
    Ologs, Move = Expectimax.FindBestMove(GameState, Chance, MaxDepth[Player],0)
    return Ologs, Move

def Star1(GameState, Player, Chance = None):
    Ologs, Move = Expectimax.FindBestMove(GameState, Chance, MaxDepth[Player],1)
    return Ologs, Move

def Star2(GameState, Player, Chance = None):
    Ologs, Move = Expectimax.FindBestMove(GameState, Chance, MaxDepth[Player],2)
    return Ologs, Move

def Star25(GameState, Player, Chance = None):
    Ologs, Move = Expectimax.FindBestMove(GameState, Chance, MaxDepth[Player],3)
    return Ologs, Move

def RandomTurn(GameState, Chance = None):
    Moves = GameState.GetAvailableMoves(Chance)
    Ologs = ""
    Move = rd.choice(Moves)
    return Ologs, Move

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

if __name__ == '__main__':
    
    
    if len(sys.argv) > 1:
        IndexCounter = 0
        InputStringT = str(sys.argv[1])
        InputString = InputStringT.split(",")
        
        ID = InputString[0]
    
        NumberOfGames = int(InputString[1])
        if InputString[2] == "T":
            SwitchingSides = True
        else:
            SwitchingSides = False
        AddToSeed = int(InputString[3])
        P1 = InputString[4]
        IndexCounter = 5
        
        if P1 == "MCTS":
            RAVECounter = 0
            RolloutGames[0] = int(InputString[IndexCounter])
            Iterations[0] = int(InputString[IndexCounter + 1])
            MaxTime[0] = float(InputString[IndexCounter + 2])
            ExplorationParameter[0] = float(InputString[IndexCounter + 3])
            if InputString[IndexCounter + 4] == "T":
                LeafParal[0] = True
            else:
                LeafParal[0] = False
            if InputString[IndexCounter + 5] == "T":
                RootParal[0] = True
            else:
                RootParal[0] = False
            if InputString[IndexCounter + 6] == "T":
                RAVE[0] = True
                RAVECounter += 1
                RAVEk[0] = float(InputString[IndexCounter + 7])
            else:
                RAVE[0] = False
            IndexCounter += RAVECounter + 7
        elif P1 == "Expectimax" or P1 == "Star1" or P1 == "Star2" or P1 == "Star25":
            MaxDepth[0] = int(InputString[IndexCounter])
            IndexCounter += 1
        else:
            IndexCounter += 1
        
        P2 = InputString[IndexCounter]
        IndexCounter += 1
        
        if P2 == "MCTS":
            RAVECounter = 0
            RolloutGames[1] = int(InputString[IndexCounter])
            Iterations[1] = int(InputString[IndexCounter + 1])
            MaxTime[1] = float(InputString[IndexCounter + 2])
            ExplorationParameter[1] = float(InputString[IndexCounter + 3])
            if InputString[IndexCounter + 4] == "T":
                LeafParal[1] = True
            else:
                LeafParal[1] = False
            if InputString[IndexCounter + 5] == "T":
                RootParal[1] = True
            else:
                RootParal[1] = False
            if InputString[IndexCounter + 6] == "T":
                RAVE[1] = True
                RAVECounter += 1
                RAVEk[1] = float(InputString[IndexCounter + 7])
            else:
                RAVE[1] = False
            IndexCounter += RAVECounter + 7
        elif P2 == "Expectimax" or P2 == "Star1" or P2 == "Star2" or P2 == "Star25":
            MaxDepth[1] = int(InputString[IndexCounter])
            IndexCounter += 1
    
    if ShowLogs:
        print("P1",P1)
        print("P2",P2)
        print("RolloutGames",RolloutGames)
        print("Iterations",Iterations)
        print("MaxTime",MaxTime)
        print("ExplorationParameter",ExplorationParameter)
        print("RAVEk",RAVEk)
        print("LeafParal",LeafParal)
        print("RootParal",RootParal)
        print("RAVE",RAVE)
    
        
    
    ExperimentStartTime = time.time()
    StartingState = Carcassonne.CarcassonneState()
    WinnerCount=[[0,0,0,0],[0,0,0,0]]
    Side = 0
    FinalLogs = []
    for SwitchTurn in range(2):
        FileName = GenerateFileName(ID,P1,P2,Date)
        InitialLogs = []
        PCount = Side
        for Player in [P1, P2]:
            InitialLogs.append(Player + " Params:")
            if Player == "MCTS":
                if RootParal[PCount]:
                    ParalString = "Root"
                elif LeafParal[PCount]:
                    ParalString = "Leaf"
                else:
                    ParalString = "None"
                #ParalString += "with " + str(os.cpu_count()) + " cores"
                ParalString += "with 4 cores"
                StringToAdd = "RolloutGames " + str(RolloutGames[PCount]) + " Iterations " + str(Iterations[PCount]) + " MaxTime " + str(MaxTime[PCount]) + " ExplorationParameter " + str(ExplorationParameter[PCount]) + " Parallelization " + ParalString
                InitialLogs.append(StringToAdd)
            elif Player == "Star25" or Player == "Expectimax" or Player == "Star1" or Player == "Star2":
                StringToAdd = "MaxDepth " + str(MaxDepth[PCount])
                InitialLogs.append(StringToAdd)
            PCount = 1 - Side
        Logs = [x for x in InitialLogs]        
        for GameNumber in range(NumberOfGames):
            StartingState = Carcassonne.CarcassonneState()
            GameState = StartingState.CloneState()
            RandomSeed = GameNumber + AddToSeed
            rd.seed(RandomSeed)
            TileSequence = [x for x in GameState.TileIndexList]
            rd.shuffle(TileSequence)
            #print(RandomSeed)
            #print(TileSequence)
            #RemoveSeed = 1000 * time.time()
            #rd.seed(int(RemoveSeed) % 2**32)
            Ply = 0
            OutputName = Path + FileName + " " + "Game" + str(GameNumber) + "Side" + str(Side)
            
            while not GameState.Terminal:
                if FollowTileSequence:
                    Chance = TileSequence[Ply]
                    Skip = 0
                    while GameState.GetAvailableMoves(Chance,TilesOnly = True) == []:
                        SkipTile = TileSequence[Ply + Skip] 
                        TileSequence[Ply + Skip] = TileSequence[Ply]
                        TileSequence[Ply] = SkipTile
                        Skip += 1
                        Chance = TileSequence[Ply]
                else:
                    Chance = GameState.GetRandomChanceOption()
                if GameSaving and StepSaving:
                    GameState.SaveGame(Name = OutputName, NextTileIndex = Chance)
                if ShowLogs: print("Next tile:",Chance)
                Choices = " Choices " + str(len(GameState.GetAvailableMoves(Chance)))
                ST = time.time()
                if P1 == "Human": Ologs, Move = HumanTurn(GameState, Chance)
                elif P1 == "MCTS": Ologs, Move = MCTSTurn(GameState, Side, Chance)
                elif P1 == "Random": Ologs, Move = RandomTurn(GameState, Chance)
                elif P1 == "Expectimax": Ologs, Move = ExpectimaxTurn(GameState, Side, Chance)
                elif P1 == "Star1": Ologs, Move = Star1(GameState, Side, Chance)
                elif P1 == "Star2": Ologs, Move = Star2(GameState, Side, Chance)
                elif P1 == "Star25": Ologs, Move = Star25(GameState, Side, Chance)
                else: print("No player match")
                if Move[4] is None:
                    MeepleString = " X"
                elif Move[4][0] == "Cloister":
                    MeepleString = " M"
                else:
                    MeepleString = " " + str(Move[4][0])
                TempString = "GameNumber " + str(GameNumber) + " P1 Turn " + str(Ply) + " by player " + str(P1) + " Chance " + str(Chance) + " Move time " + str(time.time()-ST) + " Scores " + str(GameState.Scores[0]) + " " + str(GameState.Scores[1]) + " " + str(GameState.Scores[2]) + " " + str(GameState.Scores[3]) + " Meeples " + str(GameState.Meeples[0]) + " " + str(GameState.Meeples[1]) + Choices + MeepleString + Ologs
                if ShowLogs: print(TempString)
                Logs.append(TempString)
                GameState.MakeMove(Move)
                if GameSaving and StepSaving:
                    GameState.SaveGame(Name = OutputName)
                Ply += 1
                if GameState.Terminal: break
            
                    
                if FollowTileSequence:
                    Chance = TileSequence[Ply]
                    Skip = 0
                    while GameState.GetAvailableMoves(Chance,TilesOnly = True) == []:
                        SkipTile = TileSequence[Ply + Skip] 
                        TileSequence[Ply + Skip] = TileSequence[Ply]
                        TileSequence[Ply] = SkipTile
                        Skip += 1
                        Chance = TileSequence[Ply]
                else:
                    Chance = GameState.GetRandomChanceOption()
                if GameSaving and StepSaving:
                    GameState.SaveGame(Name = OutputName, NextTileIndex = Chance)
                if ShowLogs: print("Next tile:",Chance)
                Choices = " Choices " + str(len(GameState.GetAvailableMoves(Chance)))
                ST = time.time()
                if P2 == "Human": Ologs, Move = HumanTurn(GameState, Chance)
                elif P2 == "MCTS": Ologs, Move = MCTSTurn(GameState,1-Side, Chance)
                elif P2 == "Random": Ologs, Move = RandomTurn(GameState, Chance)
                elif P2 == "Expectimax": Ologs, Move = ExpectimaxTurn(GameState,1-Side, Chance)
                elif P2 == "Star1": Ologs, Move = Star1(GameState,1-Side, Chance)
                elif P2 == "Star2": Ologs, Move = Star2(GameState,1-Side, Chance)
                elif P2 == "Star25": Ologs, Move = Star25(GameState,1-Side, Chance)
                else: print("No player match")
                if Move[4] is None:
                    MeepleString = " X"
                elif Move[4][0] == "Cloister":
                    MeepleString = " M"
                else:
                    MeepleString = " " + str(Move[4][0])
                TempString = "GameNumber " + str(GameNumber) + " P2 Turn " + str(Ply) + " by player " + str(P2) + " Chance " + str(Chance) + " Move time " + str(time.time()-ST) + " Scores " + str(GameState.Scores[0]) + " " + str(GameState.Scores[1]) + " " + str(GameState.Scores[2]) + " " + str(GameState.Scores[3]) + " Meeples " + str(GameState.Meeples[0]) + " " + str(GameState.Meeples[1]) + Choices + MeepleString + Ologs
                if ShowLogs: print(TempString)
                Logs.append(TempString)
                GameState.MakeMove(Move)
                if GameSaving and StepSaving:
                    GameState.SaveGame(Name = OutputName)
                Ply += 1
                
                
            if GameSaving:    
                GameState.SaveGame(Name = OutputName)
            WinnerCount[Side][GameState.Winner] += 1
            print("ID ", str(ID), " WinnerCount ", WinnerCount, " Scores:", GameState.Scores[2], GameState.Scores[3])
            FinalLogs = [x for x in InitialLogs ]
            #FinalLogs.append(str(WinnerCount))
        
            
            if LogsAfterEachGame:  
                with open(Path + "FullLogs--" + FileName + '.csv', 'w') as csvfile:
                    filewriter = csv.writer(csvfile,lineterminator='\n')#, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    for LogLine in Logs:
                        filewriter.writerow([LogLine])
                ScoresSum = [0,0]
                ScoreSum = 0
                FinalScoresHistory = []
                FinalScoresHistory.append([])
                FinalScoresHistory.append([])
                FinalScoresStdDeviation = [0,0]
                FinalScoresDiffHistory = []
                FinalScoresDiffStdDeviation = 0
                TimeByTurnHistoryStdDeviation = [0,0]
                ScoreByTurnSum = [[0 for _ in range(71)],[0 for _ in range(71)],[0 for _ in range(71)],[0 for _ in range(71)]]
                #TotalTime = [0,0]
                TimeByTurnSum = [[0 for _ in range(36)],[0 for _ in range(36)]]
                TimeByTurnHistory = []
                TimeByTurnHistory.append([])
                TimeByTurnHistory.append([])
                TotalPlayedMeeples = [0,0]
                TurnsWithoutMeeples = [0,0]
                BranchingFactorSum = 0
                MeeplesByTurnSum = [[0 for _ in range(71)],[0 for _ in range(71)]]
                LWinnerCount = [0,0,0]
                ExpandedNodesSum = [0,0]
                ExpandedNodesByTurnSum = [[0 for _ in range(36)],[0 for _ in range(36)]]
                ExpandedCNodesSum = [0,0]
                ExpandedCNodesByTurnSum = [[0 for _ in range(36)],[0 for _ in range(36)]]
                MeepleLocationsSum = [[0,0,0,0],[0,0,0,0]]
                for LogLine in Logs:
                    #if len(LogLine) > 22:
                    if LogLine[0] == "G" and LogLine[1] == "a":
                        #print(LogLine)
                        SplitLogLine = LogLine.split(' ')
                        RowTurn = int(SplitLogLine[4])
                        RowSinglePlayerTurn = int(RowTurn/2)
                        if SplitLogLine[2] == "P1":
                            RowPlayer = 0
                        elif SplitLogLine[2] == "P2":
                            RowPlayer = 1
                        ScoreByTurnSum[0][RowTurn] += int(SplitLogLine[14])
                        ScoreByTurnSum[1][RowTurn] += int(SplitLogLine[15])
                        ScoreByTurnSum[2][RowTurn] += int(SplitLogLine[16])
                        ScoreByTurnSum[3][RowTurn] += int(SplitLogLine[17])
                        MeeplesByTurnSum[0][RowTurn] += int(SplitLogLine[19])
                        MeeplesByTurnSum[1][RowTurn] += int(SplitLogLine[20])
                        TimeByTurnSum[RowPlayer][RowSinglePlayerTurn] += float(SplitLogLine[12])
                        TimeByTurnHistory[RowPlayer].append(float(SplitLogLine[12]))
                        #TotalTime[RowPlayer] += float(SplitLogLine[12])
                        BranchingFactorSum += int(SplitLogLine[22])
                        
                        if not SplitLogLine[23] == "X":
                            TotalPlayedMeeples[RowPlayer] += 1
                            if SplitLogLine[23] == "G":
                                MeepleLocationsSum[RowPlayer][0] += 1
                            if SplitLogLine[23] == "C":
                                MeepleLocationsSum[RowPlayer][1] += 1
                            if SplitLogLine[23] == "R":
                                MeepleLocationsSum[RowPlayer][2] += 1
                            if SplitLogLine[23] == "M":
                                MeepleLocationsSum[RowPlayer][3] += 1
                        if SplitLogLine[19 + RowPlayer] == "0":
                            TurnsWithoutMeeples[RowPlayer] += 1
                        
                        if len(SplitLogLine) > 25:
                            #print(SplitLogLine)
                            ExpandedNodesByTurnSum[RowPlayer][RowSinglePlayerTurn] += int(SplitLogLine[25])
                            ExpandedNodesSum[RowPlayer] += int(SplitLogLine[25])
                            if len(SplitLogLine) > 27:
                                ExpandedCNodesByTurnSum[RowPlayer][RowSinglePlayerTurn] = int(SplitLogLine[27])
                                ExpandedCNodesSum[RowPlayer] += int(SplitLogLine[27])
                        
                        if RowTurn == 70:
                            ScoresSum[0] += int(SplitLogLine[16])
                            ScoresSum[1] += int(SplitLogLine[17])
                            ScoreSum += ScoresSum[0] + ScoresSum[1]
                            FinalScoresHistory[0].append(float(SplitLogLine[16]))
                            FinalScoresHistory[1].append(float(SplitLogLine[17]))
                            FinalScoresDiffHistory.append(float(float(SplitLogLine[16]) - float(SplitLogLine[17])))
                            if int(SplitLogLine[16]) > int(SplitLogLine[17]):
                                LWinnerCount[0] += 1
                            elif int(SplitLogLine[16]) < int(SplitLogLine[17]):
                                LWinnerCount[1] += 1
                            else:
                                LWinnerCount[2] += 1
                
                LNumberOfGames = float(GameNumber + 1)
                MeanScoresByTurn = [[float(x) / LNumberOfGames for x in ScoreByTurnSum[0]] , [float(x) / LNumberOfGames for x in ScoreByTurnSum[1]] , [float(x) / LNumberOfGames for x in ScoreByTurnSum[2]] , [float(x) / LNumberOfGames for x in ScoreByTurnSum[3]]]
                MeanTurnsWithoutMeeples = [float(x) / LNumberOfGames for x in TurnsWithoutMeeples]
                MeanPlayedMeeples = [float(x) / LNumberOfGames for x in TotalPlayedMeeples]
                MeanFinalScore = [float(x) / LNumberOfGames for x in ScoresSum]
                if MeanFinalScore[0] > MeanFinalScore[1]:
                    WinnerFinalScoreRelation = (MeanFinalScore[0] / MeanFinalScore[1])
                else:
                    WinnerFinalScoreRelation = (MeanFinalScore[1] / MeanFinalScore[0])
                VictoryPercentage = [float(x) * 100 / LNumberOfGames for x in LWinnerCount]
                MeanTimeByTurn = [[float(x) / LNumberOfGames for x in TimeByTurnSum[0]],[float(x) / LNumberOfGames for x in TimeByTurnSum[1]]]
                MeanMeeplesByTurn = [[float(x) / LNumberOfGames for x in MeeplesByTurnSum[0]] , [float(x) / LNumberOfGames for x in MeeplesByTurnSum[1]]]
                MeanBranchingFactor = float(BranchingFactorSum) / (LNumberOfGames * 71.0)
                MeanExpandedNodesByTurn = [[float(x) / LNumberOfGames for x in ExpandedNodesByTurnSum[0]] , [float(x) / LNumberOfGames for x in ExpandedNodesByTurnSum[1]]]
                MeanExpandedNodes = [float(sum(ExpandedNodesByTurnSum[0])) / (36.0 * LNumberOfGames) , float(sum(ExpandedNodesByTurnSum[1])) / (35.0 * LNumberOfGames)]
                MeanExpandedCNodesByTurn = [[float(x) / LNumberOfGames for x in ExpandedCNodesByTurnSum[0]] , [float(x) / LNumberOfGames for x in ExpandedCNodesByTurnSum[1]]]
                MeanExpandedCNodes = [float(sum(ExpandedCNodesByTurnSum[0])) / (36.0 * LNumberOfGames), float(sum(ExpandedCNodesByTurnSum[1])) / (35.0 * LNumberOfGames)]
                MeanTurnTime = [float(sum(MeanTimeByTurn[0])) / (36.0) , float(sum(MeanTimeByTurn[1])) / (35.0)]
                MeanMeeplesUse = [[float(x) / LNumberOfGames for x in MeepleLocationsSum[0]] , [float(x) / LNumberOfGames for x in MeepleLocationsSum[1]]]
                MeanMeeplesUsePercentage = [[float(x) * 100.0 / float(sum(MeepleLocationsSum[0])) for x in MeepleLocationsSum[0]],[float(x) * 100.0 / float(sum(MeepleLocationsSum[1])) for x in MeepleLocationsSum[1]]]
                MeanScoreDifference = float(MeanScoresByTurn[2][70] - MeanScoresByTurn[3][70])
                if len(FinalScoresHistory[0]) > 1 and len(FinalScoresHistory[1]) > 1 and len(FinalScoresDiffHistory) > 1:
                    FinalScoresStdDeviation[0] = stddev(FinalScoresHistory[0],1)
                    FinalScoresStdDeviation[1] = stddev(FinalScoresHistory[1],1)
                    FinalScoresDiffStdDeviation = stddev(FinalScoresDiffHistory,1)
                if len(TimeByTurnHistory[0]) > 1 and len(TimeByTurnHistory[1]) > 1:
                    TimeByTurnHistoryStdDeviation[0] = stddev(TimeByTurnHistory[0],1)
                    TimeByTurnHistoryStdDeviation[1] = stddev(TimeByTurnHistory[1],1)
                    
                with open(Path + FileName + "Logs" + '.csv', 'w') as csvfile:
                    filewriter = csv.writer(csvfile,lineterminator='\n') 
                    for LogLine in FinalLogs:
                        filewriter.writerow([LogLine])
                    filewriter.writerow(["ExperimentTime " + str(time.time() - ExperimentStartTime)])
                    filewriter.writerow(["PlayedGames " + str(LNumberOfGames)])
                    filewriter.writerow(["DrawnGames " + str(WinnerCount[0][2])])
                    filewriter.writerow(["DrawnGamesPercentage " + str(VictoryPercentage[2])])
                    filewriter.writerow(["Result " + str(WinnerCount[0][0] - WinnerCount[0][1])])
                    filewriter.writerow(["MeanScoreDifference " + str(MeanScoreDifference)])
                    filewriter.writerow(["StdDeviationScoreDifference " + str(FinalScoresDiffStdDeviation)])
                    filewriter.writerow(["WinnerFinalScoresRelation " + str(WinnerFinalScoreRelation)])
                    filewriter.writerow(["MeanBranchingFactor " + str(MeanBranchingFactor)]) 
                    filewriter.writerow(["Name P1 P2"])
                    filewriter.writerow(["Wins " + str(WinnerCount[0][0]) + " " + str(WinnerCount[0][1])])
                    filewriter.writerow(["TotalExpandedNodes " + str(ExpandedNodesSum[0]) + " " + str(ExpandedNodesSum[1])])
                    filewriter.writerow(["MeanPlayedMeeples " + str(MeanPlayedMeeples[0])  + " " + str(MeanPlayedMeeples[1])])
                    filewriter.writerow(["MeanFinalScore " + str(MeanFinalScore[0]) + " " + str(MeanFinalScore[1])])
                    filewriter.writerow(["StdDeviationFinalScore " + str(FinalScoresStdDeviation[0]) + " " + str(FinalScoresStdDeviation[1])])
                    filewriter.writerow(["MeanTurnsWithoutMeeples " + str(MeanTurnsWithoutMeeples[0]) + " " + str(MeanTurnsWithoutMeeples[1])])
                    filewriter.writerow(["VictoryPercentage " + str(VictoryPercentage[0]) + " " + str(VictoryPercentage[1])])  
                    filewriter.writerow(["MeanTurnTime " + str(MeanTurnTime[0]) + " " + str(MeanTurnTime[1])])
                    filewriter.writerow(["StdDeviationTurnTime " + str(TimeByTurnHistoryStdDeviation[0]) + " " + str(TimeByTurnHistoryStdDeviation[1])])
                    filewriter.writerow(["MeanExpandedNodes " + str(MeanExpandedNodes[0]) + " " + str(MeanExpandedNodes[1])])
                    filewriter.writerow(["MeanExpandedCNodes " + str(MeanExpandedCNodes[0]) + " " + str(MeanExpandedCNodes[1])])
                    filewriter.writerow(["MeanFarmMeeples" + " " + str(MeanMeeplesUse[0][0]) + " " + str(MeanMeeplesUse[1][0])])
                    filewriter.writerow(["MeanCityMeeples" + " " + str(MeanMeeplesUse[0][1]) + " " + str(MeanMeeplesUse[1][1])])
                    filewriter.writerow(["MeanRoadMeeples" + " " + str(MeanMeeplesUse[0][2]) + " " + str(MeanMeeplesUse[1][2])])
                    filewriter.writerow(["MeanMonasteryMeeples" + " " + str(MeanMeeplesUse[0][3]) + " " + str(MeanMeeplesUse[1][3])])
                    filewriter.writerow(["MeanFarmMeeplesPercentage" + " " + str(MeanMeeplesUsePercentage[0][0]) + " " + str(MeanMeeplesUsePercentage[1][0])])
                    filewriter.writerow(["MeanCityMeeplesPercentage" + " " + str(MeanMeeplesUsePercentage[0][1]) + " " + str(MeanMeeplesUsePercentage[1][1])])
                    filewriter.writerow(["MeanRoadMeeplesPercentage" + " " + str(MeanMeeplesUsePercentage[0][2]) + " " + str(MeanMeeplesUsePercentage[1][2])])
                    filewriter.writerow(["MeanMonasteryMeeplesPercentage" + " " + str(MeanMeeplesUsePercentage[0][3]) + " " + str(MeanMeeplesUsePercentage[1][3])])
                    filewriter.writerow(["Turn ScoreP1 ScoreP2 VScoreP1 VScoreP2 MeeplesP1 MeeplesP2 TimeP1 TimeP2 ENodesP1 ENodesP2 ECNodesP1 ECNodesP2"])
                    for i in range(71):
                        if i < 36:
                            StringToPrint = str(i) + " " + str(MeanScoresByTurn[0][i]) + " " + str(MeanScoresByTurn[1][i]) + " " + str(MeanScoresByTurn[2][i]) + " " + str(MeanScoresByTurn[3][i]) + " " + str(MeanMeeplesByTurn[0][i]) + " " + str(MeanMeeplesByTurn[1][i]) + " " + str(MeanTimeByTurn[0][i]) + " " + str(MeanTimeByTurn[1][i]) + " " + str(MeanExpandedNodesByTurn[0][i]) + " " + str(MeanExpandedNodesByTurn[1][i]) + " " + str(MeanExpandedCNodesByTurn[0][i]) + " " + str(MeanExpandedCNodesByTurn[1][i])
                        else:
                            StringToPrint = str(i) + " " + str(MeanScoresByTurn[0][i]) + " " + str(MeanScoresByTurn[1][i]) + " " + str(MeanScoresByTurn[2][i]) + " " + str(MeanScoresByTurn[3][i]) + " " + str(MeanMeeplesByTurn[0][i]) + " " + str(MeanMeeplesByTurn[1][i])
                        filewriter.writerow([StringToPrint])
                        
        if SwitchingSides:
            print("Switching sides")
            Side = 1
            P1Temp = P1
            P1 = P2
            P2 = P1Temp
        else:
            break
    print("ID",ID," Session results:",WinnerCount)



