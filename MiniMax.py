# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 15:17:37 2019

@author: user
"""
ShowLogs = False
def MiniMax(GameState,OptimizingTurn,MaxIter=10000,IterCounter=0):
    global ShowLogs
    if ShowLogs: print("\nIterCounter",IterCounter)
    if GameState.Terminal or MaxIter==IterCounter:
        if GameState.Winner == OptimizingTurn + 1:           
            if ShowLogs:GameState.PrintGameState()
            Value = GameState.CountTiles(OptimizingTurn)#Heuristic
            if ShowLogs: print("Returning 1",Value)
            return Value#1
        elif GameState.Winner == 1 - OptimizingTurn + 1:
            
            if ShowLogs:GameState.PrintGameState()
            Value = GameState.CountTiles(OptimizingTurn)#Heuristic
            if ShowLogs:print("Returning -1",Value)
            return Value#-1
        else:
            Value = GameState.CountTiles(OptimizingTurn)#Heuristic
            if ShowLogs:print("Returning",Value)
            return Value
    else:
        MovesValue = []#[0 for _ in range(len(GameState.AvailableMoves))]
        if ShowLogs:print("Checking ",len(GameState.AvailableMoves),"Moves:",str(GameState.AvailableMoves) ," from State")
        if ShowLogs:GameState.PrintGameState()
        for Move in GameState.AvailableMoves:           
            NewState = GameState.CloneState()
            NewState.MakeMove(Move)
            if ShowLogs:print("In for loop, after move ",str(Move),"IterCounter",IterCounter)
            Value = MiniMax(NewState,OptimizingTurn,MaxIter,IterCounter+1)
            MovesValue.append(Value)
        SortedValues = sorted(MovesValue)
        if ShowLogs:print("\nFinished State at Iter",IterCounter,", sorted Values:")
        if ShowLogs:print(SortedValues)
        if GameState.PlayerTurn == OptimizingTurn:
            if ShowLogs:print("Looking for Max")
            BestValue = SortedValues[-1]
        elif 1 - GameState.PlayerTurn == OptimizingTurn:
            if ShowLogs:print("Loking for Min:")
            BestValue = SortedValues[0]        
        if ShowLogs:GameState.PrintGameState()
        if ShowLogs:print("Best Value:",BestValue)
        if ShowLogs:input("Input to continue")
        return BestValue
            
def FindBestChild(GameState,MaxIter=10000):
    if not GameState.Terminal:  
        BestVal = -9999  
        OptimizingTurn = GameState.PlayerTurn
        #print("OptimizingTurn",OptimizingTurn)
        for Move in GameState.AvailableMoves:
            NewState = GameState.CloneState()
            NewState.MakeMove(Move)
            Value = MiniMax(NewState,OptimizingTurn,MaxIter)
            print("Option:",Move,"Value:",Value)
            if Value > BestVal:
                BestVal = Value
                BestMove = Move
    return BestMove