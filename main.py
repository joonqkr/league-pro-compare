# import pandas
import pandas as pd

import math

# hard coded tournament
most_recent_tourn = "LCK%202020%20Summer"

def get_dfs():
    """Asks the user for a player name and returns data frame of match
    history of that player
    (player name, tournament name)

    Returns
    -------
    match_df : Pandas data frame
        The data frame of the match history of input player and tournament
    champ_df : Pandas data frame
        The data frame of the champion stats of input player and tournament
    """

    name = input("Player name: ")

    # tourn = input("Tournament name: ")

    # Check if input name is a valid name
    # if :
    #     alternative =
    #     yn_response = input("Do you mean " + alternative + "?")
    #     if yn_response == alternative:
    #         name = alternative

    # url with player name and tournament
    url = f'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryPlayer?pfRunQueryFormName=MatchHistoryPlayer&MHP%5Bpreload%5D=Player&MHP%5Btournament%5D={most_recent_tourn}&MHP%5Blink%5D={name}&MHP%5Bchampion%5D=&MHP%5Brole%5D=&MHP%5Bteam%5D=&MHP%5Bpatch%5D=&MHP%5Byear%5D=&MHP%5Bregion%5D=&MHP%5Btournamentlevel%5D=&MHP%5Brecord%5D=&MHP%5Brecordorder%5D%5Bis_checkbox%5D=true&MHP%5Bitem%5D=&MHP%5Bjungleitem%5D=&MHP%5Bjungleenchant%5D=&MHP%5Brune%5D=&MHP%5Blimit%5D=50&MHP%5Bwhere%5D=&MHP%5Bincludelink%5D%5Bis_checkbox%5D=true&MHP%5Btextonly%5D%5Bis_checkbox%5D=true&wpRunQuery=Run+query&pf_free_text='

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
    """Returns data on one player when only one player is input

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

    # Win/Loss Ratio - more team-based so might not do

    # Top 3 Most Played Champions
    champions = []
    for i in range(3):
        champions.append(champ_df.at[i, 'Champion'])
    player_stats['Champions'] = champions

    return player_stats

def duo_data():
    """Returns comparative data on two players

    Parameters
    ----------
    name_one : str
        The name of the player 1
    name_two : str
        The name of player 2

    Returns
    -------
    dictionary
        Dictionary containing each player's stats as well as
        comparative stats
    """
    return

if __name__ == "__main__":

    match_df, champ_df = get_dfs()
    stats = solo_data(match_df, champ_df)
    print(stats)
