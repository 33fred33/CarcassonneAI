from player.Player import Player

import operator
from operator import attrgetter
import numpy as np
import time
import random
from statistics import mean
import math

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp



class MCTS_ES_BACK_SEM_Player(Player):
    
    # MCTS with ES and backpropogation and semantics
    
    def __init__(self, iterations = 500, timeLimit = 10, isTimeLimited = False, c_param = 3, logs=False, logfile=None, name='ES_B_S_MCTS', Lambda=4, NGen=20, ES_Sims=30, ESType = "plus",Sem_L=5, Sem_U=10):
        super().__init__()
        self.iterations = iterations
        self.timeLimit = timeLimit
        self.isTimeLimited = isTimeLimited
        self.c_param = c_param
        self.name = name
        self.Lambda = Lambda
        self.NGen = NGen
        self.ES_Sims = ES_Sims
        self.ESType = ESType
        self.Sem_L = Sem_L
        self.Sem_U = Sem_U
        self.latest_root_node = None #added
        self.nodes_dict = {} #added
        self.id_count = 0 #added
        #print("EAMCTS called, ESType:", str(self.ESType))
        
        self.fullName = f'MCTS (Time Limit = {self.timeLimit})' if self.isTimeLimited else  f'MCTS (Iterations = {self.iterations})'
        self.family = "ES_MCTS"
        self.logs = logs
        self.logfile = logfile
        self.hasGPTree = False
        self.GPTree = None
        if self.logs:
            self.cols = ['Name','Simulations','Turn','TimeTaken']
            self.file = self.CreateFile(self.cols, 'Stats')
            
            self.EVO_cols = ['Name','Turn','IsDifferent','Function','NumberNodes', 'Depth']
            self.EVO_file = self.CreateFile(self.EVO_cols, 'EvoUCT')
            
            self.ES_cols = ['Name','Turn','Generation','Lambda','TotalNodes','AverageNodes','AverageDepth','AverageSSD','IsFirstPlayer','Opponent']
            self.ES_file = self.CreateFile(self.ES_cols, 'EvoStr')
            
            self.SEM_cols = ['Name','Turn','Generation','Fitnesses','SSDs','BestIndex','WasRandom','IsFirstPlayer','Opponent']
            self.SEM_file = self.CreateFile(self.SEM_cols, 'SEM')
        
    def ClonePlayer(self):
        Clone = MCTS_ES_BACK_SEM_Player(iterations=self.iterations, timeLimit=self.timeLimit, isTimeLimited = self.isTimeLimited, 
                               c_param=self.c_param, logs=self.logs, logfile=self.logfile, name=self.name, Lambda=self.Lambda, NGen=self.NGen, ES_Sims=self.ES_Sims
                               , ESType = self.ESType, Sem_L=self.Sem_L, Sem_U = self.Sem_U)
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
        #startTime = time.time()
        
        if self.isTimeLimited:
            self.MCTS_TimeLimit(root_node, root_state)
        else:
            self.MCTS_IterationLimit(root_node, root_state)
                
        # return the node with the highest number of wins from the view of the current player
        if playerSymbol == 1:
            bestMove = sorted(root_node.child, key = lambda c: c.Q)[-1].Move
        else:
            bestMove = sorted(root_node.child, key = lambda c: c.Q)[0].Move
        self.latest_root_node=root_node #added
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
            node = self.Select(node, state, root_state) #why??
            node = self.Expand(node, state)
            self.Rollout(node, state)
            self.Backpropogate(node, state)
            
        # latest time
        endTime = time.time()
        
        if (root_state.Turn % 10 == 0):
            print(f'({self.name})   TimeTaken: {round(endTime - startTime,3)} secs  -  Turn: {root_state.Turn}  -  Time:{time.strftime("%H:%M:%S", time.localtime())}')
        
        # reset GP info
        self.GPTree = None
        self.hasGPTree = False
    
        # append info to csv
        if self.logs:
            data = {'Name': self.name,'Simulations':self.iterations,'Turn':int((root_state.Turn+1)/2), 'TimeTaken':endTime - startTime}
            self.UpdateFile(data)
    
    
    # 4 steps of MCTS
    def Select(self, node, state, root_state):
        # Select
        while node.untried_moves == [] and node.child != []:  # node is fully expanded
            if not self.hasGPTree:
                # GP search
                if root_state.Turn >= 1: ##errooooor
                    # get the GPTree of this turn
                    self.GPTree = ES_Search(node, self)
                    self.hasGPTree = True
            node = node.Search(self)
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
        state.shuffle()
        while not state.isGameOver:
            m = state.getRandomMove()
            state.move(m.move)
              
    def Backpropogate(self, node, state):
        # Backpropogate
        result = state.checkWinner()
        while node != None:  # backpropogate from the expected node and work back until reaches root_node
            node.UpdateNode(result, self.c_param)
            node = node.parent
            
