from player.Player import Player

import time
import random
import numpy as np
from collections import defaultdict

class MCTS_RAVEPlayer(Player):
    
    # Player 1 selects the optimal UCT move 
    # Player 2 selects the worst move from Player 1's position
    
    def __init__(self, iterations = 500, timeLimit = 10, isTimeLimited = False, c_param = 3, logs=False, logfile=None, name='M_RAVE'):
        super().__init__()
        self.iterations = iterations
        self.timeLimit = timeLimit
        self.isTimeLimited = isTimeLimited
        self.c_param = c_param
        self.Weight = 0
        self.name = name
        self.fullName = f'MCTS-RAVE (Time Limit = {self.timeLimit})' if self.isTimeLimited else  f'MCTS (Iterations = {self.iterations})'
        self.family = "MCTS_RAVE"
        self.logs = logs
        self.logfile = logfile
        if self.logs:
            self.cols = ['Name','Simulations','Turn','TimeTaken']
            self.file = self.CreateFile(self.cols, 'Stats')
    
    def ClonePlayer(self):
        Clone = MCTS_RAVEPlayer(iterations=self.iterations, timeLimit=self.timeLimit, isTimeLimited = self.isTimeLimited, 
                                c_param=self.c_param, logs=self.logs, logfile=self.logfile, name=self.name)
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
        # state the Root Node
        root_node = Node(state = root_state)
        
        if self.isTimeLimited:
            self.MCTS_TimeLimit(root_node, root_state)
        else:
            self.MCTS_IterationLimit(root_node, root_state)
    
        # return the node with the highest number of wins from the view of the current player
        bestMove = root_node.RAVESearch(self.c_param)
        
        return bestMove.Move.move
    
    
    
    def MCTS_IterationLimit(self, root_node, root_state):
        startTime = time.time()
        
        # copy 
        state = root_state.CloneState()
        actions = []
        
        # first simulation
        actions, numberOfRollouts = self.Rollout(root_node, state, actions)
        self.Backpropogate(root_node, state, actions, numberOfRollouts)
        
        for i in range(self.iterations-1):
            node = root_node
            state = root_state.CloneState()
            
            actions = []
    
            node, actions = self.Select(node, state, actions)  # Select
            node, actions = self.Expand(node, state, actions)  # Expand
            actions, numberOfRollouts = self.Rollout(node, state, actions)  # Rollout
            self.Backpropogate(node, state, actions, numberOfRollouts)  # Backpropogate
                
        endTime = time.time()
        if (root_state.Turn % 10 == 0):
            print(f'({self.name})   TimeTaken: {round(endTime - startTime,3)} secs  -  Turn: {root_state.Turn}  -  Time:{time.strftime("%H:%M:%S", time.localtime())}')
        
        # append info to csv
        if self.logs:
            data = {'Name': self.name,'Simulations':self.iterations,'Turn':int((root_state.Turn+1)/2), 'TimeTaken':endTime - startTime}
            self.UpdateFile(data)
            
            
    
    # 4 steps of MCTS
    def Select(self, node, state, actions):
        # Select
        while node.untried_moves == [] and node.child != []:  # node is fully expanded
            node = node.RAVESearch(self.c_param)
            actions.append((state.playerSymbol, node.Move.move))
            state.move(node.Move.move)
        return node, actions
    
    def Expand(self, node, state, actions):
        # Expand
        if node.untried_moves != [] and (not state.isGameOver):  # if we can expand, i.e. state/node is non-terminal
            move_random = random.choice(node.untried_moves)
            actions.append((state.playerSymbol, move_random.move))
            state.move(move_random.move)
            node = node.AddChild(move = move_random, state = state, isGameOver = state.isGameOver)
        return node, actions
    
    def Rollout(self, node, state, actions):
        # Rollout - play random moves until the game reaches a terminal state
        state.shuffle()  # shuffle deck
        numberOfRollouts = 0
        while not state.isGameOver:
            m = state.getRandomMove()
            actions.append((state.playerSymbol, m.move))
            state.move(m.move)
            numberOfRollouts += 1
        return actions, numberOfRollouts
              
    def Backpropogate(self, node, state, actions, numberOfRollouts):
        # Backpropogate
        result = state.checkWinner()
        i = numberOfRollouts
        while node != None:  # backpropogate from the expected node and work back until reaches root_node
            node.UpdateNode(result, actions[-i:])
            node = node.parent
            i+=1
    
    
    
    def MCTS_TimeLimit(self, root_node, root_state):
        startTime = endTime = time.time()
        
        # copy 
        state = root_state.CloneState()
        actions = []
        
        # first simulation
        actions, numberOfRollouts = self.Rollout(root_node, state, actions)
        self.Backpropogate(root_node, state, actions, numberOfRollouts)
        
        numberOfIterations = 1
        
        while ((endTime - startTime) < self.timeLimit):
            numberOfIterations += 1

            node = root_node
            state = root_state.CloneState()
            
            actions = []
    
            node, actions = self.Select(node, state, actions)  # Select
            node, actions = self.Expand(node, state, actions)  # Expand
            actions, numberOfRollouts = self.Rollout(node, state, actions)  # Rollout
            self.Backpropogate(node, state, actions, numberOfRollouts)  # Backpropogate
            
            # latest time
            endTime = time.time()
            
        
            
            
