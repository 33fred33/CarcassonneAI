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

