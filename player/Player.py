import os
import pandas as pd
import random
import time

class Player:
    """
    Players must be defined in pairs
    
    MCTS player returns the node and the optimal move.
    
    All other player returns None (instead of a node) and the chosen move.
    """
    
    # Player 1 selects the optimal UCT move 
    # Player 2 selects the worst move from Player 1's position
    isFirstPlayer = True
    
    def __init__(self):
        self.isFirstPlayer = Player.isFirstPlayer
        self.name = "No Name"
        self.logfile = None
        self.fullName = "Definitely has no name"
        self.isAIPlayer = True
        self.family = None
        self.opponent = None
        
        # switch
        Player.isFirstPlayer = not Player.isFirstPlayer #lol wrong
        
    
    def chooseAction(self):
        """
        Move choice based on type of player
        """
        pass
    
    def __repr__(self):
        return self.name
    
    
    def CreateFile(self, cols, fileSuffix):
        """
        Creates a Unique File for EA (ES + GP) Stats 
        """
        # name of player
        name = self.name
        logfile = os.path.join('logs', self.logfile)
        
        # add '_' to suffix
        suffix = '_' + fileSuffix
        
        # check if file exists
        if not os.path.exists(logfile):
            os.makedirs(logfile)
            print(f'Log file created - {logfile}')
        
        # current list of files
        current_logs = os.listdir(logfile)
        
        # wait a few seconds between each file being made
        n1 = random.randint(0, 100)
        n2 = random.randint(20, 80)
        time.sleep(n1/n2)
        
        # get files of matching names
        matching = [file for file in current_logs if ((name in file) and (suffix in file))]
        
        # remove specific files from search
        for file in ['ExpectimaxStats.csv', 'FinalLeagueTable.csv', 'MCTSStats.csv', 'PlayerStats.csv']:
            if file in matching:
                matching.remove(file)
    
        # if no files exist so far
        if matching == []:
            df = pd.DataFrame(columns = cols)
            new_file = os.path.join(logfile, '0_' + name + suffix + '.csv')
            df.to_csv(new_file, index=False) 
            return new_file
        
        # get file number of latest file    
        highest_number = max([int(file.split('_')[0]) for file in matching])
        
        # new file number
        next_number = highest_number + 1
        new_file = os.path.join(logfile, str(next_number) + '_' + name + suffix + '.csv')
        
        # blank template file
        df = pd.read_csv(os.path.join(logfile, '0_' + name + suffix + '.csv'))
        
        # create new file
        df.to_csv(new_file, index=False) 
        return new_file

    
    def UpdateFile(self, data):
        """
        Update csv file with data
        """
        if self.logs:
            df = pd.read_csv(self.file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            #df.to_csv(self.file, index=False)  # export
            new_df.to_csv(self.file, index=False)  # export
        
    def UpdateESFile(self, data):
        """
        Update EvoAlg csv file with data
        """
        if self.logs:
            df = pd.read_csv(self.ES_file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            #df.to_csv(self.ES_file, index=False)  # export
            new_df.to_csv(self.ES_file, index=False)  # export
    
    
    def UpdateEVOFile(self, data):
        """
        Update EvoAlg csv file with data
        """
        if self.logs:
            df = pd.read_csv(self.EVO_file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            #df.to_csv(self.EVO_file, index=False)  # export
            new_df.to_csv(self.EVO_file, index=False)  # export
        
    def UpdateSEMFile(self, data):
        """
        Update EvoAlg csv file with data
        """
        if self.logs:
            df = pd.read_csv(self.SEM_file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            #df.to_csv(self.SEM_file, index=False)  # export
            new_df.to_csv(self.SEM_file, index=False)
        
    def UpdateTreeFile(self, data):
        if self.logs:
            df = pd.read_csv(self.Tree_file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            new_df.to_csv(self.Tree_file, index=False)
            
    def UpdateMetricsFile(self, data):
        if self.logs:
            df = pd.read_csv(self.metric_file)  # read in file
            #df = df.append(data, ignore_index = True)  # new data
            data =  {k:[v] for k,v in data.items()}
            new_df = pd.concat([df,pd.DataFrame(data)])  # new data
            new_df.to_csv(self.metric_file, index=False)

class HumanPlayer(Player):
    
    def __init__(self, name = 'Human'):
        super().__init__()
        self.name = name
        self.fullName = "Human Player"
        self.isAIPlayer = False
        self.family = "Human"
    
    def chooseAction(self, state, TileIndex):
        """
        state - The current state of the game board
        """
        positions = state.availableMoves(TileIndex)
        
        # user input
        while True:
            print(f'Available moves: \n {positions} \n')
            choice = int(input("Input your choice:"))
            if choice in positions:
                return choice
    
            
class RandomPlayer(Player):
    
    def __init__(self, name = 'Random'):
        super().__init__()
        self.name = name
        self.fullName = "Random Player"
        self.family = "Random"
        
    def ClonePlayer(self):
        return self
    
        
    def chooseAction(self, state):
        """
        Make a random move from all possible actions
        """
        if (state.Turn % 10 == 0):
            print(f'({self.name})   TimeTaken: 0 secs  -  Turn: {state.Turn}  -  Time:{time.strftime("%H:%M:%S", time.localtime())}')
        
        return state.getRandomMove().move
    
    

    
    
            
            
