from player.Player import Player

import time
import random
import numpy as np

class MCTSPlayer(Player):
    
    # Player 1 selects the optimal UCT move 
    # Player 2 selects the worst move from Player 1's position
    
    def __init__(self, iterations = 500, timeLimit = 10, isTimeLimited = False, c_param = 1, logs=False, logfile=None, name='MCTS_V', detailed_logs=True):
        super().__init__()
        self.iterations = iterations
        self.timeLimit = timeLimit
        self.isTimeLimited = isTimeLimited
        self.c_param = c_param
        self.name = name
        self.fullName = f'MCTS (Time Limit = {self.timeLimit})' if self.isTimeLimited else  f'MCTS (Iterations = {self.iterations})'
        self.family = "MCTS"
        self.logs = logs
        self.logfile = logfile
        self.latest_root_node = None #added
        self.nodes_dict = {} #added
        self.id_count = 0 #added
        self.detailed_logs = detailed_logs
        if self.logs:
            self.cols = ['Name','Simulations','Turn','TimeTaken']
            self.file = self.CreateFile(self.cols, 'Stats')
        
    def test_seed(self):
        print(random.randint(0,99999))
                
    def ClonePlayer(self):
        Clone = MCTSPlayer(iterations=self.iterations, timeLimit=self.timeLimit, isTimeLimited = self.isTimeLimited, 
                           c_param=self.c_param, logs=self.logs, logfile=self.logfile, name=self.name, detailed_logs=self.detailed_logs)
        return Clone
    
    
    def chooseAction(self, state):
        """
        Choose actions using UCT function
        """
        return self.MCTS_Search(state, self.iterations, self.timeLimit, self.isTimeLimited)
    
    
    
    def MCTS_Search(self, root_state, iterations, timeLimit, isTimeLimited):
        """
        Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with games results in the range [0, 1]
        """
        # Player 1 = 1, Player 2 = 2 (Player 2 wants to the game to be a loss)
        playerSymbol = root_state.playerSymbol
        self.latest_root_node = None #added
        
        # state the Root Node
        root_node = Node(state = root_state)
        self.nodes_dict = {0:root_node} #added
        self.id_count = 0 #added
        if self.isTimeLimited:
            self.MCTS_TimeLimit(root_node, root_state)
        else:
            self.MCTS_IterationLimit(root_node, root_state)
                
        # return the node with the highest number of wins from the view of the current player
        if playerSymbol == 1:
            bestMove = sorted(root_node.child, key = lambda c: c.Q)[-1].Move
        else:
            bestMove = sorted(root_node.child, key = lambda c: c.Q)[0].Move
        
        self.latest_root_node=root_node
        return bestMove.move
    
    
    
    def MCTS_IterationLimit(self, root_node, root_state):
        startTime = time.time()
        
        # copy 
        state = root_state.CloneState()
        
        # first simulation
        self.Rollout(root_node, state)
        self.Backpropogate(root_node, state)
        
        # iterate for each simulation
        for i in range(self.iterations-1):
            node = root_node
            state = root_state.CloneState()
            # 4 steps
            node = self.Select(node, state)
            node = self.Expand(node, state)
            self.Rollout(node, state)
            self.Backpropogate(node, state)
            
        endTime = time.time()
        if (root_state.Turn % 10 == 0):
            print(f'({self.name})   TimeTaken: {round(endTime - startTime,3)} secs  -  Turn: {root_state.Turn}  -  Time:{time.strftime("%H:%M:%S", time.localtime())}')
        # append info to csv
        if self.logs:  #ADD TREE STRUCTURE LOGS
            data = {'Name': self.name,'Simulations':self.iterations,'Turn':int((root_state.Turn+1)/2), 'TimeTaken':(endTime - startTime)}
            self.UpdateFile(data)
    
    
    
    # 4 steps of MCTS
    def Select(self, node, state):
        # Select
        while node.untried_moves == [] and node.child != []:  # node is fully expanded
            node = node.UCTSearch(self.c_param)
            state.move(node.Move.move)
        return node
    
    def Expand(self, node, state):
        # Expand
        if node.untried_moves != [] and (not state.isGameOver):  # if we can expand, i.e. state/node is non-terminal
            move_random = random.choice(node.untried_moves)
            state.move(move_random.move)
            self.id_count = self.id_count + 1 #added
            node = node.AddChild(move = move_random, state = state, isGameOver = state.isGameOver,child_id = self.id_count) #mod
            self.nodes_dict[self.id_count] = node #added
            
            
        return node
    
    def Rollout(self, node, state):
        # Rollout - play random moves until the game reaches a terminal state
        state.shuffle()  # shuffle deck
        while not state.isGameOver:
            m = state.getRandomMove()
            state.move(m.move)
              
    def Backpropogate(self, node, state):
        # Backpropogate
        result = state.checkWinner()
        while node != None:  # backpropogate from the expected node and work back until reaches root_node
            node.UpdateNode(result, self.c_param)
            node = node.parent
    
    
    def MCTS_TimeLimit(self, root_node, root_state):
        
        startTime = endTime = time.time()
        
        # copy 
        state = root_state.CloneState()
        
        # first simulation
        self.Rollout(root_node, state)
        self.Backpropogate(root_node, state)
        
        numberOfIterations = 1
        
        while ((endTime - startTime) < self.timeLimit):
            numberOfIterations += 1
            
            node = root_node
            state = root_state.CloneState()
            
            # 4 steps
            node = self.Select(node, state)
            node = self.Expand(node, state)
            self.Rollout(node, state)
            self.Backpropogate(node, state)
            
            endTime = time.time()
            
            
            
