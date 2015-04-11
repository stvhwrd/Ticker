# Author: John Freed
# Python Version 2.7

# You must enter the team name exactly as it appears
# on http://www.nhl.com/ice/scores.htm

import json
import os
import platform
import sys
import time
import requests

refresh_time = 60  # Refresh time (Seconds)
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}


def main():
    clear_screen()
    print_ascii_art()
    time.sleep(3)

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
                    tsc = game_info['tsc']

                    away_team_name = game_info['atn']
                    atv = game_info['atv']
                    away_team_score = game_info['ats']

                    home_team_name = game_info['htn']
                    htv = game_info['htv']
                    home_team_score = game_info['hts']

                    # Only show games that have occurred or are in progress
                    if away_team_score != '' and home_team_score != '':
                        header_text = away_team_name + ' @ ' + home_team_name
                        
                        # Check if the game is over and has a final score
                        if tsc != '':
                            header_text += ' (Final)'

                        print header_text
                        print away_team_name + ': ' + away_team_score
                        print home_team_name + ': ' + home_team_score
                        print ''

        # Perform the sleep
        time.sleep(refresh_time)


def print_header():
    print '======================'
    print '= Current NHL Scores ='
    print '======================'


def print_ascii_art():
    # Thanks Cheshirecat from http://www.retrojunkie.com/asciiart/sports/hockey.htm !
    print "                        .---."
    print "                       /_____\\"
    print "                      _HH.H.HH"
    print "       _          _-\"\" WHHHHHW\"\"--__"
    print "       \\\\      _-\"   __\\VW=WV/__   /\"\"."
    print "        \\\\  _-\" \\__--\"  \"-_-\"   \"\"\"    \"_"
    print "         \\\\/ PhH  _                      \"\""
    print "          \\\\----_/_|     ___      /\"\\  T\"\"\\====-"
    print "           \\\\ /\"-._     |%|H|    (   \"\\|) | /  .:)"
    print "            \\/     /    |-+-|     \\    |_ J .:::-'"
    print "            /     /     |H|%|  _-' '-._  \" )/;\""
    print "           /     / \\    __    (  \\ \\   \\   \""
    print "          /     /\\/ '. /  \\   \\ \\ \\ _- \\"
    print "          \"'-._/  \\/  \\    \"-_ \\ -\"\" _- \\"
    print "         _,'\\\\  \\  \\/  )      \"-, -\"\"    \\"
    print "      _,'_- _ \\\\ \\  \\,'          \\ \\_\\_\\  \\"
    print "    ,'    _-    \\_\\  \\            \\ \\_\\_\\  \\"
    print "    \\_ _-   _- _,' \\  \\            \\ \"\"\"\"   )"
    print "     C\\_ _- _,'     \\  \"--------.   L_\"\"\"\"_/"
    print "      \" \\/-'         \"-_________|     '\"-Y"
    print ""
    print "             NHL Scores by John Freed"


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':
    main()