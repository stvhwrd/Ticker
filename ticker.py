#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show live scores of today's NHL games"""

import argparse
import datetime
import json
import os
import platform
import requests
import sys
import time
from colorama import init, Fore, Style

# API purportedly updates every 60 seconds
REFRESH_TIME = -1

class Game:
    """Game represents a scheduled NHL game"""

    def __init__(self, game_info):
        self.game_id     = str(game_info['id'])
        self.game_clock  = game_info['ts']
        self.game_stage  = game_info['tsc']
        self.status      = game_info['bs']
        self.away_locale = fix_locale(game_info['atn'])
        self.away_name   = fix_name(game_info['atv'])
        self.away_score  = game_info['ats']
        self.away_result = game_info['atc']
        self.home_locale = fix_locale(game_info['htn'])
        self.home_name   = fix_name(game_info['htv'])
        self.home_score  = game_info['hts']
        self.home_result = game_info['htc']

        # Playoff-specific game information
        if '03' in self.game_id[4:6]:
            self.playoffs            = True
            self.playoff_round       = self.game_id[6:8]
            self.playoff_series_id   = self.game_id[8:9]
            self.playoff_series_game = self.game_id[9]
        else:
            self.playoffs = False

    def print_score(self, width):
        score = self.away_name + ' ' + self.away_score + \
            " - " + self.home_score + ' ' + self.home_name
        print(score.center(width))

    def print_matchup(self, width):
        matchup = self.away_locale + ' ' + self.away_name + \
            ' @ ' + self.home_locale + ' ' + self.home_name
        print(matchup.center(width))

    def print_playoff_info(self, width):
        round = self.playoff_round
        series = self.playoff_series_id
        playoff_info = playoffs_structure(round,series)
        playoff_info += ' -- GAME ' + self.playoff_series_game
        print(playoff_info.center(width))
        print(''.center(width, '-'))

    def print_clock(self, width):
        clock = self.game_clock + ' (' + self.status + ')'
        print(clock.center(width))

    def is_today(self):
        if 'TODAY' in self.game_clock or 'LIVE' in self.status:
            return True
        else:
            return False

def main():
    """Generate a scoreboard of today's NHL games"""

    while True:
        data = get_JSON('http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp')

        # Instantiate a Game object for each game in JSON
        games = []
        for game_info in data['games']:
            game = Game(game_info)
            if game.is_today():
                games.append(game)

        # Display current game information
        clear_screen()
        width = current_terminal_width()

        for game in games:
            print('\n')
            if game.playoffs is True:
                game.print_playoff_info(width)
            game.print_matchup(width)
            game.print_clock(width)
            game.print_score(width)
            print('\n')

        # Perform the sleep only if we're not currently testing
        if REFRESH_TIME > 0:
            time.sleep(REFRESH_TIME)
        else:
            os._exit(0)


def get_date(delta):
    """Build a date object with given day offset"""
    date = datetime.datetime.now()
    if delta is not None:
        offset = datetime.timedelta(days=delta)
        date = date + offset
    date = date.strftime("%A %-m/%-d")

    return date


def get_JSON(URL):
    "Request JSON from API server"
    response = requests.get(URL)
    if 'nhl' in URL:
        # Trim wrapper
        response = response.text.replace('loadScoreboard(', '')
        response = response.replace(')', '')
    return json.loads(response)


def clear_screen():
    """Clear terminal screen"""
    if os.name == 'NT':
        os.system('cls')
    else:
        os.system('clear')


def fix_locale(team_locale):
    """Expand and fix place names from the values in JSON"""
    if 'NY ' in team_locale:
        team_locale = 'New York'
    elif 'Montr' in team_locale:
        team_locale = u'Montréal'
    return team_locale.title()


def fix_name(team_name):
    """Expand team names from the values in JSON"""
    if 'wings' in team_name:
        team_name = 'Red Wings'
    elif 'jackets' in team_name:
        team_name = 'Blue Jackets'
    elif 'leafs' in team_name:
        team_name = 'Maple Leafs'
    elif 'knights' in team_name:
        team_name = 'Golden Knights'
    return team_name.title()


def parse_arguments(args):
    """Process the arguments provided at runtime"""
    args = args[1:]
    for arg in args:
        if arg == '--refresh' or arg == '-r':
            global REFRESH_TIME
            REFRESH_TIME = 30
        else:
            print ('Invalid flag supplied.  Please try again')
            os._exit(1)


def current_terminal_width():
    """Get the current with of the terminal window"""
    return os.get_terminal_size().columns


def playoffs_structure(round, series):
    round_info = {
        "01": {
            "1": "First Round: East #1 vs. Wildcard #2",
            "2": "First Round: Atlantic #2 vs. Atlantic #3",
            "3": "First Round: East #2 vs. Wildcard #1",
            "4": "First Round: Metropolitan #2 vs. Metropolitan #2",
            "5": "First Round: West #1 vs. Wildcard #2",
            "6": "First Round: Central #2 vs. Central #3",
            "7": "First Round: West #2 vs. Wildcard #1",
            "8": "First Round: Pacific #2 vs. Pacific #3",
        },
        "02": {
            "1": "Eastern Conference Semifinals",
            "2": "Eastern Conference Semifinals",
            "3": "Western Conference Semifinals",
            "4": "Western Conference Semifinals",
        },
        "03": {
            "1": "Eastern Conference Finals",
            "2": "Western Conference Finals",
        },
        "04": {
            "Stanley Cup Final": {
                "1": "Western Conference Champion vs. Eastern Conference Champion"
            },
        }
    }
    return round_info[round][series]

if __name__ == '__main__':
    init()  # colorama
    parse_arguments(sys.argv)
    main()

# Originally forked from John Freed's NHL-Scores - https://github.com/jtf323/NHL-Scores
