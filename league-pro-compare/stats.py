# import statements
import pandas as pd

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