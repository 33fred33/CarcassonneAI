 # -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:23:59 2019

@author: user
"""

ShowLogs = False
RecordLogs = True
MaxDepth = 3
Method = 0 #0:Expectimax, 1:Star1, 2:Star2, 3:Star2.5
L = -100
U = 100

TotalNodes = 0
VisitedNodes = 0
ChanceNodes = 0
VisitedChanceNodes = 0
    
def FindBestMove(GameState, GivenChance = None, NewMaxDepth = 3, NewMethod = 0):
    global Method
    global MaxDepth
    global TotalNodes
    global VisitedNodes
    global ChanceNodes
    global VisitedChanceNodes
    TotalNodes = 0
    VisitedNodes = 0
    ChanceNodes = 0
    VisitedChanceNodes = 0
    Method = NewMethod
    MaxDepth = NewMaxDepth
    MaxPlayer = GameState.PlayerTurn
    #BestMove, _ = Negamax(GameState, Chance, MaxPlayer, Depth = 0, Alpha = -float('inf'), Beta = float('inf'))
    if NewMethod == 1:
        BestMove, _ = MyStar1(GameState, MaxPlayer, 0, Alpha = -float('inf'), Beta = float('inf'), Chance = GivenChance)
    elif NewMethod == 0:
        BestMove, _ = MyExpectimax(GameState, MaxPlayer, 0, Alpha = -float('inf'), Beta = float('inf'), Chance = GivenChance)
    elif NewMethod == 2:
        BestMove, _ = MyStar2(GameState, MaxPlayer, 0, Alpha = -float('inf'), Beta = float('inf'), Chance = GivenChance)
    elif NewMethod == 3:
        BestMove, _ = MyStar25(GameState, MaxPlayer, 0, Alpha = -float('inf'), Beta = float('inf'), ProbingFactor = 5, Chance = GivenChance)
    #print("TotalNodes", TotalNodes, "Pruned nodes:", TotalNodes - VisitedNodes)
    #print("Chance nodes", ChanceNodes, "Pruned ChanceNodes", ChanceNodes - VisitedChanceNodes)
    Ologs = " VisitedNodes " + str(VisitedNodes) + " VisitedChanceNodes " + str(VisitedChanceNodes)
    return Ologs, BestMove

def MyStar1 (GameState, MaxPlayer, Depth = 0, Alpha = -float('inf'), Beta = float('inf'), Chance = None):
    if ShowLogs: print("Depth",Depth,"Alpha",Alpha,"Beta",Beta)
    if GameState.Terminal or Depth == MaxDepth:
        return 0, GameState.Scores[MaxPlayer+2] - GameState.Scores[(1-MaxPlayer)+2]
    else:
        global TotalNodes
        global VisitedNodes
        global ChanceNodes
        global VisitedChanceNodes
        global U
        global L
        if Chance is None: 
            Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
            #Sort chances from largest to smallest
            IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
            OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
            Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
            Probabilities = [x[1] for x in OrderedIndexedProbs]
        else:
            Chances = [Chance]
            Probabilities = [1]
        CX = 0
        ProbabilityLeft = 1
        ChanceNodes += len(Chances)
        for i in range(len(Chances)):
            VisitedChanceNodes += 1
            if ShowLogs: print("Chance",Chance,"Probabilities",Probabilities[i])
            ProbabilityLeft -= Probabilities[i]
            CAlpha = (Alpha - CX - U * ProbabilityLeft) / Probabilities[i]
            CBeta = (Beta - CX - L * ProbabilityLeft) / Probabilities[i]
            AX = max(L,CAlpha)
            BX = min(U,CBeta)
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            TotalNodes += len(Moves)
            if GameState.PlayerTurn == MaxPlayer: 
                BestValue = -float('inf')                
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Max")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar1(NewState, MaxPlayer, Depth +1, AX, BX)
                    if MoveValue > BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    AX = max(AX,MoveValue)
                    if BX <= AX:
                        break                           
            else: 
                BestValue = float('inf')
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Min")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar1(NewState, MaxPlayer, Depth +1, AX, BX)
                    if MoveValue < BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    BX = min(BX,MoveValue)
                    if BX <= AX: 
                        break 
            if ShowLogs: print("BestValue",BestValue,"BestMove",BestMove,"CAlpha",CAlpha,"CBeta",CBeta)
            if ShowLogs:input("Pause")
            if BestValue >= CBeta:
                return 0, Beta
            elif BestValue <= CAlpha:
                return 0, Alpha
            CX += Probabilities[i] * BestValue
        return BestMove, CX
    
def MyExpectimax (GameState, MaxPlayer, Depth = 0, Alpha = -float('inf'), Beta = float('inf'), Chance = None):
    if ShowLogs: print("Depth",Depth,"Alpha",Alpha,"Beta",Beta)
    if GameState.Terminal or Depth == MaxDepth:
        if ShowLogs: print("Returned score",GameState.Scores[MaxPlayer+2] - GameState.Scores[(1-MaxPlayer)+2])
        return 0, GameState.Scores[MaxPlayer+2] - GameState.Scores[(1-MaxPlayer)+2]
    else:
        global TotalNodes
        global VisitedNodes
        global ChanceNodes
        global VisitedChanceNodes
        if Chance is None: 
            Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
            #Sort chances from largest to smallest
            IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
            OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
            Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
            Probabilities = [x[1] for x in OrderedIndexedProbs]
        else:
            Chances = [Chance]
            Probabilities = [1]
        Value = 0
        ChanceNodes += len(Chances)
        for i in range(len(Chances)):
            VisitedChanceNodes += 1
            if ShowLogs: print("Chance",Chances[i],"Probabilities",Probabilities[i])
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            TotalNodes += len(Moves)
            if GameState.PlayerTurn == MaxPlayer: 
                BestValue = -float('inf')                
                for Move in Moves:
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Max")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyExpectimax(NewState, MaxPlayer, Depth +1, Alpha, Beta)
                    if MoveValue > BestValue:
                        BestMove = Move
                        BestValue = MoveValue                          
            else: 
                BestValue = float('inf')
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Min")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyExpectimax(NewState, MaxPlayer, Depth +1, Alpha, Beta)
                    if MoveValue < BestValue:
                        BestMove = Move
                        BestValue = MoveValue
            Value += BestValue * Probabilities[i]
            if ShowLogs:
                print("Value",Value,"BestValue",BestValue,"BestMove",BestMove,"Depth",Depth,"\n")
                input("Finished Depth")
        return BestMove, Value
    
def MyStar2 (GameState, MaxPlayer, Depth = 0, Alpha = -float('inf'), Beta = float('inf'), Chance = None):
    if ShowLogs: print("Depth",Depth,"Alpha",Alpha,"Beta",Beta)
    if GameState.Terminal or Depth == MaxDepth:
        return 0, GameState.Scores[MaxPlayer+2] - GameState.Scores[(1-MaxPlayer)+2]
    else:
        global TotalNodes
        global VisitedNodes
        global ChanceNodes
        global VisitedChanceNodes
        global U
        global L
        if Chance is None: 
            Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
            #Sort chances from largest to smallest
            IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
            OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
            Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
            Probabilities = [x[1] for x in OrderedIndexedProbs]
        else:
            Chances = [Chance]
            Probabilities = [1]
            
        #Probing phase
        CX = 0
        ProbabilityLeft = 1
        CW = 0
        CAlpha = (Alpha - U * (1 - Probabilities[0])) / Probabilities[0]
        AX = max(L, CAlpha)
        for i in range(len(Chances)):
            ProbabilityLeft -= Probabilities[i]
            CBeta = (Beta - L * ProbabilityLeft - CX) / Probabilities[i]
            BX = min(U, CBeta)
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            NewState = GameState.CloneState()
            NewState.MakeMove(Moves[0])
            _, MoveValue = MyStar2(NewState, MaxPlayer, Depth +1, AX, BX)
            CW += MoveValue
            if MoveValue >= CBeta:
                return 0, Beta
            CX += Probabilities[i] * MoveValue
        #Star1 (CW modified) 
        CX = 0
        ProbabilityLeft = 1
        ChanceNodes += len(Chances)
        for i in range(len(Chances)):
            VisitedChanceNodes += 1
            if ShowLogs: print("Chance",Chance,"Probabilities",Probabilities[i])
            ProbabilityLeft -= Probabilities[i]
            CAlpha = (Alpha - CX - U * ProbabilityLeft) / Probabilities[i]
            CBeta = (Beta - CX - CW) / Probabilities[i]
            AX = max(L,CAlpha)
            BX = max(U,CBeta)
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            TotalNodes += len(Moves)
            if GameState.PlayerTurn == MaxPlayer: 
                BestValue = -float('inf')                
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Max")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar2(NewState, MaxPlayer, Depth +1, AX, BX)
                    if MoveValue > BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    AX = max(AX,MoveValue)
                    if BX <= AX:
                        break                           
            else: 
                BestValue = float('inf')
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Min")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar2(NewState, MaxPlayer, Depth +1, AX, BX)
                    if MoveValue < BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    BX = min(BX,MoveValue)
                    if BX <= AX: 
                        break 
            if ShowLogs: print("BestValue",BestValue,"BestMove",BestMove,"CAlpha",CAlpha,"CBeta",CBeta)
            if ShowLogs:input("Pause")
            if BestValue >= CBeta:
                return 0, Beta
            elif BestValue <= CAlpha:
                return 0, Alpha
            CX += Probabilities[i] * BestValue
        return BestMove, CX
    
def MyStar25 (GameState, MaxPlayer, Depth = 0, Alpha = -float('inf'), Beta = float('inf'), ProbingFactor = 5, Chance = None):
    if ShowLogs: print("Depth",Depth,"Alpha",Alpha,"Beta",Beta)
    if GameState.Terminal or Depth == MaxDepth:
        return 0, GameState.Scores[MaxPlayer+2] - GameState.Scores[(1-MaxPlayer)+2]
    else:
        #global TotalNodes
        global VisitedNodes
        #global ChanceNodes
        global VisitedChanceNodes
        #global U
        #global L
        U = 100
        L = -100
        
        if Chance is None: 
            Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
            #Sort chances from largest to smallest
            IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
            OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
            Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
            Probabilities = [x[1] for x in OrderedIndexedProbs]
        else:
            Chances = [Chance]
            Probabilities = [1]
            
        #Probing phase
        CX = 0
        ProbabilityLeft = 1
        CW = 0
        CAlpha = (Alpha - U * (1 - Probabilities[0])) / Probabilities[0]
        AX = max(L, CAlpha)
        for i in range(len(Chances)):
            ProbabilityLeft -= Probabilities[i]
            CBeta = (Beta - L * ProbabilityLeft - CX) / Probabilities[i]
            BX = min(U, CBeta)
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            if len(Moves) > ProbingFactor:
                Its = ProbingFactor
            else:
                Its = len(Moves)
            for j in range(Its):               
                NewState = GameState.CloneState()
                NewState.MakeMove(Moves[j])
                _, TempValue = MyStar25(NewState, MaxPlayer, Depth +1, AX, BX)
                if TempValue >= BX:
                    MoveValue = BX
                elif TempValue > AX:
                    MoveValue = TempValue
                else:
                    MoveValue = AX
            CW += MoveValue
            if MoveValue >= CBeta:
                return 0, Beta
            CX += Probabilities[i] * MoveValue
        #Star1 (CW modified) 
        CX = 0
        ProbabilityLeft = 1
        #ChanceNodes += len(Chances)
        for i in range(len(Chances)):
            VisitedChanceNodes += 1
            if ShowLogs: print("Chance",Chance,"Probabilities",Probabilities[i])
            ProbabilityLeft -= Probabilities[i]
            CAlpha = (Alpha - CX - U * ProbabilityLeft) / Probabilities[i]
            CBeta = (Beta - CX - CW) / Probabilities[i]
            AX = max(L,CAlpha)
            BX = max(U,CBeta)
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            #TotalNodes += len(Moves)
            if GameState.PlayerTurn == MaxPlayer: 
                BestValue = -float('inf')                
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Max")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar25(NewState, MaxPlayer, Depth +1, AX, BX, ProbingFactor)
                    if MoveValue > BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    AX = max(AX,MoveValue)
                    if BX <= AX:
                        break                           
            else: 
                BestValue = float('inf')
                for Move in Moves: 
                    VisitedNodes += 1
                    if ShowLogs: print("Move",Move,"from",len(Moves),"Min")
                    NewState = GameState.CloneState()
                    NewState.MakeMove(Move)
                    _, MoveValue = MyStar25(NewState, MaxPlayer, Depth +1, AX, BX, ProbingFactor)
                    if MoveValue < BestValue:
                        BestMove = Move
                        BestValue = MoveValue
                    BX = min(BX,MoveValue)
                    if BX <= AX: 
                        break 
            if ShowLogs: print("BestValue",BestValue,"BestMove",BestMove,"CAlpha",CAlpha,"CBeta",CBeta)
            if ShowLogs:input("Pause")
            if BestValue >= CBeta:
                return 0, Beta
            elif BestValue <= CAlpha:
                return 0, Alpha
            CX += Probabilities[i] * BestValue
        return BestMove, CX

def Negamax (GameState, Chance, MaxPlayer, Depth, Alpha, Beta): #Missing pruning with alpha, beta
    global TotalNodes                                                          #Data
    global TotalLeafNodes                                                      #Data
    if ShowLogs: print("Negamax, Chance",Chance,"Depth",Depth)
    #input("Input")
    Score = -float('inf')
    Moves = GameState.GetAvailableMoves(Chance)
    Moves = sorted(Moves, key = GetMoveKey)
    TotalNodes += len(Moves)                                                   #Data
    if Depth == MaxDepth: TotalLeafNodes += len(Moves)                         #Data
    for Move in Moves:
        if ShowLogs: print("Move",Move)
        NewState = GameState.CloneState()
        NewState.MakeMove(Move)
        if Method == 0:
            Value = -Expectimax(NewState, MaxPlayer, Depth, Alpha, Beta)
            #Score = max(Value, Score)
            if Depth == 0:
                print("Move Value",Value, "Move",Move)
            if Value > Score:
                BestMove = Move
                Score = Value
        elif Method == 1:
            Value = -Star1(GameState, MaxPlayer, Depth, Alpha, Beta)
            if Value < Alpha:
                return Alpha
            elif Value > Beta:
                return Beta
                    
        elif Method == 2:
            Value = -Star2
        elif Method == 3:
            Value = -Star25
        
    if ShowLogs: print("Return Score",Score, "BestMove", BestMove)
    if Depth == 0:
        print("Score",Score,"BestMove",BestMove)
        input("t")
    return BestMove, Score

def Expectimax (GameState, MaxPlayer, Depth, Alpha, Beta):
    if ShowLogs: print("Expectimax,Depth",Depth)
    if GameState.Terminal or Depth == MaxDepth:
        if ShowLogs: print("Return evaluation:",GameState.Scores[MaxPlayer + 2] - GameState.Scores[(1 - MaxPlayer) + 2])
        return GameState.Scores[MaxPlayer + 2] - GameState.Scores[(1 - MaxPlayer) + 2]
    Score = 0
    Chances, Probabilities = GameState.GetChanceOptions(GiveProbability = True)
    for i in range(len(Chances)):           
        Chance = Chances[i]
        _, Value = Negamax(GameState, Chance, MaxPlayer, Depth + 1, Alpha, Beta)
        Score += Value * Probabilities[i]
    if ShowLogs: print("Return Score",Score)
    return Score

def Star1 (GameState, MaxPlayer, Depth, Alpha, Beta):
    if ShowLogs: print("Star1,Depth",Depth)
    if GameState.Terminal or Depth == MaxDepth:
        if ShowLogs: print("Return evaluation:",GameState.Scores[MaxPlayer + 2] - GameState.Scores[(1 - MaxPlayer) + 2])
        return GameState.Scores[MaxPlayer + 2] - GameState.Scores[(1 - MaxPlayer) + 2]
    Chances, Probabilities = GameState.GetChanceOptions(GiveProbability = True)
    #<Sort Chances according to probabilities>
    IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
    OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
    Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
    Probabilities = [x[1] for x in OrderedIndexedProbs]
    #</Sort Chances according to probabilities>
    CX = 0
    CY = 1
    for i in range(len(Chances)):
        CY -= Probabilities[i]
        CAlpha = (Alpha - CX - U * CY)/Probabilities[i]
        CBeta = (Beta - CX - L * CY)/Probabilities[i]
        AX = max(L, CAlpha)
        BX = max(U, CBeta)
        Value = Negamax(GameState, Chances[i], MaxPlayer, Depth+1, AX, BX)
        if Value >= CBeta: return Beta
        if Value <= CAlpha: return Alpha
        CX += Probabilities[i]*Value
    return CX
    

def GetMoveKey(Move): #Game specific
    if Move[4] is None:
        Key = 10
    else:
        if Move[4][0] == 'C':
            Key = 1
        elif Move[4][0] == 'Cloister':
            Key = 2
        elif Move[4][0] == 'R':
            Key = 3
        elif Move[4][0] == 'G':
            Key = 11
        else: Key == 100 #Never happens
    return Key            



















"""
def Expectimax (GameState, ExpectimaxPlayer = 0, MaxDepth = 3, Depth = 0):
    if GameState.Terminal or Depth == MaxDepth:
        return GameState.Scores[ExpectimaxPlayer+2] - GameState.Scores[(1-ExpectimaxPlayer)+2]
    else:
        Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
        Value = 0
        for i in range(len(Chances)):           
            Chance = Chances[i]
            Moves = GameState.GetAvailableMoves(Chance)
            #Sort moves
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