##############################################################################
##############################################################################
##############################################################################


#C_PARAM = 2

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
        # UCT score
        self.UCT_high = 0
        self.UCT_low = 0
        # GP search decision
        self.GP_Tree = None
        
    
    def __repr__(self):
        visits = 1 if self.visits == 0 else self.visits
        move = str(None) if (self.Move is None) else str(self.Move.move)
        String = "["
        String += f'Move:{move}, Wins:{round(self.wins,1)},'
        String += f' Losses:{self.losses}, Draws:{self.draws}, Q:{round(self.Q,3)},'
        String += f' Wins/Visits:{round(self.wins,1)}/{self.visits} ({round(self.wins/visits,3)}),'
        String += f' UCT_high:{round(self.UCT_high, 3)}, UCT_low:{round(self.UCT_low, 3)},'
        String += f' Remaining Moves:{len(self.untried_moves)}'
        String += "]"
        
        return String
    
    def AddChild(self, move, state, isGameOver, child_id):#mod
        """
        Add new child node for this move remove m from list of untried_moves.
        Return the added child node.
        """
        node = Node(Move = move, state = state, isGameOver = isGameOver, parent = self, id = child_id) #mod
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
    
    
    def Search(self, MCTS_Player):
        """
        For the first half of the game use the UCB1 formula.
        Else, use GP to find an alternative to UCT 
        """
        # initialize
        hasGPTree = MCTS_Player.hasGPTree
        c_param = MCTS_Player.c_param
        
        # select the child chosen from the GP tree
        if hasGPTree:
            return ES_Search(self, MCTS_Player)
        # else, use normal UCT
        else:
            if self.playerSymbol == 1:
                #  look for maximum output
                choice_weights = [c.Q + (c_param * np.sqrt(np.log(self.visits) / c.visits)) for c in self.child]
                return self.child[np.argmax(choice_weights)]
            else: 
                #  look for minimum output
                choice_weights = [c.Q - (c_param * np.sqrt(np.log(self.visits) / c.visits)) for c in self.child]
                return self.child[np.argmin(choice_weights)]



        
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################


# random constant
def randomC():
    c = random.choice([0.25, 0.5, 1, 2, 3, 5, 7, 10])
    return c

