# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:23:59 2019

@author: user
"""

ShowLogs = False
def Expectimax (GameState, ExpectimaxPlayer = 0, MaxDepth = 3, Depth = 0):
    if GameState.Terminal or Depth == MaxDepth:
        return GameState.Scores[ExpectimaxPlayer+2] - GameState.Scores[(1-ExpectimaxPlayer)+2]
    else:
        Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
        Value = 0
        for i in range(len(Chances)):           
            Chance = Chances[i]
            Moves = GameState.GetAvailableMoves(Chance)
            MovesValue = []
            for Move in Moves: 
                NewState = GameState.CloneState()
                NewState.MakeMove(Move)
                MoveValue = Expectimax(NewState, ExpectimaxPlayer, MaxDepth, Depth +1)
                MovesValue.append(MoveValue)
            if GameState.PlayerTurn == ExpectimaxPlayer: BestValue = sorted(MovesValue)[-1]
            else: BestValue = sorted(MovesValue)[0]
            Value += Probabilities[i]*BestValue
        return Value
    
def FindBestMove(GameState, Chance = None, MaxDepth = 3):
    Moves = GameState.GetAvailableMoves(Chance)
    ExpectimaxPlayer = GameState.PlayerTurn
    MaxValue = -999
    for Move in Moves:
        NewState = GameState.CloneState()
        NewState.MakeMove(Move)
        MoveValue = Expectimax(NewState, ExpectimaxPlayer, MaxDepth)
        #if ShowLogs: 
        #print("Move",Move,"Value",MoveValue,"\n")
        if MoveValue > MaxValue:
            BestMove = Move
            MaxValue = MoveValue
    return BestMove