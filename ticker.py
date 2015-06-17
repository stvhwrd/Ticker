#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests


REFRESH_TIME = 30  # Minimize delay by doubling the API refresh rate
API_URL      = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp'


def main():
    ''''''
    intermission_clock = 18.0
    games_today        = False
    games_to_show      = 8
    saw_period_end     = True

    # Today's date
    t_object       = datetime.datetime.now()
    today_date     = "" + t_object.strftime("%A") + " " + "%s/%s" % (t_object.month, t_object.day)

    # Yesterday's date
    y_object       = t_object - datetime.timedelta(days=1)
    yesterday_date = "" + y_object.strftime("%A") + " " + "%s/%s" % (y_object.month, y_object.day)

    # Next two weeks
    next_two_weeks = []
    for index in range(1, 15):
        d_object   = t_object + datetime.timedelta(days=index)
        next_day   = "" + d_object.strftime("%A") + " " + "%s/%s" % (d_object.month, d_object.day)
        next_two_weeks.append(next_day)

    # Current season
    season = str(t_object.year - 1) + str(t_object.year) + '/'

    while True:
        clear_screen()

        scraped_page = requests.get(API_URL)

        # Convert the scraped page to text to do some cropping
        json_data    = scraped_page.text

        # Crop the leading text: 'loadScoreboard('
        json_data    = json_data.replace('loadScoreboard(', '')

        # Crop the trailing text: ')'
        json_data    = json_data[:-1]

        data         = json.loads(json_data)

        for key in data:
            if key == 'games':
                for game_info in data[key]:
                    # Assign more meaningful names
                    game_id     = str(game_info['id'])
                    game_clock  = game_info['ts']
                    game_stage  = game_info['tsc']
                    status      = game_info['bs']

                    away_locale = game_info['atn']
                    away_name   = game_info['atv'].title()
                    away_score  = game_info['ats']
                    away_result = game_info['atc']

                    home_locale = game_info['htn']
                    home_name   = game_info['htv'].title()
                    home_score  = game_info['hts']
                    home_result = game_info['htc']

                    # Fix strange names / locales returned by NHL
                    away_locale = fix_locale(away_locale)
                    home_locale = fix_locale(home_locale)
                    away_name   = fix_name(away_name)
                    home_name   = fix_name(home_name)

                    playoffs = False
                    series_game_number = game_id[-1:]
                    if game_id[4:6] == '03':
                        playoffs = True

                    # Show games from yesterday and today
                    if yesterday_date in game_clock.title() \
                    or today_date in game_clock.title() \
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

                        # Upcoming game, ex: TUESDAY 4/21, 7:00 PM PDT)
                        elif 'DAY' in game_clock and not 'FINAL' in status:
                            status = eastern_to_pacific(status)
                            header_text += Fore.YELLOW + '\n(' + game_clock + ', ' + status + ' PDT)' + Fore.RESET

                        # Last 5 minutes of game and overtime, ex: (1:59 3rd
                        # PERIOD) *in red font*
                        elif 'LIVE' in status and 'critical' in game_stage:
                            saw_period_end = True
                            header_text += Fore.RED + '\n(' + game_clock + ' PERIOD)' + Fore.RESET
                            if 'END 3rd' in game_clock or 'OT' in game_clock:
                                intermission_clock = 15.0
                            print_intermission_clock(header_text, intermission_clock)

                        # Any other time in game, ex: (10:34 1st PERIOD)
                        else:
                            header_text += Fore.YELLOW + '\n(' + game_clock + Style.RESET_ALL
                            if 'PRE GAME' not in game_clock:
                                saw_period_end = True
                                header_text += Fore.YELLOW + ' PERIOD'

                            # Display a countdown for 18 minutes of intermission (regular periods)
                            #     or 15 minutes of intermission (OVERTIME)
                            if 'END ' in game_clock and 'FINAL' not in status and saw_period_end:
                                if 'END 3rd' in game_clock or 'OT' in game_clock:
                                    intermission_clock = 15.0
                                print_intermission_clock(
                                    header_text, intermission_clock)

                            header_text += Fore.YELLOW + ')' + Style.RESET_ALL

                        print(header_text)

                        # Highlight the winner of finished games in blue, and games underway in green:
                        # Away team wins
                        if away_result == 'winner':
                            print(Style.BRIGHT + Fore.BLUE + away_name +
                                  ': ' + away_score + Style.RESET_ALL)
                            print(home_name + ': ' + home_score)

                        # Home team wins
                        elif home_result == 'winner':
                            print(away_name + ': ' + away_score)
                            print(Style.BRIGHT + Fore.BLUE + home_name +
                                  ': ' + home_score + Style.RESET_ALL)

                        # Game still underway
                        elif 'progress' in game_stage or 'critical' in game_stage:
                            print(Fore.GREEN + away_name + ': ' + away_score)
                            print(home_name + ': ' + home_score + Fore.RESET)

                        else:
                            print(away_name + ': ' + away_score)
                            print(home_name + ': ' + home_score)
                        print('')

                    elif not games_today:
                        if games_to_show > 0:
                            header_text = away_locale + ' ' + away_name + ' @ ' + home_locale + ' ' + home_name
                            # Show the game number of current 7-game series
                            # if it's playoff time
                            if playoffs:
                                header_text += ' -- Game ' + series_game_number

                            print header_text
                            print Fore.YELLOW + '(' + game_clock + ', ' + status + ' PDT)' + Fore.RESET
                            print away_name + ': ' + away_score
                            print home_name + ': ' + home_score
                            print ""
                            games_to_show -= 1

        # Perform the sleep
        time.sleep(REFRESH_TIME)


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def print_help():
    ''' response to the --help flag'''
    print 'By default games from yesterday and today will be displayed.'
    print ''


