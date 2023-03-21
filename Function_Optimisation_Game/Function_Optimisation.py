import random
import itertools as it
from scipy.stats import bernoulli
import numpy as np
import itertools
import math
            
class FunctionOptimisationState:
   """
   List of important attributes:
      self.players: list of player objects (min len: 1, max len: 2)
      self.winner: Result at end of game. 1=P1 wins, 2=P2 wins, 0=Draw
      self.result: state's value
      self.playerSymbol: Indicates the current player
      self.isGameOver
   """
    
   def __init__(self, players, function, ranges, splits, minimum_step=0.00001, max_turns=np.inf, split_sequence=None):
      """
      players: list of player objects (min len: 1, max len: 2)
      function: fitness method (takes a list of len="dimensions" as argument). If is an int, default functions will be used
      ranges: list (dimensions; min len: 1, max len: any) of lists (min and max; len: 2) of domains.
      splits: (int) equal split amount
      """
      # assignation
      self.players = players
      self.function = function
      self.function_index = function
      if isinstance(self.function, int):
         def f0(x):
            """Unimodal, centered"""
            return math.sin(math.pi*x[0])
         def f1(x):
            """Multimodal, paper bubeck"""
            return 1/2*(math.sin(13*x[0])*math.sin(27*x[0])+1)
         def f2(x):
            """Smoothness with levels, paper finnsson"""
            if x[0] < 0.5:
               return 0.5+0.5*abs(math.sin(1/pow(x[0],5)))
            else:
               return 7/20+0.5*abs(math.sin(1/pow(x[0],5)))
         def f3(x):
            """Deceptive"""
            return (0.5*x[0])+(-0.7*x[0]+1)*pow(math.sin(5*math.pi*x[0]),4)
         def f4(x):
            """Deceptive, search traps"""
            return (0.5*x[0])+(-0.7*x[0]+1)*pow(math.sin(5*math.pi*x[0]),80)
         def f5(x):
            """Two variables: smooth"""
            return (x[0] + x[1])/2
         def f6(x):
            """Deceptive, search traps"""
            return ((0.5*x[0])+(-0.7*x[0]+1)*pow(math.sin(5*math.pi*x[0]),4))*((0.5*x[1])+(-0.7*x[1]+1)*pow(math.sin(5*math.pi*x[1]),4))
         def f7(x):
            """Deceptive, search traps"""
            return ((0.5*x[0])+(-0.7*x[0]+1)*pow(math.sin(5*math.pi*x[0]),80))*((0.5*x[1])+(-0.7*x[1]+1)*pow(math.sin(5*math.pi*x[1]),80))
         def f8(x):
            """Deceptive, search traps"""
            return 0.5+((math.sin(math.sqrt(x[0]**2+x[1]**2))**2-0.5)/((1+0.001*(x[0]**2+x[1]**2))**2))
         self.function_list=[f0,f1,f2,f3,f4,f5,f6,f7,f8]
         self.function = self.function_list[function]
         self.max_x = [0.5,0.867,None,0.1,0.1]
      self.ranges = ranges
      self.splits = splits
      self.minimum_step = minimum_step
      self.max_turns = max_turns
      self.name = "FunctionOptimisation"
      #calculated variables
      self.winner = None
      self.result = None
      self.playerSymbol = 1
      self.isGameOver = False
      self.Turn = 1
    
   def CloneState(self):
        """
        Clones the game state - quicker than using copy.deepcopy()
        """
        Clone = FunctionOptimisationState(self.players, self.function, self.ranges, self.splits, self.minimum_step, self.max_turns)
        Clone.winner = self.winner
        Clone.result = self.result
        Clone.playerSymbol = self.playerSymbol
        Clone.isGameOver = self.isGameOver   
        Clone.Turn = self.Turn
        return Clone

   def reset(self):
        """
        Create a fresh game board
        """
        return FunctionOptimisationState(self.players, self.function, self.ranges, self.splits, self.minimum_step)
   
   def eval_point(self):
      return [(r[0] + r[1])/2 for r in self.ranges]

   def move(self, Move = None):
      """
      Place a move on the game board
         Move: list (dimensions; min len: 1, max len: any) of lists (min and max; len: 2) of domains.
      """
      self.ranges = Move
      if self.ranges[0][1] - self.ranges[0][0] < self.minimum_step or self.Turn > self.max_turns:
         self.isGameOver = True
         p = self.function(self.eval_point())
         self.result = bernoulli.rvs(p)
         return
      
      #Turn end routine
      if len(self.players) == 2:
         self.playerSymbol = 3 - self.playerSymbol # switch turn
      self.Turn += 1  # increment turns

   def availableMoves(self):
      if self.ranges[0][1] - self.ranges[0][0] < self.minimum_step or self.Turn > self.max_turns:
         return []
      available_ranges = []
      for r in self.ranges:
         dimension_ranges = []
         for s in range(self.splits):
            start = r[0] + (r[1]-r[0])*s/self.splits
            finish = r[0] + (r[1]-r[0])*(s+1)/self.splits
            dimension_ranges.append([start, finish])
         available_ranges.append(dimension_ranges)
      available_combinations = itertools.product(*available_ranges)
      available_moves = [AvailableMove(move) for move in available_combinations]
      return available_moves
    
   def checkWinner(self):
      """
      Returns result
      """
      return self.result
    
   def getRandomMove(self):
        """
        Returns a random move from all possible moves
        """
        availableMoves = self.availableMoves()
        return random.choice(availableMoves)
    
   def shuffle(self): #DUMMY. Called by MCTS agents
      pass
    
   def featureVector(self):
      """Features: turn, player turn, ranges0, ranges1"""
      return [self.Turn, self.playerSymbol, self.ranges[0][0], self.ranges[0][1]]

   def __repr__(self):
      return str(self.ranges)

class AvailableMove:
   """
   A class used to represent available moves.
   Attributes
      ranges: list (dimensions; min len: 1, max len: any) of lists (min and max; len: 2) of domains.
      move : All information in one attribute
   """
   
   def __init__(self, ranges):
      self.move = ranges
      self.moveString = str(ranges)
      
   def __repr__(self):
      String = "Move:" + self.moveString
      return String
        
             
            