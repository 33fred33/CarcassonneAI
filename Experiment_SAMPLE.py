from Experimental_Setup import RunLeague

from player.Player import RandomPlayer

from player.MCTS_Player import MCTSPlayer
from player.MCTS_RAVE_Player import MCTS_RAVEPlayer
from player.MCTS_ES_BACK_SEM_Player import MCTS_ES_BACK_SEM_Player

from datetime import date



############################################################################

# All controllers experiment (simulations=SAMPLE)

# random seed
RANDOM_SEED_SAMPLE = 100

# number of games
GAMES_SAMPLE = 1

# logs
LOGS_SAMPLE = True
LOGFILE_SAMPLE = 'Experiment_SAMPLE_1_' + str(date.today())

# iterations
ITERATIONS_SAMPLE = 10


PLAYER_LIST_SAMPLE = [
    MCTSPlayer(iterations=ITERATIONS_SAMPLE, logs=LOGS_SAMPLE, logfile=LOGFILE_SAMPLE, c_param = 2, name='MCTS_2'),
    #RandomPlayer()
    MCTS_ES_BACK_SEM_Player(iterations=ITERATIONS_SAMPLE, logs=LOGS_SAMPLE, logfile=LOGFILE_SAMPLE, c_param=1, Lambda=4, NGen=5, ES_Sims=5, ESType="comma"),
    
    ]


############################################################################


if __name__ == "__main__":
    # MCTS param experiment
    RunLeague(RANDOM_SEED_SAMPLE, PLAYER_LIST_SAMPLE, GAMES_SAMPLE, LOGS_SAMPLE, LOGFILE_SAMPLE)