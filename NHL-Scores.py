# -*- coding: utf-8 -*-
# Original Author: @jtf323
# Contributor: @stvhwrd

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

                    # NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
                    if 'NY ' in home_team_locale:
                        home_team_locale = 'New York'
                    if 'NY ' in away_team_locale:
                        away_team_locale = 'New York'

                    # NHL API refers to Detroit's team as "redwings" (one word)
                    if 'wings' in away_team_name:
                        away_team_name = 'Red Wings'
                    if 'wings' in home_team_name:
                        home_team_name = 'Red Wings'

                    # NHL API refers to Columbus' team as "bluejackets" (one word)
                    if 'jackets' in away_team_name:
                        away_team_name = 'Blue Jackets'
                    if 'jackets' in home_team_name:
                        home_team_name = 'Blue Jackets'

                    # NHL API refers to Toronto's team as "mapleleafs" (one word)
                    if 'leafs' in away_team_name:
                        away_team_name = 'Maple Leafs'
                    if 'leafs' in home_team_name:
                        home_team_name = 'Maple Leafs'


                    # Show games from today AND yesterday
                    if yesterdays_date in game_clock.title() or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:
                
                    #--- OR if you'd rather see only scores from today ---#
                
                    # Only show games from today
                    #if todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:

                        header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        

                        # Different displays:
                        
                        # finished game
                        if 'FINAL' in status:           # example (FINAL OT) 
                            if yesterdays_date in game_clock.title():
                                header_text += '\non ' + game_clock + ' '
                            else:
                                header_text += '\n'
                            header_text += '(' + status + ')'                           

                        # upcoming game
                        elif 'DAY' in game_clock:       # example (TUESDAY 4/21, 7:00 PM EST)
                            header_text += '\n(' + game_clock + ', ' + status + ' EST)'
                        
                        # pre game
                        elif 'PRE GAME' in game_clock:       # example (PRE GAME)
                            header_text += '\n(' + game_clock + ')'
                        
                        # last 5 minutes of game
                        elif 'critical' in game_stage:  # example output: (1:59 3rd PERIOD) **in RED**
                            header_text += '\n(' + Fore.RED +  game_clock  + ' PERIOD'+ Fore.RESET + ')'
                        
                        # any other time in game
                        else:                           # example (10:34 1st PERIOD)
                            header_text += '\n(' + game_clock + ' PERIOD)'

                        print header_text


                        # Highlight the winner of finished games in red, and games underway in green:

                        # Away team wins
                        if game_info['atc'] == 'winner':
                            print Fore.RED + away_team_name + ': ' + away_team_score + Fore.RESET
                            print home_team_name + ': ' + home_team_score
                        
                        # Home team wins
                        elif game_info['htc'] == 'winner':
                            print away_team_name + ': ' + away_team_score
                            print Fore.RED + home_team_name + ': ' + home_team_score + Fore.RESET

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


if __name__ == '__main__':
    init()
    main()
