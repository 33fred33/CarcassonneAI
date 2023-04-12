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
#from plotly.tools import make_subplots

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
from scipy import optimize
from itertools import repeat


#run experiments
logs_folder = "FO2"
for f in [5,6,7,8,9]:
   #for its in [5000]:
   for c in [0.5,1,math.sqrt(2),2,3]:
      generic_name = "MCTS_c"
      exps.fo_experiment(func_index=f,
                  random_seed=0,
                  experiment_type="1p",
                  player_dicts = [{"type":"VMCTS", 
                                   "c":c,
                                   "name":generic_name +str(c)
                                   }],
                  runs = 30,
                  splits = 2,
                  ranges = [[0,1],[0,1]],
                  minimum_step=0.00001,
                  #Logs data
                  log_path = [logs_folder,"Vanilla_MCTS_f"+str(f)+"_c"+str(c)],
                  logs_divisions=3,
                  tree_data=True,)

   for its in [2600,5000]:
      exps.fo_experiment(func_index=f,
                     random_seed=0,
                     experiment_type="1p",
                     player_dicts = [{"type":"SIEAMCTS", 
                                    "iterations":its,
                                    "name":"SIEA_MCTS" + str(its)
                                    }],
                     runs = 30,
                     splits = 2,
                     ranges = [[0,1],[0,1]],
                     minimum_step=0.00001,
                     #Logs data
                     log_path = [logs_folder,"SIEA_MCTS_f"+str(f)+"_its"+ str(its)],
                     logs_divisions=3,
                     tree_data=True,)
   
   for its in [2600,5000]:
      exps.fo_experiment(func_index=f,
                     random_seed=0,
                     experiment_type="1p",
                     player_dicts = [{"type":"EAMCTS", 
                                    "iterations":its,
                                    "name":"EA_MCTS" + str(its)
                                    }],
                     runs = 30,
                     splits = 2,
                     ranges = [[0,1],[0,1]],
                     minimum_step=0.00001,
                     #Logs data
                     log_path = [logs_folder,"EA_MCTS_f"+str(f)+"_its"+ str(its)],
                     logs_divisions=3,
                     tree_data=True,)
      
for f in [0,1,2,3,4]:
   #for its in [5000]:
   for c in [0.5,1,math.sqrt(2),2,3]:
      generic_name = "MCTS_c"
      exps.fo_experiment(func_index=f,
                  random_seed=0,
                  experiment_type="1p",
                  player_dicts = [{"type":"VMCTS", 
                                   "c":c,
                                   "name":generic_name +str(c)
                                   }],
                  runs = 30,
                  splits = 2,
                  ranges = [[0,1]],
                  minimum_step=0.00001,
                  #Logs data
                  log_path = [logs_folder,"Vanilla_MCTS_f"+str(f)+"_c"+str(c)],
                  logs_divisions=3,
                  tree_data=True,)
   
   for its in [2600,5000]:
      exps.fo_experiment(func_index=f,
                     random_seed=0,
                     experiment_type="1p",
                     player_dicts = [{"type":"SIEAMCTS", 
                                    "iterations":its,
                                    "name":"SIEA_MCTS" + str(its)
                                    }],
                     runs = 30,
                     splits = 2,
                     ranges = [[0,1]],
                     minimum_step=0.00001,
                     #Logs data
                     log_path = [logs_folder,"SIEA_MCTS_f"+str(f)+"_its"+ str(its)],
                     logs_divisions=3,
                     tree_data=True,)
   
   for its in [2600,5000]:
      exps.fo_experiment(func_index=f,
                     random_seed=0,
                     experiment_type="1p",
                     player_dicts = [{"type":"EAMCTS", 
                                    "iterations":its,
                                    "name":"EA_MCTS" + str(its)
                                    }],
                     runs = 30,
                     splits = 2,
                     ranges = [[0,1]],
                     minimum_step=0.00001,
                     #Logs data
                     log_path = [logs_folder,"EA_MCTS_f"+str(f)+"_its"+ str(its)],
                     logs_divisions=3,
                     tree_data=True,)
      
exp_path = os.path.join("logs",logs_folder)
exp_names = [ item for item in os.listdir(exp_path) if os.path.isdir(os.path.join(exp_path, item)) ]
exp_names_filtered = []
for name in exp_names:
    for distinctive in ["_f0_","_f1_","_f2_","_f3_","_f4_"]:
        if distinctive in name:
            exp_names_filtered.append(name)
            break
exps.Collect_FO_logs(exp_path, exp_names=exp_names_filtered, output_name = "1d_collective_logs.csv", output_tree_name = "1d_collective_tree_logs.csv")

exp_names_filtered = []
for name in exp_names:
    for distinctive in ["_f5_","_f6_","_f7_","_f8_","_f9_"]:
        if distinctive in name:
            exp_names_filtered.append(name)
            break
exps.Collect_FO_logs(exp_path, exp_names=exp_names_filtered, output_name = "2d_collective_logs.csv", output_tree_name = "2d_collective_tree_logs.csv")