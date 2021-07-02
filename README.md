# League Pro Compare
A tool that can compare the competitive stats of two League of Legends
pro players.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)

## General Information
Given the name of one to two League of Legends pro players and the name
of a tournament, the program web scrapes the League of Legends Gampedia
wiki to return comparative stats between the two players (or just solo
stats if given only one name).

This was made to help with more quickly comparing the performance of
two players in a specific tournament.

## Technologies Used
- Python - version 3.7.4
- Pandas - version 1.2.4
- Numpy - version 1.20.3

## Features
List the ready features here:
- Get a player's KDA, CS/M, Gold, Winrate, and Top 5 Most Used Champions
- Compare two players' stats and see which common champions they have in common

## Setup
`requirements.txt` is located in the root directory.

From the root directory, do:
`pip install -r requirements.txt`


## Usage
First, run from the root directory:
`python main.py`

- To get stats for one player, enter `1`, the name of the player, and the name of the tournament.
  - Example:
    ```
    Enter 1 for stats on one player, 2 for comparative stats between 2 players: 1
    Player name: Chovy
    Enter 1 for all-time stats, 2 for one-tournament stats: 2
    Tournament name: LCK 2020 Summer
    ```
    This returns:
    `{'KDA': 4.23, 'CS/M': 9.8, 'Gold': 14.3, 'Winrate': 71.11, 'Champions': ['Azir', 'Twisted Fate', 'Sett']}`

- To get stats for one player across all tournaments, enter `1`, the name of the player, and then `1`.
  - Example:
    ```
    Enter 1 for stats on one player, 2 for comparative stats between 2 players: 1
    Player name: ShowMaker
    Enter 1 for all-time stats, 2 for one-tournament stats: 1
    ```
    This returns:
    `{'KDA': 6.16, 'CS/M': 9.0, 'Gold': 13.5, 'Winrate': 68.26, 'Champions': ['Zoe', 'Syndra', 'Corki', 'Akali', 'LeBlanc']}`

- To get comparative stats between two players, enter `2`, the names of the players, and the name of the tournament.
  - Example:
    ```
    Enter 1 for stats on one player, 2 for comparative stats between 2 players: 2
    Player 1 name: Bjergsen
    Player 2 name: Jensen
    Enter 1 for all-time stats, 2 for one-tournament stats: 2
    Tournament name: LCS 2020 Summer
    ```
    This returns:
    `{'Overall KDA': [6.46, 5.74], 'Overall CS/M': [8.7, 9.3], 'Overall Gold': [14.2, 15.3], 'Overall Winrate': [66.67, 83.33], 'Common Top 5 Champions': ['LeBlanc', 'Twisted Fate', 'Syndra'], 'Head-to-head score': [0, 2], 'Head-to-head KDA': [1.0, 7.0], 'Head-to-head CS/M': [8.5, 10.0], 'Head-to-head Gold': [9.9, 12.6]}`

- To get comparative stats between two players across all tournaments, enter `2`, the names of the players, and then `1`.
  - Example:
    ```
    Enter 1 for stats on one player, 2 for comparative stats between 2 players: 2
    Player 1 name: ShowMaker
    Player 2 name: Chovy
    Enter 1 for all-time stats, 2 for one-tournament stats: 1
    ```
    This returns:
    `{'Overall KDA': [6.02, 5.08], 'Overall CS/M': [9.0, 9.8], 'Overall Gold': [13.5, 13.9], 'Overall Winrate': [66.67, 63.31], 'Common Top 5 Champions': ['Zoe', 'Akali'], 'Head-to-head score': [25, 24], 'Head-to-head KDA': [4.64, 3.85], 'Head-to-head CS/M': [8.7, 9.9], 'Head-to-head Gold': [12.8, 14.0]}`

## Project Status
Project is: _tentatively completed_.


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Check validity of inputs
- Resolve problems from when two players have the same game name
- Allow user to choose alternative input if original input is invalid
- Tournament name conflicts

To do:
- Output stats in table format
- Set up website where the user can use the program