def parse_game_info(game_info):
    # Assign more meaningful names
    parsed_list = {
        game_id:     str(game_info['id']),
        game_clock:  game_info['ts'],
        game_stage:  game_info['tsc'],
        status:      game_info['bs'],
        away_locale: game_info['atn'],
        away_name:   game_info['atv'].title(),
        away_score:  game_info['ats'],
        away_result: game_info['atc'],
        home_locale: game_info['htn'],
        home_name:   game_info['htv'].title(),
        home_score:  game_info['hts'],
        home_result: game_info['htc'],
    }
    return parsed_list


def get_address(game_id, season):
    prefix = 'http://live.nhle.com/GameData/'
    suffix = '/gc/gcsb.jsonp'
    game_url = prefix + season + str(game_id) + suffix

    return game_url


def fix_locale(team_locale):
    # NHL API forces team name in locale for both New York teams, i.e. locale
    # + name == "NY Islanders islanders"
    if 'NY ' in team_locale:
        return 'New York'
    #
    if 'Montr' in team_locale:
        return u'Montréal'

    return team_locale


def print_intermission_clock(header_text, intermission_clock):
    header_text += Fore.YELLOW + ', ' + \
        str(intermission_clock) + ' minutes remaining in the intermission'
    intermission_clock -= (REFRESH_TIME / 60.0)
    if intermission_clock < 0:
        if 'END 3rd' in game_clock or 'OT' in game_clock:
            intermission_clock = 15.0
        else:
            intermission_clock = 18.0
    return header_text


def fix_name(team_name):
    # Change "redwings" to "Red Wings"
    if 'wings' in team_name:
        return 'Red Wings'

    # Change "bluejackets" to "Blue Jackets"
    if 'jackets' in team_name:
        return 'Blue Jackets'

    # Change "mapleleafs" to "Maple Leafs"
    if 'leafs' in team_name:
        return 'Maple Leafs'

    return team_name


def print_schedule():
    for games in next_two_weeks:
        print away_locale + ' ' + away_name + ' @ ' + home_locale + ' ' + home_name
        print Fore.YELLOW + '(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET
        print away_name + ': ' + away_score
        print home_name + ': ' + home_score
        print "\n"


def eastern_to_pacific(clock):
    '''Translate time into Pacific for us West Coast-ers'''
    pacific_time = {
        '12:00 PM': '9:00 AM',
        '1:00 PM': '10:00 AM',
        '2:00 PM': '11:00 AM',
        '3:00 PM': '12:00 PM',
        '4:00 PM': '1:00 PM',
        '5:00 PM': '2:00 PM',
        '6:00 PM': '3:00 PM',
        '7:00 PM': '4:00 PM',
        '8:00 PM': '5:00 PM',
        '9:00 PM': '6:00 PM',
        '10:00 PM': '7:00 PM',
        '11:00 PM': '8:00 PM',
    }
    return pacific_time[clock]


def parse_arguments(arguments):
    '''process the arguments provided at runtime'''
    for index in range(1, len(arguments)):
        argument = arguments[index]

        if argument == '--help' or argument == '-h':
            print_help()
            sys.exit(0)


if __name__ == '__main__':
    # Initialize Colorama
    init()

    # Parse any arguments provided
    parse_arguments(sys.argv)

    # Start the main loop
    main()

# The MIT License (MIT)

# Copyright (c) 2015 John Freed

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
