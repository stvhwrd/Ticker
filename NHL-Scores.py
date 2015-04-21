# All credit to @jtf323 for the original script which I have changed.

import json
import os
import platform
import sys
import time
import datetime
import requests
from colorama import init, Fore, Back, Style

refresh_time = 60  # Refresh time (Seconds)
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
                    gameClock = game_info['ts']
                    status = game_info['bs']

                    away_team_name = game_info['atn']
                    away_team_score = game_info['ats']

                    home_team_name = game_info['htn']
                    home_team_score = game_info['hts']

                    # Only show games that are scheduled for today or still in progress
                    if gameClock.lower() == today.lower() or status == 'LIVE':
                        header_text = away_team_name + ' @ ' + home_team_name
                        
                        # Check if the game is over, hasn't started yet, or is still in progress
                        if 'FINAL' in status:
                            header_text += ' (' + status + ')'    # example (FINAL OT)                        
                        elif 'DAY' in gameClock:
                            header_text += ' (' + gameClock + ', ' + status + ' EST)'
                        else:
                            header_text += ' (' + gameClock + ' period)'     # example output: (10:34 3rd period)

                        print header_text

                        #highlight the winner green, loser red
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
