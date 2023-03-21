from Carcassonne_Game.Carcassonne import CarcassonneState
from TicTacToe_Game.TicTacToe import TicTacToeState #mod

import os
import pandas as pd
from datetime import date
from collections import OrderedDict
import time
import multiprocessing as mp
import numpy as np
import ast
import random

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import math
import statistics as stats
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import bernoulli



###################################################

###################################################

def RunLeague_ES(randomSeed, players, gamesPerMatch, logs, logfile, game_name = "Carcassonne", ADD_NAME=None,match_list = None): #mod
    
    print(f'\n\n\nRandom Seed: {randomSeed}\n')

    # number of players
    n = len(players)
    
    # initial statement
    if logs:print(f'Welcome to the start of a new League \nDate: {date.today().strftime(("%d %B, %Y"))} \n')
    
    # print each competitor
    if logs:
        print('Here are the competitors: \n')
        i = 1
        for player in players:
            print(f'{i}. {player}')
            i += 1
        
    # create league table
    data = {
        "Pos": list(range(1,n+1)),
        "Player": [player for player in players], 
        "MatchesPlayed": n*[0], 
        "Points": n*0, 
        "BWP": n*0, 
        "BLP": n*0, 
        "W": n*0, 
        "L": n*0, 
        "D": n*0, 
        "PD": n*0
        }
    # create pandas league table
    df_league = pd.DataFrame(OrderedDict(data))
    
    # check if file exists
    path_file = os.path.join('logs', logfile)
    if not os.path.exists(path_file):
        os.makedirs(path_file)
    
    # create empty log files
    if logs:
        df_league.to_csv(os.path.join('logs', logfile, 'FinalLeagueTable.csv'), index=False)
    
    
    # get full fixture list
    fixtures = Fixtures(players)
    
    # initialize full list of games
    fixtureGames = []
    
    fixtureSetNumber = 1
    # each set of fixtures
    for fixtureSet in fixtures:
        j = 1
        for pairing in fixtureSet:
            
            fixtureMatchNumber = 1
            
            if 'Idle' in pairing: # skip match if there is an 'Idle' player
                continue
            
            # name
            p1name = pairing[0].name
            p2name = pairing[1].name
            
            add_match = False
            if p1name != p2name:
                if match_list is None and ADD_NAME is None:
                    add_match=True
                else:
                    if (ADD_NAME is not None and (ADD_NAME in p1name or ADD_NAME in p2name)):
                        add_match=True
                    if (match_list is not None and (p1name,p2name) in match_list):
                        add_match=True

            if add_match:        
                player1 = pairing[0].ClonePlayer()
                player2 = pairing[1].ClonePlayer()
                
                j += 1
                # add game to list
                fixtureGames.append((player1, player2, gamesPerMatch, fixtureSetNumber, fixtureMatchNumber, randomSeed, logs, logfile, game_name)) #mod
                randomSeed += 1 ##Potential error source
                fixtureMatchNumber += 1
        
        # increment by 1
        fixtureSetNumber += 1
        
    
    print(f'Number of Games: {len(fixtureGames) * gamesPerMatch}')

    # store number of games completed
    dataGames = {"Games_Completed": 0, "Total_Games": len(fixtureGames) * gamesPerMatch}
    df_Games = pd.DataFrame(OrderedDict(dataGames), index=[0])
    if logs: df_Games.to_csv(os.path.join('logs', logfile, 'GamesCompleted.csv'), index=False)
    
    # each fixture
    print('\nFixtures:')
    for f in fixtureGames: print(f)
    
    # multiprocessing, play multiple games
    print("AVAILABLE CPU's: ", str(mp.cpu_count()))
    pool = mp.Pool(mp.cpu_count())
    pool.map(PlayFullMatchMultiWrapper, fixtureGames)
        
    if logs:
        # group all files together
        CombineFiles(logs, logfile)
        CreateStatsFiles(logfile, game_name)

def RunLeague(randomSeed, players, gamesPerMatch, logs, logfile, game_name = "Carcassonne"): #mod
    
    print(f'\n\n\nRandom Seed: {randomSeed}\n')

    # number of players
    n = len(players)
    
    # initial statement
    if logs:print(f'Welcome to the start of a new League \nDate: {date.today().strftime(("%d %B, %Y"))} \n')
    
    # print each competitor
    if logs:
        print('Here are the competitors: \n')
        i = 1
        for player in players:
            print(f'{i}. {player}')
            i += 1
        
    # create league table
    data = {
        "Pos": list(range(1,n+1)),
        "Player": [player for player in players], 
        "MatchesPlayed": n*[0], 
        "Points": n*0, 
        "BWP": n*0, 
        "BLP": n*0, 
        "W": n*0, 
        "L": n*0, 
        "D": n*0, 
        "PD": n*0
        }
    # create pandas league table
    df_league = pd.DataFrame(OrderedDict(data))
    
    # check if file exists
    path_file = os.path.join('logs', logfile)
    if not os.path.exists(path_file):
        os.makedirs(path_file)
    
    # create empty log files
    if logs:
        df_league.to_csv(os.path.join('logs', logfile, 'FinalLeagueTable.csv'), index=False)
    
    
    # get full fixture list
    fixtures = Fixtures(players)
    
    # initialize full list of games
    fixtureGames = []
    
    fixtureSetNumber = 1
    # each set of fixtures
    for fixtureSet in fixtures:
        j = 1
        for pairing in fixtureSet:
            
            fixtureMatchNumber = 1
            
            if 'Idle' in pairing: # skip match if there is an 'Idle' player
                continue
            
            # name
            p1name = pairing[0].name
            p2name = pairing[1].name
            
            if p1name != p2name:
                player1 = pairing[0].ClonePlayer()
                player2 = pairing[1].ClonePlayer()
                
                j += 1
                # add game to list
                fixtureGames.append((player1, player2, gamesPerMatch, fixtureSetNumber, fixtureMatchNumber, randomSeed, logs, logfile, game_name)) #mod
                randomSeed += 1
                fixtureMatchNumber += 1
        
        # increment by 1
        fixtureSetNumber += 1
        
    
    print(f'Number of Games: {len(fixtureGames) * gamesPerMatch}')

    # store number of games completed
    dataGames = {"Games_Completed": 0, "Total_Games": len(fixtureGames) * gamesPerMatch}
    df_Games = pd.DataFrame(OrderedDict(dataGames), index=[0])
    if logs: df_Games.to_csv(os.path.join('logs', logfile, 'GamesCompleted.csv'), index=False)
    
    # each fixture
    print('\nFixtures:')
    for f in fixtureGames: print(f)
    
    # multiprocessing, play multiple games
    pool = mp.Pool(mp.cpu_count())
    pool.map(PlayFullMatchMultiWrapper, fixtureGames)
        
    if logs:
        # group all files together
        CombineFiles(logs, logfile)
        CreateStatsFiles(logfile, game_name)
    
def PlayFullMatchMultiWrapper(args):
    PlayFullMatch(*args)
  
