# import statements
import pandas as pd
from .dataframes import get_dfs
from .stats import solo_data, duo_data

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

def main():
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

        data = duo_data(p1_match, p1_champ, p2_match, p2_champ)
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

        data = solo_data(p1_match, p1_champ)

    print(data)