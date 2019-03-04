# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 17:13:13 2019

@author: fredx
"""


import time
import random as rd
import copy
import math
import hashlib
import logging
import argparse

#Input values, will be used if None are given while calling
ShowLogs = False
RolloutGames = 100
UCTExplorationParameter = 2
MCTSIterations = 400

#PointsPerWin = 1
#PointsPerLose = -PointsPerWin
#MaxValue = RolloutGames# PointsPerWin*RolloutGames #Game specific Formula

#For logs
RolloutTotalTime = 0

class CNode():
    def __init__(self, GameState, IDMove = [-1,-1], Parent = None): #ID = [level, number in level]
        self.Visits = 0
        self.Reward = 0.0
        self.GameState = GameState
        self.Children = []
        self.IDMove = IDMove
        self.Parent = Parent
        if self.GameState.Terminal:
            self.AvailableChildrenMoves = []
        else:
            self.AvailableChildrenMoves = self.GameState.AvailableMoves[:]
            #print(self.AvailableChildrenMoves)
    def AddChild(self, ChildState, IDMove):
        Child = CNode(ChildState, IDMove, self)
        self.Children.append(Child)
        self.AvailableChildrenMoves.remove(IDMove)
    def Update(self,Reward):
        self.Reward += Reward
        self.Visits += 1
    def SelectBestChildren(self):
        global UCTExplorationParameter
        BestChild = sorted(self.Children, key = lambda Child: Child.Reward / Child.Visits + UCTExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
        return BestChild
    def __repr__(self):
        global ShowLogs
        #if ShowLogs: print("\nNODE:")
        Str = "NODE, Parent:[%d,%d] IDMove:" + str(self.IDMove) + " Children: %d left: %d, Visits: %d, Reward: "+":{:.3f}".format(self.Reward)+", Value:"
        #print(self.ID[0], self.ID[1])
        try: String = Str %(self.Parent.IDMove[0],self.Parent.IDMove[1],len(self.Children),len(self.AvailableChildrenMoves),self.Visits,self.Reward)
        except: String = Str %(-1,-1,len(self.Children),len(self.AvailableChildrenMoves),self.Visits)
        #self.GameState.PrintGameState()
        return String
    


    
def Selection(Node):
    #while Node.AvailableChildrenMoves == [] and Node.Children != [] and not Node.GameState.Terminal:
    while Node.AvailableChildrenMoves == [] and Node.Children != []:
        Node = Node.SelectBestChildren()
        if ShowLogs: print("Moving to node:",Node)
        if ShowLogs: Node.GameState.PrintGameState()
    if ShowLogs: print("Selected Node:",Node)
    return Node

def Expand(Node):
    if len(Node.AvailableChildrenMoves) > 0:
        if ShowLogs: print("Expanding Node:", Node)
        NextMove = rd.choice(Node.AvailableChildrenMoves)
        NewState = Node.GameState.CloneState()
        NewState.MakeMove(NextMove)
        Node.AddChild(NewState, NextMove)
        if ShowLogs: print("Created Child Node:", Node.Children[-1])
    else:
        return Node
    return Node.Children[-1]

def Backpropagate(Node,Reward):
    if ShowLogs: print("Backpropagating with Reward",Reward)
    BPReward = copy.deepcopy(Reward)
    while not Node == None:
        Node.Update(BPReward)
        BPReward = -BPReward
        if ShowLogs: print("Updated Node:", Node)
        Node = Node.Parent

def Rollout(Node):
    RolloutStartTime = time.time()
    global RolloutTotalTime
    global RolloutGames
    #global PointsPerWin
    #global PointsPerLose
    #global MaxValue   
    WinnerCount = [0,0,0]#P1 wins, P2 wins, Draws
    if Node.GameState.Terminal:
        WinnerCount[Node.GameState.Winner-1] += RolloutGames
    else:
        for i in range(RolloutGames):
            CurrentState = Node.GameState.CloneState()
            while not CurrentState.Terminal:#Default policy 
                CurrentState.MakeMove()#Default policy 
            WinnerCount[CurrentState.Winner-1] += 1
    Reward = WinnerCount[Node.Parent.GameState.PlayerTurn] - WinnerCount[Node.GameState.PlayerTurn]# * PointsPerWin + WinnerCount[Node.GameState.PlayerTurn] * PointsPerLose
    if ShowLogs: print("WinnerCount",WinnerCount,"Points:",Reward)
    Reward = Reward / RolloutGames 
    if ShowLogs: print("Rollout results: PlayerTurn",Node.Parent.GameState.PlayerTurn,",Reward:",Reward)
    RolloutTotalTime += time.time() - RolloutStartTime
    return Reward #Victories - Defeats / TotalGames           

def MCTSearch(RootNode,Hyper=[]):
    global ShowLogs
    global MCTSIterations
    if ShowLogs: print("Starting MCTS at RootNode:", RootNode)
    #### Hyperparameters assignment:
    for i in range(MCTSIterations):
        if ShowLogs: print("Iteration",i,"of",MCTSIterations,"in MCTS")
        if ShowLogs: print("\nRunning Selection")
        #input("Input to continue")
        CurrentBestLeaf = Selection(RootNode)    
        if ShowLogs: print("\nRunning Expansion")
        #input("Input to continue")
        NewNode = Expand(CurrentBestLeaf)
        if ShowLogs: print("\nRunning Rollout from State:")
        if ShowLogs: NewNode.GameState.PrintGameState()
        #input("Input to continue")
        NewNodeReward = Rollout(NewNode)
        if ShowLogs: print("NewNodeReward from Rollout:",NewNodeReward)
        if ShowLogs: print("\nRunning Backpropagation")
        #input("Input to continue")
        Backpropagate(NewNode,NewNodeReward)
        if ShowLogs: input("Input to continue")

    for Option in RootNode.Children:
        print("Option node",Option)
    BestCandidateNode = sorted(RootNode.Children, key = lambda Child: Child.Visits)[-1]
    print("RolloutTotalTime:",RolloutTotalTime)
        
    return BestCandidateNode
            

def FindBestChild(GameState, IRolloutGames = None, IUCTExplorationParameter = None, IMCTSIterations = None):
    MCTSStartTime = time.time()
    global RolloutTotalTime
    RolloutTotalTime = 0
    if IRolloutGames is not None:
        global RolloutGames
        #global MaxValue
        RolloutGames = IRolloutGames
        #MaxValue = PointsPerWin*RolloutGames
    if IUCTExplorationParameter is not None:
        global UCTExplorationParameter
        UCTExplorationParameter = IUCTExplorationParameter
    if IMCTSIterations is not None:
        global MCTSIterations
        MCTSIterations = IMCTSIterations
        
    RootState = GameState.CloneState()
    CurrentNode = CNode(RootState)    
    BestChildNode = MCTSearch(CurrentNode)    
    SelectedMove = BestChildNode.IDMove   
    MCTSTime = time.time() - MCTSStartTime
    print("MCTS Move Time",MCTSTime)
    print("Rollout Time in MCTS: "+":{:.5f}".format(1-(MCTSTime-RolloutTotalTime)/(MCTSTime+0.0001)),"%")
    print("True MCTS Time:" + ":{:.5f}".format(MCTSTime-RolloutTotalTime))
    return SelectedMove