def Fixtures(players):
    """
    Returns a round robin fixture with "home-and-away" results
    """
    # need an even amount of players
    if len(players) % 2:
        players.append("Idle")
    
    n = len(players)
    
    matchs = []  # individual matches (P1 vs P2)
    fixtures = []  # set of matches containing each player [(P1 vs. P2), (P3 vs. P4)]
    return_matches = []
    for fixture in range(1, n):
        for i in range(n//2):
            matchs.append((players[i], players[n - 1 - i]))
            return_matches.append((players[n - 1 - i], players[i]))
        players.insert(1, players.pop())
        fixtures.insert(len(fixtures)//2, matchs)
        fixtures.append(return_matches)
        matchs = []
        return_matches = []
    
    return fixtures
  
def PlayFullMatch(player1, player2, gamesPerMatch, fixtureSetNumber, fixtureMatchNumber, randomSeed, logs, logfile, game_name, showLogs=False): #mod
    """
    Play a full set of games between two players
    """
    if logs:
        print("\n##############################################################################################\n")
        print(f'Fixture Set: {fixtureSetNumber},   Fixture Match: {fixtureMatchNumber},   Players:  {player1}  vs. {player2}')
        print("\n##############################################################################################\n")

    winners = [0,0,0]  # [P1 wins, P2 wins, Draws]
    results = []  # points difference of each games
    timePerMatch = []
    
    # different seed for each match
    random.seed(randomSeed)
    
    # wait a few seconds between each file being made
    n1 = random.randint(0, 200)
    n2 = random.randint(40, 120)
    time.sleep(n1/n2)
    if logs:
        new_file, dfStats = CreateNewStatsFile(logfile)
    else:
        dfStats = None
    
    for game in range(gamesPerMatch):
        winner, result, timeTaken, dfStats = PlayOneGame(player1, player2, game+1, fixtureSetNumber, randomSeed, dfStats, logs, logfile, game_name) #mod
        # record the results
        winners[(winner-1)%3] += 1
        results.append(result)
        timePerMatch.append(timeTaken)
        
    # update league table
    # wait a few seconds between each file being made
    n1 = random.randint(0, 200)
    n2 = random.randint(40, 120)
    time.sleep(n1/n2)
    UpdateLeagueTable(player1, player2, gamesPerMatch, winners, results, logs, logfile)
    
    if logs:
    # export stats table
        dfStats.to_csv(new_file, index=False) 
    
    if showLogs:
        print(f'Games:{gamesPerMatch} - Player1 Wins:{winners[0]}    Player2 Wins:{winners[1]}    Draws:{winners[2]}')

def CombineFiles(logs, logfile):
    """
    Group the individual files and combine them into one file
    """
    # current list of files
    current_logs = os.listdir(os.path.join('logs', logfile))
    # split files into groups
    expecetimaxGroup = [file for file in current_logs if 'Star' in file]
    mctsGroup = [file for file in current_logs if (('MCTS' in file or 'M_RAVE' in file) and not(('Evo' in file) or ('SEM' in file)))]
    statsGroup = [file for file in current_logs if 'Match_Stats' in file]
    evoUCTGroup = [file for file in current_logs if 'EvoUCT' in file]
    evoStrGroup = [file for file in current_logs if 'EvoStr' in file]
    semGroup = [file for file in current_logs if 'SEM' in file]
    
    # names of grouped files
    groups = [expecetimaxGroup, mctsGroup, statsGroup, evoUCTGroup, evoStrGroup, semGroup]
    fileNames = ['ExpectimaxStats', 'MCTSStats', 'PlayerStats', 'EvolvedUCT', 'UCTStats', 'SemanticsStats']

    # for each file in group add to a joint csv file
    i = 0
    for group in groups:
        if group == []:
            i += 1
            continue
        first = True
        
        for j,file in enumerate(group):
            if first:
                df = pd.read_csv(os.path.join('logs', logfile, file))
                df["run"] = [j for _ in range(len(df))]
                first = False
            else:
                dfNew = pd.read_csv(os.path.join('logs', logfile, file))
                dfNew["run"] = [j for _ in range(len(dfNew))]
                #df = df.append(dfNew)
                df = pd.concat([df,dfNew])  # new data
        
        df.to_csv(os.path.join('logs', logfile, fileNames[i] + '.csv'), index=False)
        i += 1

def PlayOneGame(player1, player2, gameNumber, fixtureSetNumber, randomSeed, dfStats, logs, logfile, game_name, showLogs=False): #mod
    """
    Plays a single game between two players
    """
    times = [[],[]] # record each player's play time
    numberMeeples = [0,0] # record number of meeples each player places
    meepleTurn = [[],[]] # record when each player plays a meeple
    meepleFeature = [[],[]]  # record what feature they place meeple on
    
    # record time of game
    startTime = time.time()
    
    # begin the game state #mod
    if game_name == "Carcassonne":
        state = CarcassonneState(player1, player2)
    elif game_name == "TicTacToe":
        state = TicTacToeState(player1, player2)
    elif game_name == "Carcassonne_reduced":
        state = CarcassonneState(player1, player2, no_farms=True, no_monasteries=True)
    
    player1.opponent = player2.name
    player2.opponent = player1.name

    # record the turn number
    turns = [1,1]
    
    # game loop
    while (not state.isGameOver):
        
        if state.playerSymbol == 1:
            # calculate move time
            initialMoveTime = time.time()
            m = player1.chooseAction(state) # make move
            endMoveTime = time.time()
            times[0].append(endMoveTime - initialMoveTime)
            # record meeple info
            if game_name == "Carcassonne": #mod
                if (m != 0) and (m[4] is not None):
                    numberMeeples[0] += 1  # meeple has been played
                    meepleTurn[0].append(turns[0])  # record turn
                    meepleFeature[0].append(m[4][0])  # record feature type
            turns[0] += 1
            
        else:
            # calculate move time
            initialMoveTime = time.time()
            m = player2.chooseAction(state) # make move
            endMoveTime = time.time()
            times[1].append(endMoveTime - initialMoveTime)
            # record meeple info
            if game_name == "Carcassonne": #mod
                if (m != 0) and (m[4] is not None):
                    numberMeeples[1] += 1  # meeple has been played
                    meepleTurn[1].append(turns[1])  # record turn
                    meepleFeature[1].append(m[4][0])  # record feature type
            turns[1] += 1
        
        # make the move on the board
        state.move(m)
    
    # final scores
    finalScore = state.Scores
    # winner (1 = P1 wins, 2 = P2 wins, 0 = Draw)
    winner = state.winner
    # result = P1 score - P2 Score
    result = state.result
    
    # game time 
    endTime = time.time()
    timeTaken = endTime-startTime
    
    if logs:
        print(f'\nGame Over: \nFixture Set: {fixtureSetNumber},  Game: {gameNumber}, Players:  {player1}  vs. {player2}')
    
    gameResult = 'Draw' if winner == 0 else f'Player{winner} Wins'
    
    # update players stats table
    if logs:
        dfStats = UpdateStatsTable(player1, player2, gameNumber, fixtureSetNumber, randomSeed, dfStats, finalScore, winner, 
                                   state.FeatureScores, times, numberMeeples, meepleTurn, meepleFeature, turns)
        updateGamesCompletedFile(logfile)    
    
    if showLogs:
        print(f'    Game {gameNumber}, Player1: {finalScore[0]} - Player2: {finalScore[1]}      {gameResult}     (Time: {int(timeTaken//60)} Mins {int(timeTaken%60)} Secs)')
    # return results of game
    return winner, result, timeTaken, dfStats

def UpdateStatsTable(player1, player2, gameNumber, fixtureSetNumber, randomSeed, dfStats, finalScore, winner, 
                     FeatureScores, times, numberMeeples, meepleTurn, meepleFeature, turns):
    """
    Update a players stats after each game
    """
    # new data to be added
    data = {"FixtureSet": fixtureSetNumber, "Game": gameNumber, "RandomSeed": randomSeed, "Player": player1, "Opponent": player2, "Result": winner,
            "Win":int(winner==1), "Loss":int(winner==2), "Draw":int(winner==0), 
            "PlayerScore": finalScore[0], "OpponentScore": finalScore[1], "CompleteCityScore": FeatureScores[0][0], 
            "CompleteRoadScore": FeatureScores[0][1], "CompleteMonasteryScore": FeatureScores[0][2], 
            "IncompleteCityScore": FeatureScores[0][3], "IncompleteRoadScore": FeatureScores[0][4], 
            "IncompleteMonasteryScore": FeatureScores[0][5], "FarmScore": FeatureScores[0][6],
            "MeeplesPlayed": numberMeeples[0], "MeepleTurns": [meepleTurn[0]], "MeepleFeatures": [meepleFeature[0]], 
            "Turns": turns[0], "AvgTurnTime": (sum(times[0]))/turns[0]}
    p1_data = pd.DataFrame(data)
    dfStats = dfStats.append(p1_data)  # add new data to table
    
    # new data to be added
    data = {"FixtureSet": fixtureSetNumber, "Game": gameNumber, "RandomSeed": randomSeed, "Player": player2, "Opponent": player1, "Result": (3-winner)%3,
            "Win":int(winner==2), "Loss":int(winner==1), "Draw":int(winner==0), 
            "PlayerScore": finalScore[1], "OpponentScore": finalScore[0], "CompleteCityScore": FeatureScores[1][0], 
            "CompleteRoadScore": FeatureScores[1][1], "CompleteMonasteryScore": FeatureScores[1][2], 
            "IncompleteCityScore": FeatureScores[1][3], "IncompleteRoadScore": FeatureScores[1][4], 
            "IncompleteMonasteryScore": FeatureScores[1][5], "FarmScore": FeatureScores[1][6],
            "MeeplesPlayed": numberMeeples[1], "MeepleTurns": [meepleTurn[1]], "MeepleFeatures": [meepleFeature[1]], 
            "Turns": turns[1], "AvgTurnTime": (sum(times[1]))/turns[1]}
    p2_data = pd.DataFrame(data)
    dfStats = dfStats.append(p2_data)  # add new data to table
    
    return dfStats

def CreateNewStatsFile(logfile):
    """
    A new stats file per match
    """
    # create a table of stats for all players
    columnNames = ["FixtureSet", "Game", "RandomSeed", "Player", "Opponent", "Result", "Win", "Loss", "Draw", 
                   "PlayerScore", "OpponentScore", "CompleteCityScore", "CompleteRoadScore", 
                   "CompleteMonasteryScore", "IncompleteCityScore", "IncompleteRoadScore", 
                   "IncompleteMonasteryScore", "FarmScore","MeeplesPlayed", "MeepleTurns", 
                   "MeepleFeatures", "Turns", "AvgTurnTime"]
    dfStats = pd.DataFrame(columns = columnNames)
    
    # current list of files
    current_logs = os.listdir(os.path.join('logs', logfile))
    
    # get files of matching names
    matching = [file for file in current_logs if 'Match_Stats' in file]
    #print(f'Matching: {matching}')
    
    # if no files exist so far
    if matching == []:
        new_file = os.path.join('logs', logfile, '0_Match_Stats.csv')
        #print(new_file)
        dfStats.to_csv(new_file, index=False) 
        return new_file, dfStats
    
    # get file number of latest file    
    #highest_number = max([int(file.split('_')[0]) for file in matching])
    
    # new file number
    #next_number = highest_number + 1
    new_file = os.path.join('logs', logfile, str(random.randint(1,9999999)) + '_Match_Stats.csv')
    
    # create new file
    dfStats.to_csv(new_file, index=False) 
    return new_file, dfStats

def UpdateLeagueTable(player1, player2, gamesPerMatch, winners, results, logs, logfile):
    """
    Update table with the results after a full match
    """

    p1Wins, p2Wins = winners[0], winners[1]
    isP1Winner = isP1Loser = isP2Winner = isP2Loser = isDraw = False  
    isP1BW = isP2BW = isP1BL = isP2BL = False
    p1Score = p2Score = 0  # initialize scores
    
    if p1Wins > p2Wins:  # player 1 wins
        p1Score += 4
        isP1Winner = True
        isP2Loser = True
        if (p1Wins/(p1Wins+p2Wins) >= 0.75):  # dominant winner
            p1Score += 1
            isP1BW = True
        elif (p1Wins/(p1Wins+p2Wins) <= 0.55): # bonus losing point for other player
            p2Score += 1
            isP2BL = True
            
    elif p2Wins > p1Wins:  # player 2 wins
        p2Score += 4
        isP2Winner = True
        isP1Loser = True
        if (p2Wins/(p1Wins+p2Wins) >= 0.75):  # dominant winner
            p2Score += 1
            isP2BW = True
        elif (p2Wins/(p1Wins+p2Wins) <= 0.55): # bonus losing point for other player
            p1Score += 1
            isP1BL = True
            
    else: # draw
        p1Score += 2
        p2Score += 2
        isDraw = True
    
    avgScoreDifference = round(sum(results)/len(results), 3)
    
    # update table with these values
    p1Update = [player1.name, 1, p1Score, int(isP1BW), int(isP1BL), int(isP1Winner), int(isP1Loser), int(isDraw), round(avgScoreDifference,2)]
    p2Update = [player2.name, 1, p2Score, int(isP2BW), int(isP2BL), int(isP2Winner), int(isP2Loser), int(isDraw), -round(avgScoreDifference,2)]
    

    if logs:
        print(f'Points Earned - Player 1: {p1Score}    Player 2: {p2Score}')
        # read in latest league table csv
        df_league = pd.read_csv(os.path.join('logs', logfile, 'FinalLeagueTable.csv'))
        
        # update values for each player 
        for update in (p1Update, p2Update):
            updateValue = 1
            for column in df_league.columns:
                player = update[0]
                if column != "Pos" and column != "Player":
                    df_league.loc[df_league['Player'] == player, column] += update[updateValue]
                    updateValue += 1
                    
        # sort league table by points, then PD, then wins
        df_league = df_league.sort_values(by=['Points', 'PD', 'W'], ascending=False)
        df_league['Pos'] = df_league['Pos'].sort_values().values
        # export the updated table
        df_league.to_csv(os.path.join('logs', logfile, 'FinalLeagueTable.csv'), index=False)

def updateGamesCompletedFile(logfile):
    done = False
    # wait
    while not done:
        n1 = random.randint(0, 200)
        n2 = random.randint(40, 120)
        time.sleep(n1/n2)
        # update csv
        try:
            df_Games = pd.read_csv(os.path.join('logs', logfile, 'GamesCompleted.csv'))
            done = True
        except:
            print("In except for game count")

    df_Games['Games_Completed'] += 1
    df_Games.to_csv(os.path.join('logs', logfile, 'GamesCompleted.csv'), index=False)
    # print number of games
    completed = df_Games['Games_Completed'].tolist()[0]    
    total = df_Games['Total_Games'].tolist()[0]
    print(f'\n  #####   #####   Games Completed: {completed}/{total}  ({round(100 * completed /total, 2)} %)  #####   #####   \n')

def CreateStatsFiles(logfile, game_name = "Carcassonne"): #mod
    """
    Create Stats files to be used in the Stats UI (plotly-dash)
    """
    print('\nCreating Final Stats Files....')
    
    # read in the necessary files
    dfLeague = pd.read_csv(os.path.join('logs', logfile, 'FinalLeagueTable.csv'))
    dfStats = pd.read_csv(os.path.join('logs', logfile, 'PlayerStats.csv'), converters={'MeepleFeatures': eval, 'MeepleTurns': eval})
 
        
    # clean up some of the tables
    # round off league table columns
    dfLeague = dfLeague.round(2)

    # number of games each team played
    MATCHES = dfLeague['MatchesPlayed'].values[0]
    GAMES = (dfStats['Game'].max())
    TOTAL_GAMES = MATCHES*GAMES
    
    
    
    #--------------------------------------------------------------------------
    
    
    
    #  ---  1. Results Matrix  ---
    dfMatches = dfStats[['FixtureSet', 'Game', 'Player', 'Opponent', 'Result', 'Win', 'Loss']].iloc[::2, :]  # only need these columns
    df1 = dfMatches.groupby(['FixtureSet', 'Player', 'Opponent'])[['Win', 'Loss']].sum().reset_index()  # results per match
    df1["Scores"] = df1['Win'].map(str) + "-" + df1['Loss'].map(str)
    dfT = df1.reset_index()
    dfT['Player2'] = dfT['Opponent']
    dfT['Players'] = dfT['Player']
    dfResults = dfT.pivot(index='Players', columns='Player2', values='Scores').fillna("- ")
    dfResults = dfResults.reset_index()
    dfResults = dfResults.rename(columns={'Players': 'P1 \ P2'})
    dfResults.to_csv(os.path.join('logs', logfile, 'ResultsMatrix.csv'), index=False)
    
    
    #--------------------------------------------------------------------------
    

    #  ---  2. Feature Scores  ---
    dfMeepleScores = dfStats[['Player','CompleteCityScore','CompleteRoadScore', 'CompleteMonasteryScore', 'IncompleteCityScore', 'IncompleteRoadScore', 'IncompleteMonasteryScore', 'FarmScore']]
    Total = dfMeepleScores[list(dfMeepleScores.columns)[1:]].sum(axis=1)
    dfMeepleScores.loc[:,'Total'] = Total
    dfAvgMeepleScores = dfMeepleScores.groupby('Player',as_index=False).mean()
    dfAvgMeepleScores = dfAvgMeepleScores.melt('Player', var_name='Feature', value_name='Scores').sort_values(['Player','Feature']).reset_index(drop=True)
    # feature types
    conditions = PandasConditions(dfAvgMeepleScores)
    # create a list of the values we want to assign for each condition
    values = ['City','Road','Monastery','Farm', 'Total']
    dfAvgMeepleScores['FeatureType'] = np.select(conditions, values)
    dfAvgMeepleScores['FeatureType'] = dfAvgMeepleScores['FeatureType']
    # full breakdown 
    dfAvgMeepleScoresFull = dfAvgMeepleScores[['Player','Feature','Scores']]
    # specific feature types
    conditions = PandasConditions(dfAvgMeepleScoresFull, full=True)
    values = ['City (C)', 'City (INC)', 'Road (C)', 'Road (INC)', 'Monastery (C)', 'Monastery (INC)', 'Farm', 'Total']
    dfAvgMeepleScoresFull['FeatureType'] = np.select(conditions, values)
    dfAvgMeepleScoresFull = dfAvgMeepleScoresFull.round(1)
    dfAvgMeepleScoresFull.to_csv(os.path.join('logs', logfile, 'dfAvgMeepleScoresFull.csv'), index=False)
    
    
    
    #  ---  2A. Feature Scores by Feature  ---
    # Meeple Scores by feature
    dfAvgMeepleScoresByFeature = dfAvgMeepleScores.groupby(['Player','FeatureType']).sum().reset_index(drop=False)
    dfAvgMeepleScoresByFeature = dfAvgMeepleScoresByFeature.round(1)
    dfAvgMeepleScoresByFeature.to_csv(os.path.join('logs', logfile, 'dfAvgMeepleScoresByFeature.csv'), index=False)
    
    
    
    #  ---  2B. Feature Scores (Percent)  ---
    # percentages
    dfMeepleScoresPercent = dfMeepleScores.copy(deep=True)
    cols = ['CompleteCityScore','CompleteRoadScore', 'CompleteMonasteryScore', 'IncompleteCityScore', 'IncompleteRoadScore', 'IncompleteMonasteryScore','FarmScore']
    dfMeepleScoresPercent.loc[:,cols] = dfMeepleScoresPercent.loc[:,cols].divide(dfMeepleScoresPercent.loc[:,"Total"]/100, axis="index")
    dfMeepleScoresPercent = dfMeepleScoresPercent.groupby('Player',as_index=False).mean()
    dfMeepleScoresPercent = dfMeepleScoresPercent.melt('Player', var_name='Feature', value_name='Scores').sort_values(['Player','Feature']).reset_index(drop=True)
    # feature types
    conditions = PandasConditions(dfMeepleScoresPercent)
    # create a list of the values we want to assign for each condition
    values = ['City','Road','Monastery','Farm', 'Total']
    dfMeepleScoresPercent['FeatureType'] = np.select(conditions, values)
    
    # full breakdown 
    dfMeepleScoresPercentFull = dfMeepleScoresPercent[['Player','Feature','Scores']]
    # specific feature types
    conditions = PandasConditions(dfMeepleScoresPercentFull, full=True)
    values = ['City (C)', 'City (INC)', 'Road (C)', 'Road (INC)', 'Monastery (C)', 'Monastery (INC)', 'Farm', 'Total']
    dfMeepleScoresPercentFull['FeatureType'] = np.select(conditions, values)
    dfMeepleScoresPercentFull = dfMeepleScoresPercentFull.round(1)
    dfMeepleScoresPercentFull.to_csv(os.path.join('logs', logfile, 'dfMeepleScoresPercentFull.csv'), index=False)
    
    
    
    #  ---  2C. Feature Scores by Feature (Percent)  ---
    # Meeple Scores by feature
    dfMeepleScoresPercentByFeature = dfMeepleScoresPercent.groupby(['Player','FeatureType']).sum().reset_index(drop=False)
    dfMeepleScoresPercentByFeature = dfMeepleScoresPercentByFeature.round(1)
    dfMeepleScoresPercentByFeature.to_csv(os.path.join('logs', logfile, 'dfMeepleScoresPercentByFeature.csv'), index=False)
    
    
    #--------------------------------------------------------------------------
    
    
    #  ---  3. Meeple Placement   ---
    # Meeple Placement
    colsMeeple = ['Player', 'Feature', 'Turns']
    colsGames = ['Player', 'NumberGames']
    df1 = pd.DataFrame(columns=colsMeeple)
    df_Games = pd.DataFrame(columns=colsGames)
    
    dfMeepleFeatures = dfStats[['Player','MeeplesPlayed','MeepleTurns','MeepleFeatures']]
    for player in (dfMeepleFeatures['Player'].unique()):
        df = dfMeepleFeatures[dfMeepleFeatures['Player'] == player]
        
        locations = df['MeepleFeatures'].values.tolist()
        locationsAll = [item for sublist in locations for item in sublist]
        turns = df['MeepleTurns'].values.tolist()
        turnsAll = [item for sublist in turns for item in sublist]
        df_temp = pd.DataFrame({'Player': len(locationsAll)*[player],
                                'Feature': locationsAll,
                                'Turns': turnsAll})
        df1 = df1.append(df_temp)
        
        # nu
        # number of matches for each player
        NumberGames = dfLeague.loc[dfLeague['Player'] == player]['MatchesPlayed'] * GAMES
        df_temp1 = pd.DataFrame({'Player': player,
                                 'NumberGames': NumberGames.values[0]}, index=[0])
        df_Games = df_Games.append(df_temp1)
    
    dfTotalPlacements = (pd.crosstab(df1['Player'], df1['Feature']))
    dfAvgPlacements = pd.merge(dfTotalPlacements, df_Games, on='Player', how='left')
    
    # normalize results per games
    if game_name=="Carcassonne": #mod
        featureCols = ['C','G','Monastery','R']
        dfAvgPlacements.loc[:, featureCols] = dfAvgPlacements.loc[:, featureCols].div(dfAvgPlacements.NumberGames, axis=0)
        del dfAvgPlacements['NumberGames']
        # total
        Total = dfAvgPlacements[list(dfAvgPlacements.columns)[1:]].sum(axis=1)
        dfAvgPlacements.loc[:,'Total'] = Total
        dfAvgPlacementsFinal = dfAvgPlacements.melt('Player', var_name='Feature', value_name='Number').sort_values(['Player','Feature']).reset_index(drop=True)
        dfAvgPlacementsFinal = dfAvgPlacementsFinal.round(1)
        # fix feature names
        conditions = PandasConditionsMeeple(dfAvgPlacementsFinal)
        # create a list of the values we want to assign for each condition
        values = ['City','Road','Farm','Monastery','Total']
        dfAvgPlacementsFinal['Feature'] = np.select(conditions, values)
        dfAvgPlacementsFinal['Number'] = dfAvgPlacementsFinal['Number'].astype(float).round(2)
        dfAvgPlacementsFinal.to_csv(os.path.join('logs', logfile, 'dfAvgPlacementsFinal.csv'), index=False)
        
        
        #  ---  3A. Meeple Placement (Percent)  ---
        dfAvgPlacementsPercent = dfAvgPlacements.copy(deep=True)
        cols = ['C','G', 'Monastery', 'R']
        cols=list(set(dfAvgPlacementsPercent.columns).intersection(cols))
        dfAvgPlacementsPercent.loc[:,cols] = dfAvgPlacementsPercent.loc[:,cols].divide(dfAvgPlacementsPercent.loc[:,"Total"]/100, axis="index")
        dfAvgPlacementsPercent = dfAvgPlacementsPercent.melt('Player', var_name='Feature', value_name='Number').sort_values(['Player','Feature']).reset_index(drop=True)
        dfAvgPlacementsPercent = dfAvgPlacementsPercent.round(1)
        # fix feature names
        conditions = PandasConditionsMeeple(dfAvgPlacementsPercent)
        # create a list of the values we want to assign for each condition
        values = ['City','Road','Farm','Monastery','Total']
        dfAvgPlacementsPercent['Feature'] = np.select(conditions, values)
        dfAvgPlacementsPercent['Number'] = dfAvgPlacementsPercent['Number'].astype(float).round(2)
        dfAvgPlacementsPercent.to_csv(os.path.join('logs', logfile, 'dfAvgPlacementsPercent.csv'), index=False)
        
    
    #  ---  4. ES  ---
    
    if 'SemanticsStats.csv' in os.listdir(os.path.join('logs',logfile)):
        
        #  ---  4A. Average Semantics (per Generation, per Turn) ---
        dfSemanticsStats = pd.read_csv(os.path.join('logs', logfile, 'SemanticsStats.csv'))
        df1 = dfSemanticsStats
        
        colsAvgSSD = ['Name', 'Turn', 'AvgSSD']
        dfAvgSSD =  pd.DataFrame(columns = colsAvgSSD)
        
        for index, row in dfSemanticsStats.iterrows():
            data = {'Name': row['Name'], 'Turn': row['Turn'], 'AvgSSD': (sum(ast.literal_eval(row['SSDs'])))/4 } #not good
            dfAvgSSD = dfAvgSSD.append(data, ignore_index = True)
        
        dfAvgSSD.to_csv(os.path.join('logs', logfile, 'dfAvgSSD.csv'), index=False)
        
        
        #  ---  4A. Average Semantics (per Turn) ---
        colsSSD = ['Name', 'Turn', 'SSD']
        dfSSD =  pd.DataFrame(columns = colsSSD)
        
        for index, row in dfSemanticsStats.iterrows():
            SSDs = (ast.literal_eval(row['SSDs']))[1:]  # don't want first SSD
            for value in SSDs:
                data = {'Name': row['Name'], 'Turn': row['Turn'], 'SSD': value}
                dfSSD = dfSSD.append(data, ignore_index = True)
            
        dfSSD.to_csv(os.path.join('logs', logfile, 'dfSSD.csv'), index=False) 
    
    
    
    print('Finished Creating Final Stats Files')
    
def PandasConditions(df, full=False):
    if full:
        return [(df['Feature'].str.contains("CompleteCityScore")),
                (df['Feature'].str.contains("IncompleteCityScore")),
                (df['Feature'].str.contains("CompleteRoadScore")),
                (df['Feature'].str.contains("IncompleteRoadScore")),
                (df['Feature'].str.contains("CompleteMonasteryScore")),
                (df['Feature'].str.contains("IncompleteMonasteryScore")),
                (df['Feature'].str.contains("Farm")),
                (df['Feature'].str.contains("Total"))]
    else:
        return [(df['Feature'].str.contains("City")),
                (df['Feature'].str.contains("Road")),
                (df['Feature'].str.contains("Monastery")),
                (df['Feature'].str.contains("Farm")),
                (df['Feature'].str.contains("Total"))]

def PandasConditionsMeeple(df):
    return [(df['Feature'] == 'C'),
            (df['Feature'] == 'G'),
            (df['Feature'] == 'R'),
            (df['Feature'] == 'Monastery'),
            (df['Feature'] == 'Total'),
            ]

def tree_data(player, divisions=3, dimension=0, early_cut=False):
   """Division method Options: percentage, best_changed
      early_cut: only nodes that were added before a terminal state was reached by an expanded node"""
   
   if early_cut:
      nodes = []
      for key,node in player.nodes_dict.items():
         if node.state.isGameOver:
            break
         nodes.append(node)
   else:
      nodes = [node for key,node in player.nodes_dict.items()]
   n_nodes = len(player.nodes_dict)

   id_list = []
   x_list = []
   id_block_list = []
   features_list = []

   for node in nodes:
      id_list.append(node.id)
      x_list.append(node.state.eval_point()[dimension])
      id_block_list.append(int((node.id/(n_nodes+1))/(1/divisions)))
      features_list.append(node.state.featureVector())
   data_dict = {"player":player.name,"id":id_list, "x":x_list, "id_block":id_block_list}

   for feature_index in range(len(features_list[0])): #Assumes the feature vector size is constant
      data_dict["feature_"+str(feature_index)] = [fv[feature_index] for fv in features_list]

   data = pd.DataFrame(data_dict)
   return data

def best_tree_path(node, recommendation_policy="reward"):
   if recommendation_policy == "reward":
      while node.child != []:
         if node.playerSymbol == 1:
            node = sorted(node.child, key = lambda c: c.Q)[-1]
         else:
            node = sorted(node.child, key = lambda c: c.Q)[0]
   elif recommendation_policy == "visits":
      while node.child != []:
         if node.playerSymbol == 1:
            node = sorted(node.child, key = lambda c: c.visits)[-1]
         else:
            node = sorted(node.child, key = lambda c: c.visits)[0]
   return node

def multiple_runs(state, function, player, runs, random_seed, divisions, dimension=0, division_method = "percentage", early_cut=False):
   random.seed(random_seed)
   random_seed_sequence = [random.randint(0,1000000) for _ in range(runs)]
   collective_data = []
   fo_logs = defaultdict(lambda:[])
   for run in range(runs):
      temp_player=player.ClonePlayer()
      random.seed(random_seed_sequence[run])
      np.random.seed(seed=random_seed_sequence[run])
      temp_player.chooseAction(state)
      data = tree_data(temp_player, divisions, dimension, early_cut)
      data.insert(0,"run",[run for _ in range(len(data))])
      collective_data.append(data)
      trt = False
      terminal_count = sum([1 for k,n in temp_player.nodes_dict.items() if n.untried_moves==[] and n.child ==[]])
      if terminal_count >= 1:
         trt = True
      fo_logs["Player"].append(temp_player.name)
      fo_logs["Tree_Nodes"].append(len(temp_player.nodes_dict))
      fo_logs["Max_Visits_Path"].append(function(best_tree_path(temp_player.nodes_dict[0],"visits").state.eval_point()))
      fo_logs["Max_Reward_Path"].append(function(best_tree_path(temp_player.nodes_dict[0]).state.eval_point()))
      fo_logs["Tree_Reaches_Terminal"].append(trt)
      fo_logs["Terminals_Reached"].append(terminal_count)
      fo_logs["Random_Seed"].append(random_seed_sequence[run])
   df_data = pd.concat(collective_data)
   fo_logs = pd.DataFrame(fo_logs)
   return fo_logs, df_data

def Collect_FO_logs(logs_path = "logs/FO", output_name = "collective_logs.csv", exp_names=None):
    """
    Collects data in "collective_tree_logs.csv".
    Logs names should be saved as "logs_path/Results_f0_c0.5" where f is the function, c is the parameter
    Logs in that folder should contain "Final_Player_logs.csv" and "Parameter_logs.csv"
    """
        
    if exp_names is None:
        exp_names = [ item for item in os.listdir(logs_path) if os.path.isdir(os.path.join(logs_path, item)) ]
    join = "/"
    final_df = pd.DataFrame()
    for i,exp_name in enumerate(exp_names):
        data = pd.read_csv(logs_path + join + exp_name + join + "Final_Player_logs.csv")
        pars = pd.read_csv(logs_path + join + exp_name + join + "Parameter_logs.csv")
        fi_list = [pars["func_index"][0] for _ in range(len(data))]
        c_list = [pars["c_param"][0] for _ in range(len(data))]
        expname_list = [exp_name for _ in range(len(data))]
        data["function"] = fi_list
        data["c"] = c_list
        data["expname"] = expname_list
        if i==0:
            final_df = pd.DataFrame(data)
        else:
            final_df = pd.concat([final_df,data]) 
    
    final_df.to_csv(logs_path + join + output_name, index=False)



#### Graph generation

def plot_functions(function_list, subplot_titles=None):
    n_plots = len(function_list)
    even_spaces = 1/(n_plots)
    row_heights = [even_spaces for _ in range(n_plots)]
    if subplot_titles is None:
        sub_titles = ["Function " + str(i+1) for i in range(len(function_list))]
    line_width = 1.5
    fig = make_subplots(rows=n_plots, cols=1,shared_xaxes=True,vertical_spacing=0.05,row_heights=row_heights, subplot_titles=sub_titles)
    #,subplot_titles=("Function 1","Function 2","Function 3","Function 4","Function 5"))

    show_legend = [False] + [False for _ in range(n_plots)]
    max_x = [0.5,0.867,0,0.1,0.1]
    for i,f in enumerate(function_list):
        x = np.linspace(0.001,1,5000)
        y = [f([i]) for i in x]
        fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"black"}),row=i+1,col=1)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_xaxes(range=[0, 1])
        fig.update_yaxes(range=[0, 1])
        #fig.add_vline(x=max_x[i],line_dash="dot")
    fig['layout'].update(shapes=[{'type': 'line','y0':0,'y1': 1,'x0':0.5, 
                                'x1':0.5,'xref':'x1','yref':'y1',
                                'line': {'color': "#B10909",'width': line_width, "dash":"dash"}},
                                {'type': 'line','y0':0,'y1': 1,'x0':0.867, 
                                'x1':0.867,'xref':'x2','yref':'y2',
                                'line': {'color': "#B10909",'width': line_width, "dash":"dash"}},
                                {'type': 'line','y0':0,'y1': 1,'x0':0.1, 
                                'x1':0.1,'xref':'x4','yref':'y4',
                                'line': {'color': "#B10909",'width': line_width, "dash":"dash"}},
                                {'type': 'line','y0':0,'y1': 1,'x0':0.1, 
                                'x1':0.1,'xref':'x5','yref':'y5',
                                'line': {'color': "#B10909",'width': line_width, "dash":"dash"}}])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=20),width=800,height=800,plot_bgcolor='rgba(0,0,0,0)'
                    #,title={"text":title}
                    ,font = dict(family = "Arial", size = 14, color = "black")
                ,legend=dict(
                    #orientation="h",
                    #yanchor="top",
                    y=-0.65,
                    xanchor="center",
                    x=0.5,  
                    font = dict(family = "Arial", size = 14, color = "black"),
                    #bordercolor="LightSteelBlue",
                    borderwidth=2,
                    itemsizing='trace',
                    itemwidth = 30
                    )  )
    #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
    fname_x = -0.08
    fname_y_span = 0.225
    fname_initial_y = 1
    fname_size = 30
    fname_names = ["f1","f2","f3","f4","f5"]
    """
    for i,f_name in enumerate(fname_names):
    fig.add_annotation(
            x=fname_x,
            y=fname_initial_y-i*fname_y_span,
            xref="paper",
            yref="paper",
            text=" "+f_name+" ",
            showarrow=False,
            font=dict(
                #family="Courier New, monospace",
                size=fname_size,
                color="black"
                ),
            align="left",
            #arrowhead=2,
            #arrowsize=1,
            #arrowwidth=2,
            #arrowcolor="#636363",
            #ax=20,
            #ay=-30,
            bordercolor="black",
            borderwidth=2,
            #borderpad=4,
            #bgcolor="#ff7f0e",
            #opacity=0.8
            )
    """
    return fig

