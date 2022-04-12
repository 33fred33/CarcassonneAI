from player.Player import Player

import time

# variables
MaxDepth = 3
L = -100
U = 100

TotalNodes = 0
VisitedNodes = 0
ChanceNodes = 0
VisitedChanceNodes = 0

class Star1(Player):
    
    # Player 1 selects the optimal UCT move 
    # Player 2 selects the worst move from Player 1's position
    
    def __init__(self, currentPlayer = 0, Depth = 0, MaxDepth = 1, Alpha = -float('inf'), Beta = float('inf'), name='Star1', Chance = None, logs=False, logfile=None):
        super().__init__()
        self.currentPlayer = currentPlayer
        self.Depth = Depth
        self.Alpha = Alpha
        self.Beta = Beta
        self.Chance = Chance
        self.MaxDepth = MaxDepth
        self.name = name
        self.fullName = f'Star 1 (Max Depth = {self.MaxDepth})'
        self.family = "Expectimax"
        self.logs = logs
        self.logfile = logfile
        if self.logs:
            self.cols = ['Name','MaxDepth','ProbingFactor','Turn','Time','NodesVisited']
            self.file = self.CreateFile()
        
    def ClonePlayer(self):
        Clone = Star1(self.currentPlayer, self.Depth, self.MaxDepth, self.Alpha, self.Beta, self.name, self.Chance, self.logs, logfile=self.logfile)
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
        data = {'Name': self.name,'MaxDepth':self.MaxDepth,'ProbingFactor': 0,'Turn':int((state.Turn+1)/2), 'Time': time.time()-startTime, 'NodesVisited':VN}
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
        #print("Depth: ",self.Depth," Alpha: ", self.Alpha," Beta: ",self.Beta, " Max Depth: ", self.MaxDepth)
        if state.isGameOver or self.Depth == self.MaxDepth:
            return 0, state.Scores[self.currentPlayer+1] - state.Scores[(2-self.currentPlayer)+2], VN
        else:
            global TotalNodes
            global VisitedNodes
            global ChanceNodes
            global VisitedChanceNodes
            global U
            global L
            #BestMove = None
            
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
            
            CX = 0
            ProbabilityLeft = 1
            ChanceNodes += len(Chances)
            for i in range(len(Chances)):
                VisitedChanceNodes += 1
                
                ProbabilityLeft -= Probabilities[i]
                CAlpha = (self.Alpha - CX - U * ProbabilityLeft) / Probabilities[i]
                CBeta = (self.Beta - CX - L * ProbabilityLeft) / Probabilities[i]
                AX = max(L,CAlpha)
                BX = min(U,CBeta)
                Moves = state.availableMoves(TileIndexOther = Chances[i])
                
                #Sort moves
                Moves = sorted(Moves, key = self.GetMoveKey)
                TotalNodes += len(Moves)
                
                if state.playerSymbol == self.currentPlayer: 
                    BestValue = -float('inf')                
                    for Move in Moves: 
                        VisitedNodes += 1
                        VN += 1
                        NewState = state.CloneState()
                        NewState.move(Move.move)
                        _, MoveValue, VN = Star1(self.currentPlayer, self.Depth +1, self.MaxDepth, AX, BX).bestMove(NewState, VN)
                        if MoveValue > BestValue:
                            BestMove = Move.move
                            BestValue = MoveValue
                            #print(f'(Current Player) New Best Move: Move:{BestMove}, Value:{MoveValue}')
                        AX = max(AX, MoveValue)
                        if BX <= AX:
                            break                           
                else: 
                    BestValue = float('inf')
                    for Move in Moves: 
                        VisitedNodes += 1
                        VN += 1
                        NewState = state.CloneState()
                        NewState.move(Move.move)
                        _, MoveValue, VN = Star1(self.currentPlayer, self.Depth +1, self.MaxDepth, AX, BX).bestMove(NewState, VN)
                        if MoveValue < BestValue:
                            BestMove = Move.move
                            BestValue = MoveValue
                            #print(f'(Other Player) New Best Move: Move:{BestMove}, Value:{MoveValue}')
                        BX = min(BX,MoveValue)
                        if BX <= AX: 
                            break 
                        
                #print("BestValue: ",BestValue,"BestMove: ",BestMove,"CAlpha: ",CAlpha,"CBeta: ",CBeta)
                if BestValue >= CBeta:
                    return 0, self.Beta, VN
                elif BestValue <= CAlpha:
                    return 0, self.Alpha, VN
                CX += Probabilities[i] * BestValue
            return BestMove, CX, VN


