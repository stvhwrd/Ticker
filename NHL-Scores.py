# Author: @jtf323
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
    now = datetime.datetime.now()
    today = "" + time.strftime("%A") + " " + "%s/%s" % (now.month, now.day)

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
                    gameID = game_info['id']
                    game_clock = game_info['ts']
                    status = game_info['bs']

                    away_team_locale = game_info['atn']
                    away_team_name = game_info['atv'].title()
                    away_team_score = game_info['ats']

                    home_team_locale = game_info['htn']
                    home_team_name = game_info['htv'].title()
                    home_team_score = game_info['hts']

                    # NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders Ny Islanders"
                    if 'NY ' in home_team_locale:
                        home_team_locale = 'New York'
                    if 'NY ' in away_team_locale:
                        away_team_locale = 'New York'

                    # Only show games that are scheduled for today or still in progress
                    if game_clock.lower() == today.lower() or status == 'LIVE':
                        header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        
                        # Check if the game is over, hasn't started yet, or is still in progress
                        if 'FINAL' in status:
                            header_text += '\n(' + status + ')'    # example (FINAL OT)                        
                        elif 'DAY' in game_clock:
                            header_text += '\n(' + game_clock + ', ' + status + ' EST)' # example (TUESDAY 4/21, 7:00 PM EST)
                        elif game_info['tsc'] == 'critical':
                            header_text += Fore.RED + '\n(' + game_clock + ' period)' + Fore.RESET    # example output: (10:34 3rd period)
                        else:
                            header_text += '\n(' + game_clock + ' period)'     # example (10:34 3rd period)

                        print header_text

                        #highlight the winner = green, loser = red, still playing = yellow
                        if game_info['atc'] == 'winner':
                            print Fore.GREEN + away_team_name + ': ' + away_team_score + Fore.RESET
                            print Fore.RED + home_team_name + ': ' + home_team_score + Fore.RESET 
                        
                        elif game_info['htc'] == 'winner':
                            print Fore.RED + away_team_name + ': ' + away_team_score + Fore.RESET 
                            print Fore.GREEN + home_team_name + ': ' + home_team_score + Fore.RESET
                        
                        else:
                            print Fore.YELLOW + away_team_name + ': ' + away_team_score + Fore.RESET 
                            print Fore.YELLOW + home_team_name + ': ' + home_team_score + Fore.RESET                               
                        
                        print ''
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