def PrunedExpectimax (GameState, ExpectimaxPlayer = 0, MaxDepth = 3, Depth = 0, Alpha = -float('inf'), Beta = float('inf')):
    if GameState.Terminal or Depth == MaxDepth:
        return GameState.Scores[ExpectimaxPlayer+2] - GameState.Scores[(1-ExpectimaxPlayer)+2]
    else:
        Chances,Probabilities = GameState.GetChanceOptions(GiveProbability = True)
        #Sort chances from largest to smallest
        IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
        OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1],reverse=True)
        Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
        Probabilities = [x[1] for x in OrderedIndexedProbs]
        Value = 0
        for i in range(len(Chances)):           
            Moves = GameState.GetAvailableMoves(Chances[i])
            #Sort moves
            Moves = sorted(Moves, key = GetMoveKey)
            MaxValue = -float('inf')
            MinValue = float('inf')
            NodesCount = 0
            for Move in Moves: 
                NewState = GameState.CloneState()
                NewState.MakeMove(Move)
                MoveValue = PrunedExpectimax(NewState, ExpectimaxPlayer, MaxDepth, Depth +1, Alpha, Beta)
                if GameState.PlayerTurn == ExpectimaxPlayer: 
                    BestValue = max(MaxValue,MoveValue)
                    Alpha = max(Alpha,MoveValue)
                    NodesCount += 1
                    if Beta <= Alpha: 
                        print("Chance",Chances[i],"From",len(Moves),", only",NodesCount,". Depth",Depth,"Max, alpha",Alpha,"beta",Beta)
                        break
                else: 
                    BestValue = min(MinValue,MoveValue)
                    Beta = min(Beta,MoveValue)
                    NodesCount += 1
                    if Beta <= Alpha:
                        print("Chance",Chances[i],"From",len(Moves),", only",NodesCount,". Depth",Depth,"Min, alpha",Alpha,"beta",Beta)
                        break
            if NodesCount == len(Moves): print("Chance",Chances[i],"All ",len(Moves),". Depth",Depth,"alpha",Alpha,"beta",Beta)
            Value += Probabilities[i]*BestValue
        return Value
"""