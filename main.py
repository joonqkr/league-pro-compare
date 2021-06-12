# import pandas
import pandas as pd

import math

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
    tournament : str
        The name of the tournament
    """
    duo_yn = input("Enter 1 for stats on one player, 2 for " +
    "comparative stats between 2 players: ")

    while duo_yn != '1' and duo_yn != '2':
        duo_yn = input("Error: invalid input. Only enter 1 or 2. " +
        "Enter 1 for stats on one player, 2 for comparative stats " +
        "between 2 players: ")

    names = []
    if duo_yn == '1':
        duo = False
        names.append(input("Player name: "))
    else:
        duo = True
        names.append(input("Player 1 name: "))
        names.append(input("Player 2 name: "))

    tournament = input("Tournament name: ")
    tournament = tournament.replace(' ', '%20')

    # Check if input name is a valid name
    # if :
    #     alternative =
    #     yn_response = input("Do you mean " + alternative + "?")
    #     if yn_response == alternative:
    #         name = alternative

    return duo, names, tournament

def get_dfs(name, tournament):
    """Uses the parameter information to retrieve the desired data and
    store in a data frame.

    Parameters
    ----------
    duo : boolean
        Whether the user wants comparative stats
    names : str array
        The name(s) of the player(s)
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
    match_df = match_df.dropna(subset=['VOD'])
    match_df = match_df.drop(match_df.shape[0] - 1)
    match_df = match_df.dropna('columns')
    match_df = match_df.replace(to_replace =':', value = '.', regex = True)
    match_df = match_df.replace(to_replace ='k', value = '', regex = True)

    # change string elements to numeric
    match_df['K'] = pd.to_numeric(match_df['K'])
    match_df['D'] = pd.to_numeric(match_df['D'])
    match_df['A'] = pd.to_numeric(match_df['A'])
    match_df['CS'] = pd.to_numeric(match_df['CS'])
    match_df['Len'] = pd.to_numeric(match_df['Len'])
    for i in range(len(match_df['Len'])):
        original = match_df['Len'][i]
        minute = math.floor(original)
        seconds = (original - minute) / 0.6
        length = minute + seconds
        match_df.at[i, 'Len'] = length
    match_df['G'] = pd.to_numeric(match_df['G'])

    # filter champ table to just have necessary columns
    champ_df = champ_df.droplevel(0, 1)
    champ_df = champ_df.droplevel(0, 1)
    champ_df = champ_df.drop(champ_df.shape[0] - 1)
    champ_df = champ_df.drop(champ_df.shape[0] - 1)

    # change string elements to numeric
    champ_df['G'] = pd.to_numeric(champ_df['G'])
    champ_df['W'] = pd.to_numeric(champ_df['W'])
    champ_df['L'] = pd.to_numeric(champ_df['L'])
    champ_df['KDA'] = pd.to_numeric(champ_df['KDA'])
    champ_df['CS/M'] = pd.to_numeric(champ_df['CS/M'])

    return match_df, champ_df

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

    # Top 3 Most Played Champions
    champions = []
    for i in range(5):
        champions.append(champ_df.at[i, 'Champion'])
    player_stats['Champions'] = champions

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
    p1_overall = solo_data(match_df1, champ_df1)
    p2_overall = solo_data(match_df2, champ_df2)

    comp_stats['Overall KDA'] = [p1_overall['KDA'], p2_overall['KDA']]
    comp_stats['Overall CS/M'] = [p1_overall['CS/M'], p2_overall['CS/M']]
    comp_stats['Overall Gold'] = [p1_overall['Gold'], p2_overall['Gold']]
    comp_stats['Overall Winrate'] = [p1_overall['Winrate'], p2_overall['Winrate']]
    comp_stats['Common Top 5 Champions'] = list(set(p1_overall['Champions']).intersection(p1_overall['Champions']))

    return comp_stats

if __name__ == "__main__":
    duo, names, tournament = get_inputs()
    if duo:
        p1_match, p1_champ = get_dfs(names[0], tournament)
        p2_match, p2_champ = get_dfs(names[1], tournament)
        stats = duo_data(p1_match, p1_champ, p2_match, p2_champ)
    else:
        match, champ = get_dfs(names[0], tournament)
        stats = solo_data(match, champ)

    print(stats)
