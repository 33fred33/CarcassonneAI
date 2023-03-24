
from Carcassonne_Game.Carcassonne import CarcassonneState
from TicTacToe_Game.TicTacToe import TicTacToeState 
from Function_Optimisation_Game.Function_Optimisation import FunctionOptimisationState
from player.Player import RandomPlayer
from player.MCTS_Player import MCTSPlayer
from player.MCTS_RAVE_Player import MCTS_RAVEPlayer
from player.MCTS_ES_BACK_Player import MCTS_ES_BACK_Player
from player.MCTS_ES_BACK_SEM_Player import MCTS_ES_BACK_SEM_Player

import Experimental_Setup as exps
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import os
import pandas as pd
from datetime import date
from collections import OrderedDict
import time
import multiprocessing as mp
import numpy as np
import ast
import random
import math
import statistics as stats
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import bernoulli



############################################################################

#Experiment parameters
runs = 30
origlogfile=os.path.join("FO","Results")

#Problem parameters
branching_factor = 2
func_index = 6
ranges = [[0,1]]

#Player parameters
iterations = 5000
rollouts = 1
lamb = 4
ngen = 20
es_sims = 30
c_params = [math.sqrt(2)]#[0.5,1,math.sqrt(2),2,3]
seml = 0.1
semu = 0.5
estype = "comma"

#visualization parameters
divisions = 3
buckets = 1000
buckets_2d = 10
divisions_2d=100


if __name__ == "__main__":
        for c_param in c_params:

            #Experiment setup
            random_seed = int(c_param*10)+func_index
            random.seed(random_seed)
            np.random.seed(seed=random_seed)
            logfile=origlogfile+"_f"+str(func_index)+"_c"+str(c_param)

            

            #Players defnition
            mcts_player = MCTSPlayer(iterations=iterations
                                    ,c_param = c_param
                                    ,name='MCTS_c' + str(c_param)
                                    ,rollouts = 1
                                    ,logs=True
                                    ,logfile=logfile)
                                    #,random_seed = random_seed)
            s_b_mcts_player = MCTS_ES_BACK_SEM_Player(iterations=iterations-(lamb*ngen*es_sims)
                                    ,c_param=c_param
                                    ,rollouts = 1
                                    ,name='SE_MCTS' + str(iterations-(lamb*ngen*es_sims))
                                    ,Lambda=lamb
                                    ,NGen=ngen
                                    ,ES_Sims=es_sims
                                    ,ESType=estype
                                    ,logs=True
                                    ,logfile=logfile
                                    ,Sem_L=seml
                                    ,Sem_U=semu)
            random_player = RandomPlayer()
            players = [s_b_mcts_player]#[mcts_player]#, 

            #Execution
            state = FunctionOptimisationState(players=[mcts_player], function=func_index, ranges=ranges, splits=branching_factor)# give any single player
            used_func = state.function
            #state = FunctionOptimisationState(players=[random_player], function=func2, ranges=[[0,1],[0,1]], splits=3, minimum_step=0.0000001) #multiple dimensions

            all_data = []
            all_fo_logs = pd.DataFrame()
            for p_id, player in enumerate(players):
                fo_logs, data = exps.multiple_runs(state, used_func, player, runs, random_seed, divisions)
                all_fo_logs = pd.concat([all_fo_logs,fo_logs])
                all_data.append(data)
                all_data_df = pd.concat(all_data)
                all_data_df.to_csv(os.path.join('logs', logfile, "Tree_data.csv"), index=False)
            #m2 = s_b_mcts_player.chooseAction(state)
            #plot = exps.show_search(all_data, used_func, title, n_buckets = buckets, divisions=divisions)
            #plot.write_image(os.path.join('logs', logfile, "Averaged_plot" + '.png'), width=1920, height=1080)
            #show_2d_search([data], used_funlbc, title, divisions_2d, n_buckets = buckets_2d)
            #show_search([mcts_player,s_b_mcts_player], used_func, title, n_buckets = 50, divisions=4)
            #print("Best reward path:",str(stats.mean(ors2)),str(stats.stdev(ors2)))



            #Create final logs
            #Combine separate logs
            exps.CombineFiles(logs=True,logfile=logfile)

            #Parameters logs
            final_logs={}
            final_logs["runs"]=runs
            final_logs["random_seed"]=random_seed
            final_logs["logfile"]=logfile
            #Problem parameters
            final_logs["branching_factor"]=branching_factor
            final_logs["func_index"]=func_index
            final_logs["ranges"]=ranges
            #Player parameters
            final_logs["iterations"]=iterations
            final_logs["lamb"]=lamb
            final_logs["ngen"]=ngen
            final_logs["es_sims"]=es_sims
            final_logs["c_param"]=c_param
            final_logs["seml"]=seml
            final_logs["semu"]=semu
            final_logs["estype"]=estype

            final_df = pd.DataFrame(final_logs)
            final_df.to_csv(os.path.join('logs', logfile, "Parameter_logs" + '.csv'), index=False)

            #Results logs
            player_logs = defaultdict(lambda:[])
            for player in players:
                temp_logs = all_fo_logs[all_fo_logs["Player"]==player.name]
                player_logs["Player"].append(player.name)
                player_logs["Mean_Tree_Nodes"].append(temp_logs["Tree_Nodes"].mean())
                player_logs["Std_Tree_Nodes"].append(temp_logs["Tree_Nodes"].std())
                player_logs["Mean_Terminals_Reached"].append(temp_logs["Terminals_Reached"].mean())
                player_logs["Std_Terminals_Reached"].append(temp_logs["Terminals_Reached"].std())
                player_logs["Mean_Max_Visits_Path"].append(temp_logs["Max_Visits_Path"].mean())
                player_logs["Std_Max_Visits_Path"].append(temp_logs["Max_Visits_Path"].std())
                player_logs["Mean_Max_Reward_Path"].append(temp_logs["Max_Reward_Path"].mean())
                player_logs["Std_Max_Reward_Path"].append(temp_logs["Max_Reward_Path"].std())
                player_logs["Tree_Reaches_Terminal"].append(temp_logs["Max_Reward_Path"].values.sum()/len(temp_logs))

            player_df = pd.DataFrame(player_logs)
            player_df.to_csv(os.path.join('logs', logfile, "Final_Player_logs" + '.csv'), index=False)
            all_fo_logs.to_csv(os.path.join('logs', logfile, "Player_logs" + '.csv'), index=False)

