# import pandas
import pandas as pd
import math
import numpy as np

def get_inputs():
    """Asks the user whether they want
        1. a single player's data or comparative data between
        two players
        2. name(s) of the player(s)
        3. tournament of data

    Returns
    -------
    duo : boolean
        Whether the user wants comparative stats
    names : str array
        The name(s) of the player(s)
    tournaments : str array
        The name(s) of the tournament(s)
    """
    # Asks whether user wants solo or duo data
    duo_yn = input("Enter 1 for stats on one player, 2 for " +
    "comparative stats between 2 players: ")
    while duo_yn != '1' and duo_yn != '2':
        duo_yn = input("Error: invalid input. Only enter 1 or 2. " +
        "Enter 1 for stats on one player, 2 for comparative stats " +
        "between 2 players: ")

    # Asks for player name(s)
    names = []
    if duo_yn == '1':
        duo = False
        names.append(input("Player name: "))
    else:
        duo = True
        names.append(input("Player 1 name: "))
        names.append(input("Player 2 name: "))

    # Asks whether user wants a player's entire tournment history
    # or just one tournament
    tourn_all = input("Enter 1 for all-time stats, 2 for " +
    "one-tournament stats: ")
    while tourn_all != '1' and tourn_all != '2':
        tourn_all = input("Error: invalid input. Only enter 1 or 2. " +
        "Enter 1 for all-time stats, 2 for one-tournament stats: ")

    # Sets up tournaments
    tournaments = []
    if tourn_all == '1':
        tournaments.append(get_tourns(names[0]))
        if duo:
            tournaments.append(get_tourns(names[1]))
    else:
        tourn = input("Tournament name: ")
        tourn = tourn.replace(' ', '%20')
        tournaments.append([tourn])
        if duo:
            tournaments.append([tourn])

    # Check if input name is a valid name
    # if :
    #     alternative =
    #     yn_response = input("Do you mean " + alternative + "?")
    #     if yn_response == alternative:
    #         name = alternative

    return duo, names, tournaments

def get_dfs(name, tournament):
    """Uses the parameter information to retrieve the desired data and
    store in a data frame.

    Parameters
    ----------
    names : str
        The name of the player
    tournament : str
        The name of the tournament

    Returns
    -------
    match_df : Pandas data frame
        The data frame of the match history of input player and tournament
    champ_df : Pandas data frame
        The data frame of the champion stats of input player and tournament
    """

    # url with player name and tournament
    url = f'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryPlayer?pfRunQueryFormName=MatchHistoryPlayer&MHP%5Bpreload%5D=Player&MHP%5Btournament%5D={tournament}&MHP%5Blink%5D={name}&MHP%5Bchampion%5D=&MHP%5Brole%5D=&MHP%5Bteam%5D=&MHP%5Bpatch%5D=&MHP%5Byear%5D=&MHP%5Bregion%5D=&MHP%5Btournamentlevel%5D=&MHP%5Brecord%5D=&MHP%5Brecordorder%5D%5Bis_checkbox%5D=true&MHP%5Bitem%5D=&MHP%5Bjungleitem%5D=&MHP%5Bjungleenchant%5D=&MHP%5Brune%5D=&MHP%5Blimit%5D=50&MHP%5Bwhere%5D=&MHP%5Bincludelink%5D%5Bis_checkbox%5D=true&MHP%5Btextonly%5D%5Bis_checkbox%5D=true&wpRunQuery=Run+query&pf_free_text='

    dfs = pd.read_html(url)

    # take first table on the page
    match_df = dfs[0]
    champ_df = dfs[1]

    # filter match history table to just have necessary columns and rows
    match_df = match_df.droplevel(0, 1)
    match_df = match_df.dropna(subset=['Date', 'Tournament', 'W/L',
    'Len', 'K', 'D', 'A', 'CS', 'G'])
    match_df.drop(match_df.tail(1).index,inplace=True)
    match_df = match_df.dropna('columns')
    match_df = match_df.replace(to_replace =':', value = '.', regex = True)
    match_df = match_df.replace(to_replace ='k', value = '', regex = True)

    # change string elements to numeric
    match_df['K'] = pd.to_numeric(match_df['K'])
    match_df['D'] = pd.to_numeric(match_df['D'])
    match_df['A'] = pd.to_numeric(match_df['A'])
    match_df['CS'] = pd.to_numeric(match_df['CS'])
    match_df['Len'] = pd.to_numeric(match_df['Len'])
    match_df['min'] = match_df['Len'].apply(np.floor)
    match_df['sec'] = (match_df['Len'] - match_df['min']) / 0.6
    match_df['Len'] = match_df['min'] + match_df['sec']
    match_df['G'] = pd.to_numeric(match_df['G'])

    # filter champ table to just have necessary columns
    champ_df = champ_df.droplevel(0, 1)
    champ_df = champ_df.droplevel(0, 1)
    champ_df = champ_df.drop(champ_df.shape[0] - 1)
    champ_df = champ_df.drop(champ_df.shape[0] - 1)

    # change string elements to numeric
    champ_df['G'] = pd.to_numeric(champ_df['G'])
    # champ_df['W'] = pd.to_numeric(champ_df['W'])
    # champ_df['L'] = pd.to_numeric(champ_df['L'])
    # champ_df['KDA'] = pd.to_numeric(champ_df['KDA'])
    # champ_df['CS/M'] = pd.to_numeric(champ_df['CS/M'])

    return match_df, champ_df

