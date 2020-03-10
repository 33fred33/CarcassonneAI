#!/usr/bin/env python
"""
Created on Fri Feb 22 15:08:50 2019

@author: user
"""
import math
import random as rd
import time
from multiprocessing import Process, Queue, Lock

class CNode():
    def __init__(self, GameState, IDMove = None, ChanceParent = None, Parent = None, MoveHistory = [], ChanceHistory = []):
        #Initialization
        self.Appearence = 1 #Only used at Multiprocessing
        self.Visits = 0
        self.Reward = 0.0
        self.RAVEVisits = 0
        self.RAVEReward = 0.0
        self.GameState = GameState
        self.Children = {}
        #Variables assignment
        self.ChanceParent = ChanceParent
        self.IDMove = IDMove
        self.MoveHistory = []
        if self.IDMove is not None:
            self.MoveHistory.append(IDMove)
        self.ChanceHistory = []
        if self.ChanceParent is not None:
            self.ChanceHistory.append(ChanceParent)
        self.Parent = Parent
        self.AvailableChances,_ = self.GameState.GetChanceOptions()
        self.WeightedChances = [x for x in self.GameState.TileIndexList if x in self.AvailableChances]
        self.AvailableChildrenMoves = {}
        self.FullyExpanded = {}
        for Chance in self.AvailableChances:
            self.FullyExpanded[Chance] = False
            self.AvailableChildrenMoves[Chance] = [x for x in self.GameState.GetAvailableMoves(Chance)]
        
    def AddChild(self, ChildState, IDMove, ChanceParent):
        if not ChanceParent in self.Children:
            self.Children[ChanceParent] = [CNode(ChildState, IDMove, ChanceParent, self, self.MoveHistory, self.ChanceHistory)]
        else:
            self.Children[ChanceParent].append(CNode(ChildState, IDMove, ChanceParent, self, self.MoveHistory, self.ChanceHistory))
        self.AvailableChildrenMoves[ChanceParent].remove(IDMove)
        if self.AvailableChildrenMoves[ChanceParent] == []:
            self.FullyExpanded[ChanceParent] = True
        return self.Children[ChanceParent][-1]
        
    def Update(self, Reward, RAVEReward = 0, RAVEVisits = 0):
        self.Reward += Reward
        self.Visits += 1     
        self.RAVEReward += RAVEReward
        self.RAVEVisits += RAVEVisits   
        
    def SelectBestChildren(self, Chance, ExplorationParameter, RAVE = False, RAVEk = 1):
        if RAVE:
            #BestChild = sorted(self.Children[Chance], key = lambda Child: (1 - math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.Reward / (Child.Visits + 0.0001)) + ( math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.RAVEReward / (Child.RAVEVisits + 0.0001)) + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
            BestChild = sorted(self.Children[Chance], key = lambda Child: (1 - Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.Reward / (Child.Visits + 0.0001)) + ( Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.RAVEReward / (Child.RAVEVisits + 0.0001)) + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
        else:
            BestChild = sorted(self.Children[Chance], key = lambda Child: Child.Reward / Child.Visits + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
            
            
        #Sorted = sorted(self.Children[Chance], key = lambda Child: Child.Reward / Child.Visits + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))
        
        #for Child in Sorted:
            #print("Child",Child)
            #RAVEValue = (1 - math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.Reward / Child.Visits) + ( math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.RAVEReward / (Child.RAVEVisits + 1)) + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits))
            #RAVEValue = (1 - Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.Reward / (Child.Visits + 0.0001)) + ( Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.RAVEReward / (Child.RAVEVisits + 0.0001)) + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits))
            #NormalValue = Child.Reward / Child.Visits + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits))
            #print("RAVER",Child.RAVEReward,"RAVEV",Child.RAVEVisits,"RAVEk",RAVEk,"RAVEValue",RAVEValue)
            #print(Child)
            #print("RAVEVisits", Child.RAVEVisits)
            #print("RAVEReward", Child.RAVEReward)
            #print("beta",str(math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))))
            #print("new beta",Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2)))
            #print("NormalValue       ",NormalValue)
            #print("RAVEValue         ",RAVEValue)
            #print("Weighted Normal   ", str((1 - Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.Reward / (Child.Visits + 0.0001))) )
            #print("Weighted RAVE     ", str(( Child.RAVEVisits / (Child.Visits + Child.RAVEVisits + 4 * Child.RAVEVisits * Child.Visits * (RAVEk ** 2))) * (Child.RAVEReward / (Child.RAVEVisits + 0.0001))) )
            #print("Reward/Visits     ",Child.Reward / (Child.Visits + 0.0001) )
            #print("RAVE Reward/Visits",Child.RAVEReward / (Child.RAVEVisits + 0.0001),"\n" )
            #RBestChild = sorted(self.Children[Chance], key = lambda Child: (1 - math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.Reward / (Child.Visits + 0.0001)) + ( math.sqrt( RAVEk / ( 3 *  Child.Visits + RAVEk ))) * (Child.RAVEReward / (Child.RAVEVisits + 0.0001)) + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
            #NBestChild = sorted(self.Children[Chance], key = lambda Child: Child.Reward / Child.Visits + ExplorationParameter * math.sqrt(math.log(self.Visits)/float(Child.Visits)))[-1]
        
        #print("RBestChild",RBestChild)
        #print("NBestChild",NBestChild)
        #print("Chosen:",BestChild)
        #input("stop")
        
        return BestChild
    
    def __repr__(self):
        Str = "NODE ChanceH" + str(self.ChanceHistory) + "MoveH" + str(self.MoveHistory) + " V" + str(self.Visits) + " R" + str(self.Reward)
        return Str

    def __eq__(self, OtherNode):
        if self.MoveHistory == OtherNode.MoveHistory and self.ChanceHistory == OtherNode.ChanceHistory:
            return True
        else:
            return False
    
    def __hash__(self):
        return hash((self.MoveHistory, self.ChanceHistory))  
    

def MCTSearch(GameState, RootChance, MCTSPlayer, MaxTime = 10000, Iterations = 10000, ExplorationParameter = 2, RolloutGames = 100, LeafParal = True, RAVE = False,  RAVEk = 1):
    RootNode = CNode(GameState)
    ST = time.time()
    for i in range(Iterations):
        #print("MCTS iteration",i)
        Node = RootNode
        Chance = RootChance
        
        #### RAVE logic start #########
        #print(Node.GameState.PlayerTurn)
        RAVEMovesToUpdate = [{"Move":[0,0]},{"Move":[0,0]}] #P1/P2, Reward,Visits #RAVE
        ScanPlayer = MCTSPlayer #RAVE
        if RAVE: #RAVE whole
            if Chance in Node.Children:
                for iChild in Node.Children[Chance]:
                    #if str(iChild.IDMove[:-1]) not in RAVEMovesToUpdate[ScanPlayer]:
                    if str(iChild.IDMove) not in RAVEMovesToUpdate[ScanPlayer]:
                        #RAVEMovesToUpdate[ScanPlayer][str(iChild.IDMove[:-1])] = [0,0]
                        RAVEMovesToUpdate[ScanPlayer][str(iChild.IDMove)] = [0,0]
        #### RAVE logic end #########
                
        
        #Selection
        while Node.AvailableChildrenMoves[Chance] == [] and Node.Children[Chance] != []:
            Node = Node.SelectBestChildren(Chance,ExplorationParameter,RAVE)
            if Node.WeightedChances != []: Chance = rd.choice(Node.WeightedChances)
            else: break
            ScanPlayer = 1 - ScanPlayer #RAVE
            if RAVE: #RAVE
                if Chance in Node.Children:
                    for iChild in Node.Children[Chance]:
                        if str(iChild.IDMove) not in RAVEMovesToUpdate[ScanPlayer]:
                            RAVEMovesToUpdate[ScanPlayer][str(iChild.IDMove)] = [0,0]
            #print("NewNode",Node)
            #print("NewChance",Chance)
            #print("NewScanPlayer",ScanPlayer)
            
            
        #Expansion
        if len(Node.AvailableChildrenMoves) > 0: #if not Node.FullyExpanded:
            NextMove = rd.choice(Node.AvailableChildrenMoves[Chance])
            NewState = Node.GameState.CloneState()
            NewState.MakeMove(NextMove)
            Node = Node.AddChild(NewState, NextMove, Chance)
            
        #Simulation / Rollout
        if not LeafParal:
            if RAVE:
                WinnerCount, RAVEMovesToUpdate = Node.GameState.RAVERandomGameToEnd(None,RolloutGames,"Difference",RAVEMovesToUpdate)#Default policy 
            else:
                WinnerCount = Node.GameState.RandomGameToEnd(None,RolloutGames,"Difference")#Default policy 
        else:
            WinnerCount = LeafParallelization(RolloutGames, Node.GameState)
        Reward = (WinnerCount[MCTSPlayer] - WinnerCount[1 - MCTSPlayer]) / RolloutGames * 1.0
        if Node.GameState.PlayerTurn == MCTSPlayer: Reward = -Reward
        #print("RAVEMovesToUpdate 0", RAVEMovesToUpdate[0])
        #print("RAVEMovesToUpdate 1", RAVEMovesToUpdate[1])
        
        #Backpropagation
        while True: #not Node.MoveHistory == []:
            #print()
            Node.Update(Reward)
            Reward = -Reward
            if Node == RootNode: break
            Node = Node.Parent
            
            if RAVE:
                for iChance in Node.AvailableChances:
                    if iChance in Node.Children:
                        for iChild in Node.Children[iChance]:
                            #ChildKey = str(iChild.IDMove[:-1])
                            ChildKey = str(iChild.IDMove)
                            if ChildKey in RAVEMovesToUpdate[Node.GameState.PlayerTurn]:
                                iChild.RAVEReward += RAVEMovesToUpdate[Node.GameState.PlayerTurn][ChildKey][0]
                                iChild.RAVEVisits += RAVEMovesToUpdate[Node.GameState.PlayerTurn][ChildKey][1]
                                #print("RAVE Updated Child with move", ChildKey, "\nChild:", iChild, "RAVER",iChild.RAVEReward, "RAVEV",iChild.RAVEVisits)
            
        
        if time.time() - ST > MaxTime:
            #print("MaxTime reached")
            break
        #input("stop")
    
    SortedChildren = sorted(RootNode.Children[RootChance], key = lambda Child: (Child.Visits,Child.Reward))
    BestNode = SortedChildren[-1]   
    for Child in SortedChildren:
        pass#print(Child)
    BestMove = BestNode.IDMove
    #print("Options:",len(SortedChildren),", Expanded nodes:", i)
    Ologs = " ExpandedNodes " + str(i)
    return Ologs, BestMove



def LeafParallelization(TotalGames, GameState):
    ProcessList = []
    Outputs = Queue()
    #GameNumber = int(TotalGames / os.cpu_count())
    GameNumber = int(TotalGames / 4.0)
    #for i in range(os.cpu_count()):
    for i in range(4):
        ClonedState = GameState.CloneState()
        p = Process(target = RandomGames, args = (GameNumber, ClonedState, Outputs))
        p.daemon = True
        ProcessList.append(p)
    for p in ProcessList:
        p.start()        
    for p in ProcessList:
        p.join()
    WinnerCount = [0,0,0]
    while not Outputs.empty():
        Item = Outputs.get()
        for i in range(len(WinnerCount)):
            WinnerCount[i] += Item[i]
    
    return WinnerCount

def RandomGames(GameNumber, GameState, Outputs):
    WinnerCount = GameState.RandomGameToEnd(None, GameNumber,"Difference")  
    Outputs.put(WinnerCount)
    
def ParallelMCTSearch(GameState, RootChance, MCTSPlayer, MyLock, Outputs, MaxTime = 10000, Iterations = 10000, ExplorationParameter = 2, RolloutGames = 100, ProcessID = 0):
    rd.seed(ProcessID)
    RootNode = CNode(GameState)
    ST = time.time()
    for i in range(Iterations):
        #MyLock.acquire()
        #print("In process ", ProcessID, ", iteration ", i, "random number:", rd.randint(0,10))
        #MyLock.release()
        Node = RootNode
        Chance = RootChance
        
        #Selection
        while Node.AvailableChildrenMoves[Chance] == [] and Node.Children[Chance] != []:
            Node = Node.SelectBestChildren(Chance,ExplorationParameter)
            if Node.WeightedChances != []: Chance = rd.choice(Node.WeightedChances)
            else: break
        #Expansion
        if len(Node.AvailableChildrenMoves) > 0: #if not Node.FullyExpanded:
            NextMove = rd.choice(Node.AvailableChildrenMoves[Chance])
            NewState = Node.GameState.CloneState()
            NewState.MakeMove(NextMove)
            Node = Node.AddChild(NewState, NextMove, Chance)
        #Simulation / Rollout
        WinnerCount = Node.GameState.RandomGameToEnd(None,RolloutGames,"Difference")#Default policy 
        Reward = (WinnerCount[MCTSPlayer] - WinnerCount[1 - MCTSPlayer]) / RolloutGames * 1.0
        if Node.GameState.PlayerTurn == MCTSPlayer: Reward = -Reward
        #Backpropagation
        while True: #not Node.MoveHistory == []:
            Node.Update(Reward)
            Reward = -Reward
            if Node == RootNode: break
            Node = Node.Parent
        
        if time.time() - ST > MaxTime:
            #print("MaxTime reached")
            break

    #MyLock.acquire()
    #print("Options:",len(RootNode.Children[RootChance]),", Expanded nodes:", i)
    #MyLock.release()
    Outputs.put(RootNode.Children[RootChance])

def MCTS(GameState, Chance = None, MaxTime = 10000, Iterations = 10000, ExplorationParameter = 2, RolloutGames = 100, LeafParal = True, RootParal = True, RAVE = False,  RAVEk = 1):
    if RootParal:
        ProcessList = []
        Outputs = Queue()
        MyLock = Lock()
        #print("Parallelized with ", os.cpu_count(), " cores")
        print("Parallelized with 4 cores")
        #for i in range(os.cpu_count()):
        for i in range(4):
            TempState = GameState.CloneState()
            p = Process(target = ParallelMCTSearch, args = (TempState, Chance, TempState.PlayerTurn, MyLock, Outputs, MaxTime, Iterations, ExplorationParameter, RolloutGames, i))
            p.daemon = True
            ProcessList.append(p)
        for p in ProcessList:
            p.start()
        OutputNodes = []
        OutputCounter = 0
        #while OutputCounter < os.cpu_count():
        while OutputCounter < 4:
            if not Outputs.empty():
                Item = Outputs.get()
                OutputNodes.append(Item)
                OutputCounter += 1
                
        for p in ProcessList:
            p.terminate()
        
        Nodes = 0
        for Node in OutputNodes[0]:
            for Line in range(len(OutputNodes)-1):
                Nodes += 1
                if Node in OutputNodes[Line+1]:
                    Node.Visits += OutputNodes[Line+1][OutputNodes[Line+1].index(Node)].Visits
                    Node.Reward += OutputNodes[Line+1][OutputNodes[Line+1].index(Node)].Reward
                    Node.Appearence += 1
        
        UNodes = []
        for Line in range(len(OutputNodes)):
            for Node in Line:
                if Node not in UNodes:
                    UNodes.append(Node)
                    
                
        SortedChildren = sorted(OutputNodes[0], key = lambda Child: (Child.Visits / Child.Appearence, Child.Reward / Child.Appearence))
        BestNode = SortedChildren[-1]   
        for Child in SortedChildren:
            pass#print(Child)
        BestMove = BestNode.IDMove 
        
        Ologs = " ExpandedNodes " + str(Nodes) + " UniqueNodes " + str(len(UNodes))
        
    else:
        if Chance is None: Chance = rd.choice([x for x in GameState.TileIndexList if x in GameState.GetChanceOptions()])
        Ologs, BestMove = MCTSearch(GameState, Chance, GameState.PlayerTurn, MaxTime, Iterations, ExplorationParameter, RolloutGames, LeafParal, RAVE,  RAVEk)
      
    return Ologs, BestMove