def show_search(data_list, function, title, divisions, n_buckets = 100, subplot_titles=None, max_x_location = None, y_ref_value = None):
   """
   Returns a figure with histogram for each agent
   Input: Array of dataframes, one for each agent.

   Usage example:
   
   def get_subset(data, agent_name, f_index, c_param=None):
      temp_data = data.loc[data["f_index"]==f_index]
      if c_param is not None:
         temp_data = temp_data.loc[temp_data["c_param"]==c_param]
      #print(temp_data["player"].unique())
      temp_data = temp_data.loc[temp_data["player"] == agent_name]
      return temp_data

   dummy_state = FunctionOptimisationState(players=[None], function=0, ranges=[[0,1]], splits=2)
   functions = dummy_state.function_list
   join = "/"
   logs_path = "logs/Old/FO"
   data = pd.read_csv(logs_path + join + "collective_tree_logs.csv")
   n_buckets = 128
   f_max_locations = [0.5,0.867,None,0.1,0.1]

   for f_index in [0]:#,1,2,3,4]:
      agents_names = data["player"].unique()
      print(agents_names)
      c_params = data["c_param"].unique()
      c_params.sort()
      generic_name = "MCTS_c"
      agents_names = [x for x in agents_names]
      names = []
      data_list = []

      #order names
      for c in c_params:
         string_c = str(c)
         if string_c.split(".")[-1] == "0":
               string_c = string_c[:-2]
         names.append(generic_name + string_c)
      for name in agents_names:
         if "SE_MCTS" in name:
               names.append(name)
      for name in names:
         temp_data = get_subset(data, name, f_index)
         data_list.append(temp_data)
      
      treated_names = []
      for it,st in enumerate(names):
         new_string = st.replace("_c"," C = ")
         new_string = new_string.replace("1.414","\u221A\u03052\u0305fred")
         new_string = new_string.split("fred")[0]
         if "SE_MCTS" in new_string:
               if "2600" in new_string:
                  new_string = "SIEA_MCTS 2600 iterations"
               else:
                  new_string = "SIEA_MCTS 5000 iterations"
         treated_names.append(new_string)
      #plot = exps.show_search(data_list, functions[f_index], "", 3, n_buckets = n_buckets, subplot_titles = treated_names+["Function "+str(f_index+1)], max_x_location=f_max_locations[f_index], y_ref_value=None)
      plot = nshow_search(data_list, functions[f_index], "Exploration and exploitation distribution for Function " + str(f_index+1) + "." , 3, n_buckets = n_buckets, subplot_titles = ["Function "+str(f_index+1)] + treated_names, max_x_location=f_max_locations[f_index], y_ref_value=None)
      plot.write_image(os.path.join(logs_path, "F" + str(f_index+1) + "_results"+ str(n_buckets) + '.png'))#, width=800, height=800)
      plot.show()
   
   """ 

   if divisions in [2,3]: colors = ["#5B8C5A"
                ,"#56638A"
                , "#EC7316"]#["#355691","#C874D9","#820263"   ]#["#696969","#4f4f4f","#2f2f2f"]
   if divisions==4: colors = ["#cf0000","#a2000d","#740017","#53001b"]
   #colors = ["#1F77B4","#7FBF7B","#7B6F9D","#F5E050","#4CB5B0"]
   n_plots = len(data_list)
   even_spaces = 1/(n_plots+1)
   row_heights = [even_spaces for _ in range(n_plots)] + [even_spaces]
   fig = make_subplots(rows=n_plots+1
                       ,cols=1
                       ,shared_xaxes=True
                       ,vertical_spacing=0.04
                       ,row_heights=row_heights
                       ,subplot_titles = subplot_titles
                       , specs=[[{"secondary_y": True}] for _ in range(n_plots+1)]
                       ,x_title="Central point of the state represented by each node."
                       ,y_title='Total allocated nodes.'
                       #,print_grid=True
                       )
   
   if function is not None:
      x = np.linspace(0.001,1,5000)
      y = [function([i]) for i in x]
      fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"#000000"}),row=1,col=1)

   show_legend = [True] + [False for _ in range(n_plots)]
   for i,data in enumerate(data_list):
      for div in range(divisions):

         #Set name of the divisions
         if div%divisions == 0: s1 = "{:2.0f}".format(100*(div/divisions))
         else: s1 = "{:2.1f}".format(100*(div/divisions))
         if (div+1)%divisions == 0: s2 = "{:2.0f}".format(100*((div+1)/divisions))
         else: s2 = "{:2.1f}".format(100*((div+1)/divisions))
         div_name = s1 + "% to " + s2 + "%"
         temp_data = data.loc[data["id_block"]==div]
         
         #Set number of buckets as per arguments
         if type(n_buckets) is list:
            if i < len(n_buckets):
                n_bins = n_buckets[i]
            else: print("reached i ", i, " when max is ", str(len(n_buckets)))
         else: n_bins = n_buckets

         #Add histogram
         fig.add_trace(go.Histogram(x=temp_data.x
                  , nbinsx=n_bins
                  , xbins={"start":0,"end":1,"size":1/n_bins}
                  , name = div_name
                  , showlegend=show_legend[i]
                  , marker={"color":colors[div]}),row=i+2,col=1
                  #, legendgroup=div, name=div_name
                  )
         
         #Add secondary trace in the same plot
         #fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"black"}),row=i+1,col=1,secondary_y=True)

   fig.update_layout(margin=dict(l=70, r=10, t=30, b=50)
                     ,width=800
                     ,height=900
                     ,plot_bgcolor='rgba(0,0,0,0)'
                     ,title={"text":title}
                     ,barmode='stack'
                     ,font = dict(family = "Arial", size = 14, color = "black")
                     ,legend=dict(
                        title = "Total iterations"
                        ,orientation="v"
                        ,yanchor="top"
                        ,y=1.14
                        ,xanchor="right"
                        ,x=0.97
                        ,bgcolor="rgba(255, 255, 255, 0.8)"
                        ,font = dict(family = "Arial", size = 14, color = "black")
                        ,bordercolor="Black"
                        ,borderwidth=2
                        ,itemsizing='trace'
                        ,itemwidth = 30
                        ) 
                     )
   fig.update_xaxes(showline=True
                    , linewidth=2
                    , linecolor='black'
                    , mirror=True
                    )

   fig.update_yaxes(showline=True
                    ,mirror=True
                    , linewidth=2
                    , linecolor='black'
                    , nticks=5
                    #,tickmode = 'linear'
                    ,tick0 = 0
                    , gridcolor="#5B8C5A"
                    , gridwidth=0.1
                    #, dtick=5000
                    ,showgrid=False
                    )

   #Add line where the maximum x is
   list_of_shapes = []
   if max_x_location is not None:
      for subplot_n in range(1,n_plots+2):
         yref = "y" + str(subplot_n*2)
         list_of_shapes.append({'type': 'line','y0':0,'y1': 1,'x0':max_x_location, 
                                    'x1':max_x_location,'xref':"x",'yref':yref,
                                    'line': {'color': "#B10909",'width': 1.5, "dash":"dash"}})
   
   if y_ref_value is not None:
         for subplot_n in range(1,n_plots+1):
            yref = "y" + str(subplot_n*2-1)
            list_of_shapes.append({'type': 'line','y0':y_ref_value,'y1': y_ref_value,'x0':0, 
                                       'x1':1,'xref':"x",'yref':yref,
                                       'line': {'color': "#4F5D2F",'width': 1, "dash":"dash"}})
   
   if list_of_shapes != []:
      fig['layout'].update(shapes=list_of_shapes)
      for subplot_n in range(1, n_plots+2):
         yref = "y" + str(subplot_n)
         fig.add_shape(go.layout.Shape(type="line", yref=yref, xref="x", x0=max_x_location, x1 = max_x_location, y0=0, y1=1, line=dict(color="red", width=1),),row=subplot_n, col=1)
   
   for subplot_n in range(1,n_plots+2):
         fig['layout']['yaxis'+ str(subplot_n*2)]['visible'] = False

   return fig