##############################################################################
##############################################################################
##############################################################################


class Node:
    """
    The Search Tree is built of Nodes
    A node in the search tree
    """
    
    def __init__(self, Move = None, parent = None, state = None, isGameOver = False, id = 0):#mod
        self.Move = Move  # the move that got us to this node - "None" for the root
        self.parent = parent  # parent node of this node - "None" for the root node
        self.child = []  # list of child nodes
        self.state = state
        self.id = id #added
        self.untried_moves = state.availableMoves()
        self.playerSymbol = state.playerSymbol
        # keep track of visits/wins/losses
        self.visits = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.Q = 0

        
    
    def __repr__(self):
        visits = 1 if self.visits == 0 else self.visits
        move = str(None) if (self.Move is None) else str(self.Move.move)
        String = "["
        String += f'Move:{move}, Wins:{round(self.wins,1)},'
        String += f' Losses:{self.losses}, Draws:{self.draws}, Q:{round(self.Q,3)},'
        String += f' Wins/Visits:{round(self.wins,1)}/{self.visits} ({round(self.wins/visits,3)}),'
        String += f' Remaining Moves:{len(self.untried_moves)}'
        String += "]"
        
        return String
    
    def AddChild(self, move, state, isGameOver, child_id):#mod
        """
        Add new child node for this move remove m from list of untried_moves.
        Return the added child node.
        """
        node = Node(Move = move, state = state, isGameOver = isGameOver, parent = self, id = child_id)#mod
        self.untried_moves.remove(move)  # this move is now not available
        self.child.append(node)
        return node
    
    
    def UpdateNode(self, result, c_param):
        """
        Update result and number of visits of node
        """
        self.visits += 1
        self.wins += (result > 0)
        self.losses += (result < 0)
        self.draws += (result == 0)
        self.Q = self.Q + (result - self.Q)/self.visits
        
    
    def SwitchNode(self, move, state):
        """
        Switch node to new state
        """
        # if node has children
        for i in self.child:
            if i.Move == move:
                return i
        
        # if node has no children
        return self.AddChild(move, state)
    
    
    def UCTSearch(self, c_param):
        """
        Use the UCB1 formula to select the best child node from the children array.
        C_PARAM is an exploration-explotation factor
        """
        if self.playerSymbol == 1:
            #  look for maximum output
            choice_weights = [c.Q + (2 * c_param * np.sqrt(2 * np.log(self.visits) / c.visits)) for c in self.child]
            return self.child[np.argmax(choice_weights)]
        else: 
            #  look for minimum output
            choice_weights = [c.Q - (2 * c_param * np.sqrt(2 * np.log(self.visits) / c.visits)) for c in self.child]
            return self.child[np.argmin(choice_weights)]