def get_tourns(name):
    """Returns all the tournaments the named player has played in.

    Parameters
    ----------
    names : str array
        The name of the player

    Returns
    -------
    tourns : str array
        The list of tournaments the player has played in
    """

    # url with player name
    url = f'https://lol.fandom.com/wiki/{name}/Tournament_Results'

    dfs = pd.read_html(url)

    # get player's tournament history
    history = dfs[5]
    history = history.droplevel(0, 1)

    # convert column values into list
    tourns = history['Event'].values.tolist()

    # replace names to ones that can be recognized by query
    tourn = []
    for t in tourns:
        if "KeSPA" in t:
            t = t[-4:]
            t = t + ' lol kespa cup'
        elif "Worlds" in t:
            t = t[-4:]
            t = t + ' season world championship/main event'
        fixed = t.replace(' ', '%20')
        tourn.append(fixed)

    return tourn

def solo_data(match_df, champ_df):
    """Returns data on one player when only one player is input.

    Parameters
    ----------
    match_df : Pandas data frame
        The data frame of the match history of input player and tournament
    champ_df : Pandas data frame
        The data frame of the champion stats of input player and tournament

    Returns
    -------
    dictionary
        The player's stats (KDA, champion usage, itemizations, etc.)
    """

    player_stats = {}

    match_num_rows = match_df.shape[0]
    sum_data = match_df.sum(0, numeric_only=True)

    # Average KDA
    player_stats['KDA'] = round((sum_data.get('K') + sum_data.get('A')) / sum_data.get('D'), 2)

    # Average CS/M
    csm_per_game = match_df['CS'] / match_df['Len']
    player_stats['CS/M'] = round(sum(csm_per_game) / match_num_rows, 1)

    # Average Gold
    player_stats['Gold'] = round(sum_data.get('G') / match_num_rows, 1)

    # Winrate, based on individual games
    win_df = match_df.loc[match_df['W/L'] == 'Win']
    lose_df = match_df.loc[match_df['W/L'] == 'Loss']
    wins = win_df.shape[0]
    losses = lose_df.shape[0]
    player_stats['Winrate'] = round(wins / (wins + losses), 4) * 100

    # Top 5 Most Played Champions
    player_stats['Champions'] = champ_df.head(5)['Champion'].tolist()

    return player_stats