def show_2d_search(data_list, function, title, divisions, n_buckets = 100):
   #Needs verification
   """
   Generates a 2d histogrem, where each row is a moment in the search. To show where the search was performed at which time
   """
   
   colors = ["#5e4e9c","#4169b0","#009ee3"]
   n_plots = len(data_list)
   even_spaces = 1/(n_plots+1)
   row_heights = [even_spaces for _ in range(n_plots)] + [even_spaces]
   fig = make_subplots(rows=n_plots+1, cols=1,shared_xaxes=True,vertical_spacing=0.05,row_heights=row_heights)

   show_legend = [False] + [False for _ in range(n_plots)]
   for i,data in enumerate(data_list):
      #temp_data = data.assign(div = lambda x: int((x.id/(len(data)+1))/(1/divisions)))
      div_list = [int((x["id"]/(max(data["id"])+1))/(1/divisions)) for i,x in data.iterrows()]
      #print("max div",max(div_list))
      temp_data = data.assign(div = div_list)
      fig.append_trace(go.Histogram2d(x=temp_data["x"]
                                       ,y=temp_data["div"]
                                       ,xbins={"start":0,"end":1,"size":1/n_buckets}
                                       ,ybins={"start":0,"end":divisions,"size":1}
                                       ,showlegend=show_legend[i]
                                       ,colorscale="ice")#[[0,colors[0],[0.5,colors[1]],[1,colors[2]]]])
                                    ,row=i+1,col=1)
   x = np.linspace(0.001,1,5000)
   y = [function([i]) for i in x]
   fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"black"}),row=n_plots+1,col=1)
   fig.update_layout(margin=dict(l=10, r=10, t=30, b=20),width=1000,height=800,plot_bgcolor='rgba(0,0,0,0)',title={"text":title}
                #,legend=dict(
                    #title = "Formula",
                    #orientation="h",
                    #yanchor="top",
                    #y=-0.65,
                    #xanchor="center",
                    #x=0.5,  
                    #font = dict(family = "Arial", size = 14, color = "black"),
                    #bordercolor="LightSteelBlue",
                    #borderwidth=2,
                    #itemsizing='trace',
                    #itemwidth = 30
                    #)  
                  )
   #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
   fig.show()

