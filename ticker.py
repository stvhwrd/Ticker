#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''show scores of today's NHL games'''

import datetime
import json
import os
import platform
import sys
import time
import requests
from colorama import init, Fore, Style
from pytz import reference

REFRESH_TIME = 30  # Minimize delay by doubling the API refresh rate
API_URL = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp'
TEST = False


def main():
    '''generates a scoreboard of today's NHL games'''
    games_today = False
    playoffs = False

    # Today's date
    t_object = datetime.datetime.now()
    today_date = "" + t_object.strftime("%A") + " " + "%s/%s" % (t_object.month, t_object.day)

    # Yesterday's date
    y_object = t_object - datetime.timedelta(days=1)
    yesterday_date = "" + y_object.strftime("%A") + " " + "%s/%s" % (y_object.month, y_object.day)

    while True:
        scraped_page = requests.get(API_URL)

        # Convert the scraped page to text and trim
        scraped_page = scraped_page.text.replace('loadScoreboard(', '')
        scraped_page = scraped_page[:-1]

        # Create JSON object
        data = json.loads(scraped_page)

        clear_screen()

        for key in data:
            if key == 'games':
                for game_info in data[key]:
                    # extract useful info from JSON
                    game_id = str(game_info['id'])
                    game_clock = game_info['ts']
                    game_stage = game_info['tsc']
                    status = game_info['bs']

                    away_locale = fix_locale(game_info['atn'])
                    away_name = fix_name(game_info['atv']).title()
                    away_score = game_info['ats']
                    away_result = game_info['atc']

                    home_locale = fix_locale(game_info['htn'])
                    home_name = fix_name(game_info['htv']).title()
                    home_score = game_info['hts']
                    home_result = game_info['htc']

                    if game_id[4:6] == '03':
                        playoffs = True
                        series_game_number = game_id[-1:]

                    # Show today's games
                    if today_date in game_clock.title() \
                        or 'TODAY' in game_clock \
                            or 'LIVE' in status:
                        games_today = True
                        header_text = away_locale + ' ' + away_name + \
                            ' @ ' + home_locale + ' ' + home_name

                        # Show the game number of current 7-game series,
                        # if it's playoff time
                        if playoffs:
                            header_text += ' -- Game ' + series_game_number

                        # Different displays for different states of game:
                        # Game from yesterday, ex: YESTERDAY (FINAL 2nd OT)
                        # Game from today finished, ex: TODAY (FINAL 2nd OT)
                        if 'FINAL' in status:
                            if yesterday_date in game_clock.title():
                                header_text += '\nYESTERDAY '
                            elif today_date in game_clock.title() or 'TODAY' in game_clock:
                                header_text += '\nTODAY '
                            else:
                                header_text += game_clock.title()
                            header_text += '(' + status + ')'

                        # Upcoming game, ex: TUESDAY 4/21, 7:00 PM MDT)
                        elif 'DAY' in game_clock and 'FINAL' not in status:
                            timezone = local_time()
                            header_text += Fore.YELLOW + \
                                '\n(' + game_clock + ', ' + status + \
                                ' ' + timezone + ')' + Fore.RESET

                        # Last 5 minutes of game and all of overtime,
                        # eg. (1:59 3rd PERIOD) in *red* font
                        elif 'LIVE' in status and 'critical' in game_stage:
                            header_text += Fore.RED + \
                                '\n(' + game_clock + ' PERIOD)' + Fore.RESET

                        # Any other time in game
                        # eg. (10:34 1st PERIOD)
                        else:
                            header_text += Fore.YELLOW + \
                                '\n(' + game_clock + Style.RESET_ALL
                            if 'PRE GAME' not in game_clock:
                                header_text += Fore.YELLOW + ' PERIOD'

                            header_text += Fore.YELLOW + ')' + Style.RESET_ALL

                        print header_text

                        # Highlight the winner of finished games in blue, games underway in green:
                        if away_result == 'winner':  # Away team wins
                            print Style.BRIGHT + Fore.BLUE + away_name + ' ' + away_score \
                                  + Style.RESET_ALL + ' - ' + home_score + ' ' + home_name
                        elif home_result == 'winner':  # Home team wins
                            print away_name + ' ' + away_score + ' - ' + Style.BRIGHT \
                                  + Fore.BLUE + home_score + ' ' + home_name + Style.RESET_ALL
                        elif 'progress' in game_stage or 'critical' in game_stage:  # Game underway
                            print Fore.GREEN + away_name + ' ' + away_score + ' - ' \
                                  + home_score + ' ' + home_name + Fore.RESET
                        print '\n'

        if not games_today:
            print "\nThere are no NHL games scheduled for today.\n"

        # Perform the sleep only if we're not currently testing
        if TEST is True:
            sys.exit(0)
        else:
            time.sleep(REFRESH_TIME)
            print '\n'


def clear_screen():
    '''os-adaptive screen wipe'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def fix_locale(team_locale):
    '''modify place names from the values in JSON'''
    if 'NY ' in team_locale:
        return 'New York'
    elif 'Montr' in team_locale:
        return u'Montréal'

    return team_locale


def fix_name(team_name):
    '''modify team names from the values in JSON'''
    if 'wings' in team_name:
        return 'Red Wings'
    elif 'jackets' in team_name:
        return 'Blue Jackets'
    elif 'leafs' in team_name:
        return 'Maple Leafs'
    elif 'knights' in team_name:
        return 'Golden Knights'

    return team_name


def local_time():
    '''get local timezone'''
    today = datetime.datetime.now()
    localtime = reference.LocalTimezone()
    return localtime.tzname(today)


def parse_arguments(arguments):
    '''process the arguments provided at runtime'''
    for index in range(1, len(arguments)):
        argument = arguments[index]

        if argument == '--test' or argument == '-t':
            print 'Running in TEST mode.\n'
            global TEST
            TEST = True


if __name__ == '__main__':
    init() # colorama
    parse_arguments(sys.argv)
    main()

# Originally forked from John Freed's NHL-Scores - https://github.com/jtf323/NHL-Scores