def duo_data(match_df1, champ_df1, match_df2, champ_df2):
    """Returns comparative data on two players

    Parameters
    ----------
    match_df1 : Pandas data frame
        The data frame of the match history of player1
    champ_df1 : Pandas data frame
        The data frame of the champion stats of player1
    match_df2 : Pandas data frame
        The data frame of the match history of player2
    champ_df2 : Pandas data frame
        The data frame of the champion stats of player2

    Returns
    -------
    comp_stats : dictionary
        Dictionary containing comparative stats between player1 and
        player2
    """
    comp_stats = {}

    # Calling solo_data on each player's data frames
    p1_overall = solo_data(match_df1, champ_df1)
    p2_overall = solo_data(match_df2, champ_df2)

    # Overall Stats Compared
    comp_stats['Overall KDA'] = [p1_overall['KDA'], p2_overall['KDA']]
    comp_stats['Overall CS/M'] = [p1_overall['CS/M'], p2_overall['CS/M']]
    comp_stats['Overall Gold'] = [p1_overall['Gold'], p2_overall['Gold']]
    comp_stats['Overall Winrate'] = [p1_overall['Winrate'], p2_overall['Winrate']]
    comp_stats['Common Top 5 Champions'] = list(set(p1_overall['Champions']).intersection(p2_overall['Champions']))

    # head-to-head match match history
    h2h = pd.merge(match_df1, match_df2, on=['Date', 'Len'], suffixes=('_1', '_2'))
    match_num_rows = h2h.shape[0]
    sum_data = h2h.sum(0, numeric_only=True)

    # Head-to-Head Win/Loss
    p1_wl_df = h2h.loc[h2h['W/L_1'] == 'Win']
    p2_wl_df = h2h.loc[h2h['W/L_2'] == 'Win']
    p1_wins = p1_wl_df.shape[0]
    p2_wins = p2_wl_df.shape[0]
    comp_stats['Head-to-head score'] = [p1_wins, p2_wins]

    # Head-to-Head KDA
    p1_kda = round((sum_data.get('K_1') + sum_data.get('A_1')) / sum_data.get('D_1'), 2)
    p2_kda = round((sum_data.get('K_2') + sum_data.get('A_2')) / sum_data.get('D_2'), 2)
    comp_stats['Head-to-head KDA'] = [p1_kda, p2_kda]

    # Head-to-Head CS/M
    p1_csm_pg = h2h['CS_1'] / h2h['Len']
    p2_csm_pg = h2h['CS_2'] / h2h['Len']
    p1_csm = round(sum(p1_csm_pg) / match_num_rows, 1)
    p2_csm = round(sum(p2_csm_pg) / match_num_rows, 1)
    comp_stats['Head-to-head CS/M'] = [p1_csm, p2_csm]

    # Head-to-Head Gold
    p1_gold = round(sum_data.get('G_1') / match_num_rows, 1)
    p2_gold = round(sum_data.get('G_2') / match_num_rows, 1)
    comp_stats['Head-to-head Gold'] = [p1_gold, p2_gold]

    return comp_stats

if __name__ == "__main__":
    # get user input
    duo, names, tournaments = get_inputs()

    # if it's duo or solo data
    if duo:
        # find common tournaments
        common_tourn = list(set(tournaments[0]).intersection(tournaments[1]))

        # player 1
        matches, champs = [], []
        for t in common_tourn:
            match, champ = get_dfs(names[0], t)
            matches.append(match)
            champs.append(champ)
        p1_match = pd.concat(matches)
        champs = pd.concat(champs)
        p1_champ = champs.groupby(by=['Champion'], sort=False, as_index=False).sum()
        p1_champ = p1_champ.sort_values(by=['G'], ascending=False)

        # player 2
        matches, champs = [], []
        for t in common_tourn:
            match, champ = get_dfs(names[1], t)
            matches.append(match)
            champs.append(champ)
        p2_match = pd.concat(matches)
        champs = pd.concat(champs)
        p2_champ = champs.groupby(by=['Champion'], sort=False, as_index=False).sum()
        p2_champ = p2_champ.sort_values(by=['G'], ascending=False)

        stats = duo_data(p1_match, p1_champ, p2_match, p2_champ)
    else:
        matches, champs = [], []
        for t in tournaments[0]:
            match, champ = get_dfs(names[0], t)
            matches.append(match)
            champs.append(champ)
        p1_match = pd.concat(matches)
        champs = pd.concat(champs)
        p1_champ = champs.groupby(by=['Champion'], sort=False, as_index=False).sum()
        p1_champ = p1_champ.sort_values(by=['G'], ascending=False)

        stats = solo_data(p1_match, p1_champ)

    print(stats)
