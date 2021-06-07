# import requests
from bs4 import BeautifulSoup
from selenium import webdriver

most_recent_tourn = "LCK 2020 Summer"

def get_page():
    """Asks the user for a player name and returns page data of match
    history of that player
    (player name, tournament name)

    Returns
    -------
    Driver
        The driver that has url of page
    """

    name = input("Player name: ")

    # Check if input name is a valid name
    # if :
    #     alternative =
    #     yn_response = input("Do you mean " + alternative + "?")
    #     if yn_response == alternative:
    #         name = alternative

    # url with player name and tournament
    url = f'https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryPlayer?pfRunQueryFormName=MatchHistoryPlayer&MHP%5Bpreload%5D=Player&MHP%5Btournament%5D={most_recent_tourn}&MHP%5Blink%5D={name}&MHP%5Bchampion%5D=&MHP%5Brole%5D=&MHP%5Bteam%5D=&MHP%5Bpatch%5D=&MHP%5Byear%5D=&MHP%5Bregion%5D=&MHP%5Btournamentlevel%5D=&MHP%5Brecord%5D=&MHP%5Brecordorder%5D%5Bis_checkbox%5D=true&MHP%5Bitem%5D=&MHP%5Bjungleitem%5D=&MHP%5Bjungleenchant%5D=&MHP%5Brune%5D=&MHP%5Blimit%5D=50&MHP%5Bwhere%5D=&MHP%5Bincludelink%5D%5Bis_checkbox%5D=true&MHP%5Btextonly%5D%5Bis_checkbox%5D=true&wpRunQuery=Run+query&pf_free_text='

    # set driver to get url
    driver = webdriver.Chrome('env/chromedriver')
    driver.get(url)

    return driver

def solo_data(driver):
    """Returns data on one player when only one player is input

    Parameters
    ----------
    driver : Driver
        The driver that has url of page

    Returns
    -------
    dictionary
        The player's stats (KDA, champion usage, itemizations, etc.)
    """

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table', class_='mhplayer')
    print(table)

    driver.quit()
    return

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
    player_page = get_page()
    data = solo_data(player_page)
    # print(data)
