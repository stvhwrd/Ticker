# -*- coding: utf-8 -*-
# Author: John Freed - @jtf323

import json
import os
import platform
import sys
import time
import datetime
import requests
from colorama import init, Fore, Back, Style

refresh_time = 60  # Refresh time (seconds), as per NHL API
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}


def main():
    clear_screen()

    # Format dates to match NHL API style:

    # Today's date
    t = datetime.datetime.now()
    todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
    
    # Yesterday's date
    y = t - datetime.timedelta(days=1)
    yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)


    while True:
        clear_screen()

        r = requests.get(api_url, headers=api_headers)
        
        # We get back json data with some JS around it, gotta remove the JS
        json_data = r.text

        # Remove the leading JS
        json_data = json_data.replace('loadScoreboard(', '')

        # Remove the trailing ')'
        json_data = json_data[:-1]

        data = json.loads(json_data)
        for key in data:
            if key == 'games':
                for game_info in data[key]:

                    # Assign more meaningful names    
                    game_clock = game_info['ts']
                    game_stage = game_info['tsc']
                    status = game_info['bs']

                    away_team_locale = game_info['atn']
                    away_team_name = game_info['atv'].title()
                    away_team_score = game_info['ats']

                    home_team_locale = game_info['htn']
                    home_team_name = game_info['htv'].title()
                    home_team_score = game_info['hts']

                    # Fix strange names / loacles returned by NHL
                    away_team_locale = fix_locale(away_team_locale)
                    home_team_locale = fix_locale(home_team_locale)
                    away_team_name = fix_name(away_team_name)
                    home_team_name = fix_name(home_team_name)

                    # Show games from today AND yesterday
                    if yesterdays_date in game_clock.title() or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:
                    
                    # Use the below line to only show games from today
                    #if todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:

                        header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        
                        # Different displays:
                        # Finished game ex: "(FINAL OT)"
                        if 'FINAL' in status:
                            if yesterdays_date in game_clock.title():
                                header_text += '\non ' + game_clock + ' '
                            else:
                                header_text += '\n'
                            header_text += '(' + status + ')'                           

                        # Upcoming game ex: "(TUESDAY 4/21, 7:00 PM EST)"
                        elif 'DAY' in game_clock:
                            header_text += '\n(' + game_clock + ', ' + status + ' EST)'
                        
                        # Pre game ex: "(PRE GAME)"
                        elif 'PRE GAME' in game_clock:
                            header_text += '\n(' + Fore.BLUE + game_clock + Fore.RESET + ')'
                        
                        # Last 5 minutes of game
                        elif 'critical' in game_stage:
                            header_text += '\n(' + Fore.RED +  game_clock  + ' PERIOD'+ Fore.RESET + ')'
                        
                        # Any other point in the game ex: "(10:34 1st PERIOD)"
                        else:
                            header_text += '\n(' + Fore.YELLOW + game_clock + ' PERIOD' + Fore.RESET + ')'

                        print header_text


                        # Highlight the winner of finished games in red, and games underway in green:
                        # Away team wins
                        if game_info['atc'] == 'winner':
                            print Fore.GREEN + away_team_name + ': ' + away_team_score + Fore.RESET
                            print home_team_name + ': ' + home_team_score
                        
                        # Home team wins
                        elif game_info['htc'] == 'winner':
                            print away_team_name + ': ' + away_team_score
                            print Fore.GREEN + home_team_name + ': ' + home_team_score + Fore.RESET

                        # Game still underway
                        elif 'progress' in game_stage or 'critical' in game_stage:
                            print Fore.GREEN + away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score + Fore.RESET

                        # Game hasn't yet started
                        else:
                            print away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score                              

                        print ''
                    
        # Perform the sleep
        time.sleep(refresh_time)


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def fix_locale(team_locale):
    # NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
    if 'NY ' in team_locale:
        return 'New York'

    return team_locale


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


if __name__ == '__main__':
    # Initialize Colorama
    init()

    # Start the main loop
    main()