def ES_Search(RootNode, MCTS_Player):
    """
    Find the best child from the given node
    """
    #print("In EA search")
    # initialize state variables
    state = RootNode.state  # current game state
    turn = state.Turn
    
    # initialize MCTS_Player variables
    Lambda = MCTS_Player.Lambda
    NGen = MCTS_Player.NGen
    ES_Sims = MCTS_Player.ES_Sims
    hasGPTree = MCTS_Player.hasGPTree
    GPTree = MCTS_Player.GPTree
    
    # set the number of inputs - [Q,n,N,c]
    pset = gp.PrimitiveSet("MAIN", 3)
    
    # Define new functions
    def div(left, right):
        if (abs(right) < 0.001):
            return 1
        else:
            return left/right
        
    # natural log
    def ln(left): 
        if left == 1: left = 1.001
        if left < 0.01: left = 0.01
        return np.log(abs(left))
    
    # square root
    def root(left):
        return (abs(left))**(1/2)

    # add operators
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(div, 2)
    pset.addPrimitive(ln, 1)
    pset.addPrimitive(root, 1)
    #pset.addPrimitive(operator.neg, 1)

    # rename the arguments
    pset.addTerminal(randomC(), name='c')
    pset.addTerminal(2)
    pset.renameArguments(ARG0='Q')
    pset.renameArguments(ARG1='n')
    pset.renameArguments(ARG2='N')
    pset.renameArguments(ARG3='c')
    
    # primitives and terminals list
    prims = pset.primitives[object]
    terminals = pset.terminals[object]
    
    # want to maximise the solution
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # define the structure of the programs 
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax) 
    
    #  register the generation functions into a Toolbox
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)


    def evalTree(individual, RootNode, state):
        # Transform the tree expression in a callable function
        func = toolbox.compile(expr=individual)
        isPlayer1 = (state.playerSymbol == 1)
        
        # from this point simulate the game 10 times appending the results
        results = []
        for i in range(ES_Sims):
            # copy the state
            stateCopy = state.CloneState()
            node = RootNode
            
            # child nodes
            childNodes = node.child
            nodeValues = [[c.Q, c.visits, node.visits] for c in childNodes] # values of the nodes
            
            # get the values of the tree for each child node
            v =  [func(Q,n,N) for Q,n,N in nodeValues]
            node = childNodes[np.argmax(v)] if isPlayer1 else childNodes[np.argmin(v)]
            
            # play the move of this child node
            stateCopy.move(node.Move.move)

            # shuffle deck
            stateCopy.shuffle()
            
            # random rollout
            while not stateCopy.isGameOver:
                m = stateCopy.getRandomMove()
                stateCopy.move(m.move)
                
            # result
            result = stateCopy.checkWinner()
            results.append(result)
            
            #Backpropogate
            while node != None:  # backpropogate from the expected node and work back until reaches root_node
                node.UpdateNode(result,0)
                node = node.parent
        
        # semantics check  
        individual.semantics = sorted(results)
        
        fitness = np.mean(results)
        # switch results for second player
        fitness = -fitness if (not isPlayer1) else fitness
        
        return fitness,
        

    
    # register gp functions
    toolbox.register("evaluate", evalTree, RootNode=RootNode, state=state)
    toolbox.register("select", selBestCustom)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=1, max_=3)
    toolbox.register("mutate", mutUniformCustom, expr=toolbox.expr_mut, pset=pset)
    
    # max depth of 8
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=8))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=8))
    
    # create tree for original UCT
    UCT_formula = [ prims[0], terminals[0], prims[2], prims[2], terminals[4], terminals[3], 
                   prims[5], prims[3], prims[2], terminals[4], prims[4], terminals[2], terminals[1]]
    UCT_GP_Tree = creator.Individual(UCT_formula)

    
    # if MCTS already has a gpTree, return the values for each child
    if hasGPTree:
        playerSymbol = state.playerSymbol
        nodeValues = [[c.Q, c.visits, RootNode.visits] for c in RootNode.child]
        func = toolbox.compile(expr=GPTree)
        values = [func(Q,n,N) for Q,n,N in nodeValues]
        if playerSymbol == 1:
            return RootNode.child[np.argmax(values)]
        else:
            return RootNode.child[np.argmin(values)]
    
    # else, find the optimal tree using GP 
    else:
        pop = [UCT_GP_Tree]  # one formula in tree
        hof = tools.HallOfFame(1)
            
        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", np.mean)
        mstats.register("std", np.std)
        mstats.register("min", np.min)
        mstats.register("max", np.max)
        
        pop, logbook = eaMuCommaLambdaCustom(MCTS_Player, turn, pop, toolbox, 
                                             mu=1, lambda_=Lambda, ngen=NGen, pset=pset, cxpb=0, mutpb=1, 
                                             stats=mstats, halloffame=hof, verbose=False)
        # return the best tree
        formula = str(hof[0])
        
        # append data to csv
        data = {'Name': MCTS_Player.name, 'Turn':int((turn+1)/2), 'IsDifferent':(UCT_GP_Tree != hof[0]), 
                'Function': formula, 'NumberNodes':len(hof[0]), 'Depth': (hof[0]).height }
        MCTS_Player.UpdateEVOFile(data) 
        
        #print(f'Chosen formula: {formula}')
        return hof[0]

    
#################################################################################  


def eaMuCommaLambdaCustom(MCTS_Player, turn, population, toolbox, 
                          mu, lambda_, ngen, pset, cxpb, mutpb,
                          stats=None, halloffame=None, verbose=__debug__):
    """
    This is the :math:`(\mu~,~\lambda)` evolutionary algorithm
    """
    assert lambda_ >= mu, "lambda must be greater or equal to mu."

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    record = stats.compile(population) if stats is not None else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Vary the population
        offspring = varOr(population, toolbox, lambda_, cxpb, mutpb, pset)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Select the next generation population
        population[:] = toolbox.select(population + offspring, MCTS_Player, gen, turn)
        
        # Update the statistics with the new population
        record = stats.compile(population) if stats is not None else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)
    return population, logbook


def semanticsDistance(original, new):
    return sum((np.absolute(np.subtract(original.semantics, new.semantics))/len(new.semantics)))


