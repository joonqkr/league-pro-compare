# import statements
import pandas as pd
import numpy as np

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