##############################################################################
##############################################################################
##############################################################################


class Node:
    """
    The Search Tree is built of Nodes
    A node in the search tree
    """
    
    def __init__(self, Move = None, parent = None, state = None, isGameOver = False):
        self.Move = Move  # the move that got us to this node - "None" for the root
        self.parent = parent  # parent node of this node - "None" for the root node
        self.child = []  # list of child nodes
        self.state = state
        self.untried_moves = state.availableMoves()
        self.playerSymbol = state.playerSymbol
        # keep track of visits/wins/losses
        self.visits = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.Q = 0.5
        # rave
        self.N_AMAF = defaultdict(int)
        self.Q_AMAF = {}
        
    
    def __repr__(self):
        if self.Move is None:
            move = 'None'
            Q_AMAF = 0
            N_AMAF = 0
        else :
            move = str(self.Move.move)
            Q_AMAF = (round(self.parent.Q_AMAF[(3-self.playerSymbol, self.Move.move)], 3))
            N_AMAF = self.parent.N_AMAF[(3-self.playerSymbol, self.Move.move)]
        String = "["
        String += f'Move:{move}, W:{round(self.wins,1)}, '
        String += f'L:{self.losses}, D:{self.draws}, '
        String += f'N: {self.visits}, '
        String += f'N_AMAF: {N_AMAF}, '
        String += f'Q:{round(self.Q,3)}, '
        String += f'Q_AMAF: {Q_AMAF}, '
        #String += f'Weight: {round(self.Weight, 3)}'
        String += f' Remaining Moves:{len(self.untried_moves)}'
        String += "]"
        
        return String
    
    def AddChild(self, move, state, isGameOver):
        """
        Add new child node for this move remove m from list of untried_moves.
        Return the added child node.
        """
        node = Node(Move = move, state = state, isGameOver = isGameOver, parent = self)
        self.untried_moves.remove(move)  # this move is now not available
        self.child.append(node)
        return node
    
    
    def UpdateNode(self, result, actions):
        """
        Update result and number of visits of node
        """
        self.visits += 1
        self.wins += (result > 0)
        self.losses += (result < 0)
        self.draws += (result == 0)
        self.Q = self.Q + (result - self.Q)/self.visits
        
        # update rave values
        for a in actions:
            self.N_AMAF[a] += 1
            if not a in self.Q_AMAF:
                self.Q_AMAF[a] = 0.5
                self.Q_AMAF[a] = self.Q_AMAF[a] + (result - self.Q_AMAF[a])/self.N_AMAF[a]
            else:
                self.Q_AMAF[a] = self.Q_AMAF[a] + (result - self.Q_AMAF[a])/self.N_AMAF[a]
        
    
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
    
    
    def RAVESearch(self, c_param, verbose=False):
        """
        Use the UCB1 formula to select the best child node from the children array.
        C_PARAM is an exploration-explotation factor
        """
        RAVE_constant = 10
            
        choice_weights = []
        for c in self.child:
            # mcts - rave
            factor = 1 if self.playerSymbol == 1 else -1
            N = c.visits
            N_AMAF = self.N_AMAF[(self.playerSymbol, c.Move.move)]
            Q_AMAF = self.Q_AMAF[(self.playerSymbol, c.Move.move)]
            beta = N_AMAF/(N + N_AMAF + 4*N*N_AMAF*(RAVE_constant**2))
            
            # RAVE UCT
            weight = (1-beta)*c.Q + beta*Q_AMAF + (factor * 2 * c_param * np.sqrt(2 * np.log(self.visits) / N))
            
            choice_weights.append(weight)
            if c_param > 0:
                c.Weight = weight
            
        if self.playerSymbol == 1:
            return self.child[np.argmax(choice_weights)]
        else: 
            return self.child[np.argmin(choice_weights)]