def selBestCustom(individuals, MCTS_Player, generation, turn,fit_attr="fitness"):
    # initialize values to add to table
    #print("in sel best custom, ESType:", str(MCTS_Player.ESType))
    Nodes = 0  # total number of nodes
    SSD = 0 # total semantic distance
    TotalDepth = 0  # add depth of each indivdual
    
    numInd = len(individuals)
    
    # keep track of fitness and semantic values
    fitnesses_list = []
    SSD_list = []
    
    # iterate through each individual program
    for i in individuals:
        Nodes += len(i)  # number of nodes in each individual
        # SSD between each new individual and sole parent
        distance = round(semanticsDistance(individuals[0], i), 3)
        i.SD = distance
        SSD += distance
        TotalDepth += i.height
        # append to lists
        fitnesses_list.append(i.fitness.values)
        SSD_list.append(distance)
        
    #print(f'Semantics List: {SSD_list}')
        
    # append data to csv
    data = {'Name': MCTS_Player.name, 'Turn':int((turn+1)/2), 'Generation':generation, 'Lambda':MCTS_Player.Lambda, 
            'TotalNodes': Nodes, 'AverageNodes':Nodes/numInd, 'AverageDepth': TotalDepth/(numInd), 'AverageSSD':SSD/(MCTS_Player.Lambda),
            'IsFirstPlayer':MCTS_Player.isFirstPlayer,'Opponent':MCTS_Player.opponent}
    MCTS_Player.UpdateESFile(data) 
        
    # check how many equal max fitness
    if MCTS_Player.ESType == "comma":
        #print("Reached, fred")
        numberMax = fitnesses_list[1:].count(max(fitnesses_list[1:]))
    else:
        numberMax = fitnesses_list.count(max(fitnesses_list))

    if numberMax > 1:
        return [individuals[SemanticsDecider(fitnesses_list, SSD_list, MCTS_Player, turn, generation)]]
    else:
        # sorted by fitness
        if MCTS_Player.ESType == "comma":
            individuals = individuals[1:]
        ind_sorted = sorted(individuals, key=attrgetter("fitness"), reverse=True)
        return ind_sorted[:1]
    

def SemanticsDecider(fitnesses_list, SSD_list, MCTS_Player, turn, generation):
    #print(f'(ES Semantics) Fitness: {fitnesses_list}, SSD: {SSD_list}')
    # lower and upper thresholdof SSD
    L = MCTS_Player.Sem_L
    U = MCTS_Player.Sem_U
    
    # index of max values
    if MCTS_Player.ESType == "comma":
        indices = [i for i, x in enumerate(fitnesses_list) if x == max(fitnesses_list[1:]) and i!=0]
    else:
        indices = [i for i, x in enumerate(fitnesses_list) if x == max(fitnesses_list)]
    
    isRandom = False
    lowest = U
    bestIndex = None
    
    for i in indices:
        if L < SSD_list[i] < lowest:
            lowest = SSD_list[i]  # new lowest value
            bestIndex = i  # new best index
    
    # if none match criteria
    if bestIndex is None:
        isRandom = True
        bestIndex = random.choice(indices)
    
    # update Semantics file
    data = {'Name': MCTS_Player.name, 'Turn':int((turn+1)/2), 'Generation':generation, 'Fitnesses':fitnesses_list, 
            'SSDs': SSD_list, 'BestIndex':bestIndex, 'WasRandom':isRandom, 'IsFirstPlayer':MCTS_Player.isFirstPlayer,
            'Opponent':MCTS_Player.opponent}
    MCTS_Player.UpdateSEMFile(data) 
    
    # return best index of best individual
    #print(f'(ES Semantics) Best Index: {bestIndex}')
    return bestIndex
        


def varOr(population, toolbox, lambda_, cxpb, mutpb, pset):
    """
    Part of an evolutionary algorithm applying only the variation part
    (crossover, mutation **or** reproduction). The modified individuals have
    their fitness invalidated. The individuals are cloned so returned
    population is independent of the input population.
    """
    assert (cxpb + mutpb) <= 1.0, (
        "The sum of the crossover and mutation probabilities must be smaller "
        "or equal to 1.0.")

    offspring = []
    for _ in range(lambda_):
        # randomly change c parameter
        pset.terminals[object][3] = gp.Terminal(randomC(), True, object)
        pset.renameArguments(ARG3='c')
        
        ind = toolbox.clone(random.choice(population))
        ind, = toolbox.mutate(ind)
        # make sure it's a new program less than or equal to depth 8
        while((ind == population[0]) or (ind.height > 8) ):
            ind, = toolbox.mutate(ind)
        del ind.fitness.values
        offspring.append(ind)
        
    return offspring


def mutUniformCustom(individual, expr, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.
    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :returns: A tuple of one tree.
    """
    
    # Mutation:
    #   90% internal nodes
    #   10% leaves
    
    isLeaf = (random.random() > 0.9)  # random
    
    if isLeaf:
        # get index of terminals
        isTerminals = [node in pset.terminals[object] for node in individual]
        indices = [i for i, x in enumerate(isTerminals) if x]
    else:
        # get index of primitives
        isPrims = [node in pset.primitives[object] for node in individual]
        indices = [i for i, x in enumerate(isPrims) if x]
    
    if indices == []:
        index = 0
    else:
        index = random.choice(indices)  # choose random index
        
    slice_ = individual.searchSubtree(index)  # cut individual at chosen index
    type_ = individual[index].ret
    individual[slice_] = expr(pset=pset, type_=type_)

    return individual,


##########################################################################################################






