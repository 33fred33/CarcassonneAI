from player.Player import Player

import os
import pandas as pd
import time

# variables
MaxDepth = 3
L = -100
U = 100

TotalNodes = 0
VisitedNodes = 0
ChanceNodes = 0
VisitedChanceNodes = 0

class Star2_5(Player):
    
    # Player 1 selects the optimal UCT move 
    # Player 2 selects the worst move from Player 1's position
    
    def __init__(self, currentPlayer = 0, Depth = 0, MaxDepth = 1, Alpha = -float('inf'), Beta = float('inf'), name='Star2.5', ProbingFactor = 4, Chance = None, logs = False, logfile=None):
        super().__init__()
        self.currentPlayer = currentPlayer
        self.Depth = Depth
        self.MaxDepth = MaxDepth
        self.Alpha = Alpha
        self.Beta = Beta
        self.Chance = Chance
        self.ProbingFactor = ProbingFactor
        self.name = name
        self.fullName = f'Star 2.5 (Max Depth = {self.MaxDepth}, Probing Factor = {self.ProbingFactor})'
        self.family = "Expectimax"
        self.logs = logs
        self.logfile = logfile
        if self.logs:
            self.cols = ['Name','MaxDepth','ProbingFactor','Turn','Time','NodesVisited']
            self.file = self.CreateFile(self.cols, 'Stats')
            
        
    def ClonePlayer(self):
        Clone = Star2_5(self.currentPlayer, self.Depth, self.MaxDepth, self.Alpha, self.Beta, self.name, self.ProbingFactor, self.Chance, self.logs, logfile=self.logfile)
        return Clone
    
    
    def chooseAction(self, state):
        """
        Choose actions using UCT function
        """
        # assign current player
        self.currentPlayer = state.playerSymbol
        self.Chance = state.nextTileIndex()
        
        # keep track of time
        startTime = time.time()
        move, CX, VN = self.bestMove(state)
        endTime = time.time()
        
        if (state.Turn % 10 == 0):
            print(f'({self.name})   TimeTaken: {round(endTime - startTime,3)} secs  -  Turn: {state.Turn}  -  Time:{time.strftime("%H:%M:%S", time.localtime())}')
        
        # append info to csv
        data = {'Name': self.name,'MaxDepth':self.MaxDepth,'ProbingFactor': self.ProbingFactor,'Turn':int((state.Turn+1)/2), 'Time': time.time()-startTime, 'NodesVisited':VN}
        self.UpdateFile(data)
            
        if move == 0:
            move = state.getRandomMove().move
        return move
    
    
    def GetMoveKey(self, Move): #Game specific
        Move = Move.move
        if Move[4] is None:
            Key = 10
        else:
            if Move[4][0] == 'C':
                Key = 1
            elif Move[4][0] == 'Monastery':
                Key = 2
            elif Move[4][0] == 'R':
                Key = 3
            elif Move[4][0] == 'G':
                Key = 11
            else: Key == 100 #Never happens
        return Key 
    
    
    def getChanceOptions(self, state, GiveProbability = False):
        # initialize vectors
        Tiles = []
        Probabilities = []
        # list the tile numbers still available
        NewList = [x for x in state.TileIndexList]
        
        for TileIndex in set(state.TileIndexList):
            # available moves for tile
            if state.availableMoves(TilesOnly = True, TileIndexOther = TileIndex) == []: 
                # remove from list
                NewList = [x for x in NewList if x != TileIndex]
            else:
                # append to tiles to test
                Tiles.append(TileIndex)
        if NewList != []:
            for TileIndex in Tiles:
                if GiveProbability:
                    OccurrenciesCount = len([x for x in NewList if x == TileIndex])
                    Probability = OccurrenciesCount*1.0 / len(NewList)
                    Probabilities.append(Probability)  
        else:
            state.EndGameRoutine()
        # return all tiles and probabilities
        return Tiles, Probabilities 
    
    
    
    def bestMove(self, state, VN=0):
        if state.isGameOver or self.Depth == self.MaxDepth:
            return 0, state.Scores[self.currentPlayer+1] - state.Scores[(2-self.currentPlayer)+2], VN
        
        else:
            global VisitedNodes
            global VisitedChanceNodes
            U = 100
            L = -100
            
            if self.Chance is None: 
                Chances,Probabilities = self.getChanceOptions(state, GiveProbability = True)
                #Sort chances from largest to smallest
                IndexedProbs = [[i,Probabilities[i]] for i in range(len(Probabilities))]
                OrderedIndexedProbs = sorted(IndexedProbs, key = lambda Index: Index[1], reverse=True)
                Chances = [Chances[i] for i in [x[0] for x in OrderedIndexedProbs]]
                Probabilities = [x[1] for x in OrderedIndexedProbs]
            else:
                Chances = [self.Chance]
                Probabilities = [1]
            
            #Probing phase
            CX = 0
            ProbabilityLeft = 1
            CW = 0
            CAlpha = (self.Alpha - U * (1 - Probabilities[0])) / Probabilities[0]
            AX = max(L, CAlpha)
            
            for i in range(len(Chances)):
                ProbabilityLeft -= Probabilities[i]
                CBeta = (self.Beta - CX - L * ProbabilityLeft) / Probabilities[i]
                BX = min(U,CBeta)
                Moves = state.availableMoves(TileIndexOther = Chances[i])
                
                #Sort moves
                Moves = sorted(Moves, key = self.GetMoveKey)
                if len(Moves) > self.ProbingFactor:
                    Its = self.ProbingFactor
                else:
                    Its = len(Moves)
                
                MoveValue = 0
                for j in range(Its):               
                    NewState = state.CloneState()
                    NewState.move(Moves[j].move)
                    _, TempValue, VN = Star2_5(self.currentPlayer, self.Depth +1, self.MaxDepth, AX, BX, self.name, self.ProbingFactor).bestMove(NewState, VN)                
                    if TempValue >= BX:
                        MoveValue = BX
                    elif TempValue > AX:
                        MoveValue = TempValue
                    else:
                        MoveValue = AX
                CW += MoveValue
                if MoveValue >= CBeta:
                    return 0, self.Beta, VN
                CX += Probabilities[i] * MoveValue
                
            #Star1 (CW modified)
            CX = 0
            ProbabilityLeft = 1
            #ChanceNodes += len(Chances)
            for i in range(len(Chances)):
                VisitedChanceNodes += 1
                ProbabilityLeft -= Probabilities[i]
                CAlpha = (self.Alpha - CX - U * ProbabilityLeft) / Probabilities[i]
                CBeta = (self.Beta - CX - CW) / Probabilities[i]
                AX = max(L,CAlpha)
                BX = max(U,CBeta)
                Moves = state.availableMoves(TileIndexOther = Chances[i])
                #Sort moves
                Moves = sorted(Moves, key = self.GetMoveKey)
                #TotalNodes += len(Moves)
                if state.playerSymbol == self.currentPlayer: 
                    BestValue = -float('inf')                
                    for Move in Moves: 
                        VisitedNodes += 1
                        VN += 1
                        NewState = state.CloneState()
                        NewState.move(Move.move)
                        _, MoveValue, VN = Star2_5(self.currentPlayer, self.Depth +1, self.MaxDepth, AX, BX, self.name, self.ProbingFactor).bestMove(NewState, VN)       
                        if MoveValue > BestValue:
                            BestMove = Move.move
                            BestValue = MoveValue
                        AX = max(AX,MoveValue)
                        if BX <= AX:
                            break                           
                else: 
                    BestValue = float('inf')
                    for Move in Moves: 
                        VisitedNodes += 1
                        VN += 1
                        NewState = state.CloneState()
                        NewState.move(Move.move)
                        _, MoveValue, VN = Star2_5(self.currentPlayer, self.Depth +1, self.MaxDepth, AX, BX, self.name, self.ProbingFactor).bestMove(NewState, VN)       
                        if MoveValue < BestValue:
                            BestMove = Move.move
                            BestValue = MoveValue
                        BX = min(BX,MoveValue)
                        if BX <= AX: 
                            break 
                #print("BestValue",BestValue,"BestMove",BestMove,"CAlpha",CAlpha,"CBeta",CBeta)
                if BestValue >= CBeta:
                    return 0, self.Beta, VN
                elif BestValue <= CAlpha:
                    return 0, self.Alpha, VN
                CX += Probabilities[i] * BestValue
            return BestMove, CX, VN                
                
                
                
                
                
                
                

