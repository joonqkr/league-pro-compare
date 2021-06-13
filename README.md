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
    Tournament name: LCK 2020 Summer
    ```
    This returns:
    `{'KDA': 4.23, 'CS/M': 9.8, 'Gold': 14.3, 'Winrate': 71.11, 'Champions': ['Azir', 'Twisted Fate', 'Sett']}`

- To get comparative stats between two players, enter `2`, the names of the players, and the name of the tournament.
  - Example:
    ```
    Enter 1 for stats on one player, 2 for comparative stats between 2 players: 2
    Player 1 name: Bjergsen
    Player 2 name: Jensen
    Tournament name: LCS 2020 Summer
    ```
    This returns:
    `{'Overall KDA': [6.46, 5.74], 'Overall CS/M': [8.7, 9.3], 'Overall Gold': [14.2, 15.3], 'Overall Winrate': [66.67, 83.33], 'Common Top 5 Champions': ['Orianna', 'LeBlanc', 'Syndra', 'Fiddlesticks', 'Twisted Fate']}`

## Project Status
Project is: _in progress_.


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Check validity of inputs
- Resolve problems from when two players have the same game name
- Allow user to choose alternative input if original input is invalid

To do:
- Generate head-to-head stats between two players
- Output stats in table format
- Stats over multiple tournaments / all tournaments
- Set up website where the user can use the program