def show_search_depth(data_list, plot_title, data_distance = 20, markers_distance = 20, gray_scale=False):
   """
   Plots the average depth of the expanded node at each iteration

   Usage example:
    def get_subset(data, agent_name, f_index, c_param=None):
        temp_data = data.loc[data["f_index"]==f_index]
        if c_param is not None:
            temp_data = temp_data.loc[temp_data["c_param"]==c_param]
        #print(temp_data["player"].unique())
        temp_data = temp_data.loc[temp_data["player"] == agent_name]
        return temp_data

    dummy_state = FunctionOptimisationState(players=[None], function=0, ranges=[[0,1]], splits=2)
    functions = dummy_state.function_list
    join = "/"
    logs_path = "logs/Old/FO"
    output_name = "collective_tree_logs.csv"
    data = pd.read_csv(logs_path + join + "collective_tree_logs.csv")
    n_buckets = 400
    f_max_locations = [0.5,0.867,None,0.1,0.1]

    for f_index in [0]:#,1,2,3,4]:
    agents_names = data["player"].unique()
    #print(agents_names)
    c_params = data["c_param"].unique()
    c_params.sort()
    generic_name = "MCTS_c"
    agents_names = [x for x in agents_names]
    names = []
    data_list = []

    #order names
    for c in c_params:
        string_c = str(c)
        if string_c.split(".")[-1] == "0":
            string_c = string_c[:-2]
        names.append(generic_name + string_c)
    for name in agents_names:
        if "SE_MCTS" in name:
            names.append(name)
    for name in names:
        temp_data = get_subset(data, name, f_index)
        data_list.append(temp_data)

    treated_names = []
    temp_names = [x for x in names]
    for it,st in enumerate(temp_names):
        new_string = st.replace("_c"," C = ")
        new_string = new_string.replace("1.414","sqrt(2)fred")
        new_string = new_string.split("fred")[0]
        if "SE_MCTS" in new_string:
            if "2600" in new_string:
                new_string = "SE_MCTS partial simulations"
                #continue
            else:
                new_string = "SIEA_MCTS complete simulations"
        treated_names.append(new_string)

    for i,df in enumerate(data_list):
        df['player'] = df['player'].replace([names[i]],treated_names[i])

    for i,name in enumerate(treated_names):
        if name == "SE_MCTS partial simulations":
            del data_list[i]

    #plot = exps.show_search(data_list, functions[f_index], "", 3, n_buckets = n_buckets, type="divisions")#, subplot_titles = treated_names+["Function "+str(f_index+1)], max_x_location=f_max_locations[f_index], y_ref_value=None)
    plot = show_search_depth(data_list, "Average expansion depth by iteration. Function " + str(f_index+1), 30, 10)
    #depth_plot.write_image(os.path.join(logs_path, "depth" + str(f_index) + '.png'), width=600, height=350)
    #plot = show_search2(data_list, functions[f_index], "", 3, n_buckets = 200, type="divisions", subplot_titles = agents_names+["Function "+str(f_index)])
    plot.show()
    #depth_plot.write_image(os.path.join(logs_path, "depth_f" + str(f_index) + '.png'), width=800, height=400)
    #plot.write_image(os.path.join(logs_path, "depth_histo_max_2k_f" + str(f_index) + '.png'), width=800, height=800)
    #plot.write_image(os.path.join(logs_path, "Average_depth_by_iteration_f" + str(f_index+1) + '.png'), width=800, height=400)
   
   """
   if gray_scale:
      colors = ["#696969","#4f4f4f","#2f2f2f","#000000","#0f0f0f","#666666","#234654"]
   else:
      colors = ["#000000"
                , "#B10909"
                ,  "#5B8C5A"
                ,"#56638A"
                , "#EC7316"#"#9B6DC6 "
                ,  "#FC738C" ]


   markers = ["diamond","cross","x","triangle-up","triangle-down","star","star-square","corcle-cross","square", "pentagon"]
   marker_padding = int(markers_distance/len(data_list))

   fig = go.Figure()
   max_max_y = 0
   for data_idx, data in enumerate(data_list):#list(reversed(data_list)):
      name = data["player"].unique()[0]
      #if len(name) > 12: name = name[:12]
      #print(len(data))
      #temp_data = data.groupby(by="id").mean()
      #print(len(temp_data))
      x = data["id"].unique()
      x = [k for k in x if k%data_distance==0]
      #y = [stats.mean(data.loc[data["id"]==id,["feature_0"]]["feature_0"]) for id in x]
      y=[]
      for id in x:#list(reversed(x)):
         temp = data.loc[data["id"]==id,["feature_0"]]["feature_0"]
         #print("filtered_len",len(temp))
         y.append(stats.mean(temp))

      max_y = max(y)
      if max_y > max_max_y:
         max_max_y = max_y

      x_marker = []
      y_marker = []
      for count in range(len(x)):
         if count%(markers_distance+data_idx*marker_padding) == 0:
            x_marker.append(x[count])
            y_marker.append(y[count])

      fig.add_trace(go.Scatter(x=x, y=y
            ,showlegend=False
            ,name=name
            ,mode="lines"#+markers'#"markers"
            ,marker_symbol = markers[data_idx]# + "-open-dot"
                        #,marker_color = "black"
                        #,marker_size=9
                        ,marker=dict(
                            color=colors[data_idx]#"black",#"red",#'rgba(135, 206, 250, 0.5)',
                            ,size=9
                            ,line=dict(
                                #color='MediumPurple',
                                width=0.5)
                            )))#,marker_color = "black"))
      fig.add_trace(go.Scatter(x=x_marker, y=y_marker
            ,showlegend=True
            ,name=name
            ,mode="markers"#"markers"
            ,marker_symbol = markers[data_idx]# + "-open-dot"
                        #,marker_color = "black"
                        #,marker_size=9
                        ,marker=dict(
                            color=colors[data_idx]#"black",#"red",#'rgba(135, 206, 250, 0.5)',
                            ,size=9
                            ,line=dict( 
                                #color='MediumPurple',
                                width=0.5)
                            )))#,marker_color = "black"))
   fig.update_layout(
                #title_text=title
                #,title_x=0.5
                #,title_y=1
                #xaxis_title="Turn"
                #,yaxis_title="Nodes"
                autosize=False
                ,width=700
                ,height=350
                ,plot_bgcolor='rgba(0,0,0,0)'
                ,legend=dict(
                    #title = "Formula",
                    #orientation="h",
                    #yanchor="top",
                    y=0,
                    xanchor="right",
                    x=1,  
                    font = dict(family = "Arial", size = 11, color = "black"),
                    #bordercolor="LightSteelBlue",
                    borderwidth=2,
                    itemsizing='trace',
                    #itemwidth = 30
                    )
                ,title={"text":plot_title}
                )
   fig["layout"]["yaxis"]["tickmode"] = "linear"
   fig["layout"]["yaxis"]["tick0"] = 4
   fig["layout"]["yaxis"]["dtick"] = 2
   fig["layout"]["yaxis"]["showgrid"] = True
   fig["layout"]["yaxis"]["gridcolor"] = "black"
   fig["layout"]["yaxis"]["gridwidth"] = 0.6
   fig["layout"]["xaxis"]["tickmode"] = "linear"
   fig["layout"]["xaxis"]["tick0"] = 0
   fig["layout"]["xaxis"]["dtick"] = 500
   fig["layout"]["xaxis"]["showgrid"] = True
   fig["layout"]["xaxis"]["gridcolor"] = "black"
   fig["layout"]["xaxis"]["gridwidth"] = 0.6
   fig['layout'].update(margin=dict(
                                       l=20,
                                       r=10,
                                       b=0,
                                       t=30))    
   fig.update_xaxes(range=[0,5000])
   fig.update_yaxes(range=[6,max_max_y])
   fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   return fig

def fo_function_analysis(fo_state, title, max_depth=3, max_val=None):
   """
    Plots MCTS's fitness landscape for a 1d function
    
    Usage example:
    random_player = RandomPlayer()
    dummy_state = FunctionOptimisationState(players=[random_player], function=4, ranges=[[0,1]], splits=2)
    functions = dummy_state.function_list
    fig = fo_function_analysis(dummy_state, max_depth=5)
    fig.show()
   """

    #Initialize
   stop = fo_state.ranges[0][1]
   start = fo_state.ranges[0][0]

   #get max depth and step size
   step = fo_state.ranges[0][1] - fo_state.ranges[0][0]
   depth = 0
   while step > fo_state.minimum_step:
      depth += 1
      step = step / fo_state.splits
      if depth>1000:
         print("Infinite while error")
         break
   
   #Calculations
   bar_widths= []
   values_by_depth = {}
   x = np.linspace(start,stop,int((stop-start)/step))
   x=x[1:-1]
   y_dict = {xi:fo_state.function([xi]) for xi in x}
   for d in range(1,max_depth+1):
      bar_widths.append([1/(fo_state.splits**d) for _ in range(fo_state.splits**d)])
      divisions = fo_state.splits**d
      division_size = (stop-start)/divisions
      for i in range(divisions):
         section_begin = division_size*i
         section_end = division_size*(i+1)
         values = []
         for (k,v) in y_dict.items():
            if k > section_begin and k < section_end:
               values.append(v)
         values_by_depth[(d,i)] = stats.mean(values)
   #print(bar_widths)

   #create subplots
   n_plots = max_depth
   even_spaces = 1/(n_plots+1)
   row_heights = [even_spaces for _ in range(n_plots)] + [even_spaces]
   sub_titles = ["Function "+ str(fo_state.function_index)] + ["Tree depth " + str(i+1) for i in range(max_depth)]
   fig = make_subplots(rows=n_plots+1, cols=1,shared_xaxes=True,vertical_spacing=0.03,row_heights=row_heights, specs=[[{"secondary_y": True}] for _ in range(n_plots+1)], subplot_titles=sub_titles)
   
   #add function plot
   x = np.linspace(0.001,1,5000)
   y = [fo_state.function([i]) for i in x]
   fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"black"}),row=1,col=1)
   

   #add analysis plots
   for d in range(1,max_depth+1):
      widths = bar_widths[d-1]
      x = np.linspace(start,stop,((fo_state.splits**(d))*2)+1)
      x = [x[i] for i in range(1,len(x)) if i%2]
      #print(x)
      x=np.cumsum(widths)-widths
      #print(x)
      valid_keys = [k for k in values_by_depth.keys() if k[0] == d]
      y = [values_by_depth[k] for k in valid_keys]

      #Find max and change color
      max_y=max(y)
      colors = ["#5B8C5A" for _ in range(len(y))]
      for i, y_i in enumerate(y):
         if abs(max_y-y_i) < 0.0001:
            colors[i] = "#56638A"

      fig.add_trace(go.Bar(x=x
                           , y=y
                           , showlegend=False
                           ,marker_color=colors
                           ,width=widths
                           ,offset=0
                           )
                        ,row=d+1,col=1)
      fig.add_trace(go.Scatter(x=[start,stop], y=[max(y),max(y)], line=dict(color="#56638A", width=2, dash='dash'),showlegend=False,marker={"color":"#56638A"}),row=d+1,col=1)

      #add vertical lines
      if d > 1:
         x_breaks = np.linspace(start,stop,fo_state.splits**(d-1)+1)
         x_breaks = x_breaks[1:-1]
         for x_break in x_breaks:
            fig.add_trace(go.Scatter(x=[x_break,x_break], y=[0,1], showlegend=False,marker={"color":"black"}),row=d+1,col=1)
            pass

   #update fig layout
   fig.update_layout(barmode='stack')
   fig.update_layout(margin=dict(l=10, r=10, t=35, b=20),width=800,height=800,plot_bgcolor='rgba(0,0,0,0)',title={"text": title},font = dict(family = "Arial", size = 14, color = "black")
                ,legend=dict(
                    #title = "Formula",
                    #orientation="h",
                    #yanchor="top",
                    y=-0.65,
                    xanchor="center",
                    x=0.5,  
                    font = dict(family = "Arial", size = 14, color = "black"),
                    #bordercolor="LightSteelBlue",
                    borderwidth=2,
                    itemsizing='trace',
                    itemwidth = 30
                    )  )
   #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
   fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   # fig.update_xaxes(range=[start,stop])
   fig.update_xaxes(range=[0,1])
   fig.update_yaxes(range=[0,1])
   if max_val is not None:
         fig.add_shape({'type': 'line','y0':0,'y1': 1,'x0':max_val, 
                        'x1':max_val,
                        'line': {'color': "#B10909",'width': 1.5, "dash":"dash"}}, row="all", col=1)
   return fig

def fo_function_analysis_2d(fo_state, max_depth=3, print_logs=False):
   """Returns a figure with a 2d histogram plotting the function landscape as MCTS will se it. Manual (Fast)
    Usage example:
    random_player = RandomPlayer()
    dummy_state = FunctionOptimisationState(players=[random_player], function=6, ranges=[[0,1],[0,1]], minimum_step=0.001, splits=3)
    fig = exps.fo_function_analysis_2d(dummy_state, print_logs=True, max_depth=4)
    fig.show()
   """

   #Find evaluation points
   stop = {}
   start = {}
   max_depth_step = {}
   x = {}
   division_size = {}
   dimensions = len(fo_state.ranges)

   #splits by dimension
   for d in range(dimensions):
      
      stop[d] = fo_state.ranges[d][1]
      start[d] = fo_state.ranges[d][0]
      max_depth_step[d] = (stop[d]-start[d])/(fo_state.splits**max_depth)
      division_size[d] = stop[d] - start[d]
      while division_size[d] > fo_state.minimum_step:
         division_size[d] = division_size[d]/fo_state.splits   
      #if print_logs: print("dimension", d, " division_size", division_size[d], "start", start[d], "stop", stop[d], "max_detph_step", max_depth_step[d])

      #get central points
      x[d] = []   
      next_start = start[d]
      center_distance = division_size[d]/2
      while next_start+center_distance < stop[d]:
         next_stop = next_start + division_size[d]
         x[d].append(next_start+center_distance) #gets the value in the middle
         next_start = next_stop
      #if print_logs: print("x", x[d])
   #if print_logs: print("max_depth_step", max_depth_step)


   fig_x = {}
   fig_y = {}
   fig_z = {}
   for current_depth in reversed([md+1 for md in range(max_depth)]):
      depth_step = {}
      for d in range(dimensions):
         depth_step[d] = (stop[d]-start[d])/(fo_state.splits**current_depth)
      #if print_logs: print("current_depth", current_depth, "depth_step", depth_step)

      if max_depth == current_depth:
         granular_x = x[0]
         granular_y = x[1]
      else:
         granular_x = fig_x[current_depth+1]
         granular_y = fig_y[current_depth+1]
         granular_z = {}
         for i in range(len(granular_x)):
            granular_z[(granular_x[i], granular_y[i])] = fig_z[current_depth+1][i]

      all_depth_steps = {}
      for d in range(dimensions):
         all_depth_steps[d] = [[i*depth_step[d], (i+0.5)*depth_step[d], (i+1)*depth_step[d]] for i in range(fo_state.splits**current_depth)]
         all_depth_steps[d][0][0] = start[d]
         all_depth_steps[d][-1][2] = stop[d]
      #if print_logs: print("all_depth_steps shape:", str([str(k)+":"+str(len(v)) for k,v in all_depth_steps.items()]))
      #if print_logs: print("all_depth_steps max:", str(max([max(v) for k,v in all_depth_steps.items()])), str(min([min(v) for k,v in all_depth_steps.items()])))

      avg_by_y={}
      for j in granular_y:
         avg_by_y[j] = {}
         steps = 0
         count = 0
         accum = 0
         for i in granular_x:
            #if print_logs: print("i", i, "steps", steps)
            if i > all_depth_steps[0][steps][2]:
               avg_by_y[j][all_depth_steps[0][steps][1]] = accum/count
               count = 0
               accum = 0
               steps += 1
            if max_depth == current_depth:
               accum = accum + fo_state.function([i,j])
            else:
               accum = accum + granular_z[(i,j)]
            count += 1
         #if print_logs: print("i", i, "steps", steps)
         avg_by_y[j][all_depth_steps[0][steps][1]] = accum/count
         all_x_keys = avg_by_y[j].keys()
      #if print_logs: print("avg_by_y", avg_by_y)
      #if print_logs: print("all_x_keys", all_x_keys)

      fig_x[current_depth]=[]
      fig_y[current_depth]=[]
      fig_z[current_depth]=[]
      for i in all_x_keys:
         steps = 0
         count = 0
         accum = 0
         for j in avg_by_y.keys():
            if j > all_depth_steps[1][steps][2]:
               fig_x[current_depth].append(i)
               fig_y[current_depth].append(all_depth_steps[1][steps][1])
               fig_z[current_depth].append(accum/count)
               count = 0
               accum = 0
               steps += 1
            accum = accum + avg_by_y[j][i]
            count += 1
         fig_x[current_depth].append(i)
         fig_y[current_depth].append(all_depth_steps[1][steps][1])
         fig_z[current_depth].append(accum/count)


   #create subplots
   plot_pixels = 150
   n_plots = max_depth
   """
   if n_plots%2==0:
      row_heights = [1/(n_plots/2) for _ in range(int(n_plots/2))]
      column_widths = [0.5, 0.5]
   else:
   """
   row_heights = [1/n_plots for _ in range(n_plots)]
   column_widths = [1]
   #if print_logs: 
   #   print(row_heights, column_widths)
   #   print("rows",len(row_heights),"cols",len(column_widths))
   fig = make_subplots(
      rows=len(row_heights)
      ,cols=len(column_widths)
      ,shared_xaxes=True
      ,vertical_spacing=0.03
      ,row_heights = row_heights
      ,column_widths = column_widths
      #,specs=[[{"secondary_y": True}] for _ in range(len(column_widths))]
      )
   
   #add function plot
   #x = np.linspace(0.001,1,5000)
   #y = [fo_state.function([i]) for i in x]
   #fig.add_trace(go.Scatter(x=x, y=y, showlegend=False,marker={"color":"black"}),row=1,col=1)
   

   #add analysis plots
   n_ticks_colorbar = [0,3,0,0,0,0,0,0,0,0,0,0]
   for d in range(1,max_depth+1):
      if d==1: show_legend = True
      else: show_legend = False
      #print("n_bins", str(fo_state.splits**d))
      #if print_logs:
         #print("fig_x[d]", fig_x[d])
         #print("fig_y[d]", fig_y[d])
         #print("fig_z[d]", fig_z[d])
         #print("nbinsx",str(fo_state.splits**d))
      fig.add_trace(
         go.Histogram2d(x=fig_x[d], y=fig_y[d], z=fig_z[d],histfunc ="avg"
            #,autobinx =False
            #,nbinsx=5
            ,xbins = {"size":(stop[0]-start[0])/fo_state.splits**d}
            ,ybins = {"size":(stop[1]-start[1])/fo_state.splits**d}
            #,nbinsy=fo_state.splits**d
            #,color_continuous_scale="gray"
            ,colorscale = [[0, 'rgb(235,235,235)'], [1, 'rgb(0,0,0)']]
            ,showlegend = False
            ,colorbar = {"nticks":n_ticks_colorbar[d]}
            #,texttemplate= "%{z}"
            )
         ,row=d,col=1)
      #fig.add_trace(go.Scatter(x=[start,stop], y=[max(y),max(y)], line=dict(color='royalblue', width=2, dash='dash'),showlegend=False,marker={"color":"blue"}),row=d+1,col=1)

   #update fig layout
   #fig.update_layout(barmode='stack')
   fig.update_layout(margin=dict(l=10, r=10, t=30, b=20)
      ,width=plot_pixels+100
      ,height=plot_pixels*n_plots
      ,autosize=False
      ,plot_bgcolor='rgba(0,0,0,0)',title={"text":"2D Function analysis"}
                #,legend=dict(
                    #title = "Formula",
                    #orientation="h",
                    #yanchor="top",
                    #y=-0.65,
                    #xanchor="center",
                    #x=0.5,  
                    #font = dict(family = "Arial", size = 14, color = "black"),
                    #bordercolor="LightSteelBlue",
                    #borderwidth=2,
                    #itemsizing='trace',
                    #itemwidth = 30
                    #)  
                    )
   #fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
   #fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   #fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
   # fig.update_xaxes(range=[start,stop])
   fig.update_xaxes(range=[start[0],stop[0]])
   fig.update_yaxes(range=[start[1],stop[1]])
   

   return fig

