# -*- coding: utf-8 -*-
# Author: John Freed - @jtf323

from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests

scoreboard_url = 'http://www.nhl.com/ice/scores.htm'
refresh_time = 60  # Refresh time (seconds), as per NHL API
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

show_today_only = False

def main():

    intermission_clock = 18
    
    games_today = False

    clear_screen()

    # Format dates to match NHL API style:

    # Current season
    season = '20142015/'

    # Today's date
    t = datetime.datetime.now()
    todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
    
    # Yesterday's date
    y = t - datetime.timedelta(days=1)
    yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)

    # Next two weeks
    next_two_weeks = []
    for index in range(1, 15):
        d = t + datetime.timedelta(days=index)
        next_day = "" + d.strftime("%A") + " " + "%s/%s" % (d.month, d.day)
        next_two_weeks.append(next_day)


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
        # import pdb; pdb.set_trace()
        for key in data:
            if key == 'games':
                for game_info in data[key]:

                    # Assign more meaningful names
                    game_id = str(game_info['id'])
                    game_clock = game_info['ts']
                    game_stage = game_info['tsc']
                    status = game_info['bs']

                    away_team_locale = game_info['atn']
                    away_team_name = game_info['atv'].title()
                    away_team_score = game_info['ats']
                    away_team_result = game_info['atc']

                    home_team_locale = game_info['htn']
                    home_team_name = game_info['htv'].title()
                    home_team_score = game_info['hts']
                    home_team_result = game_info['htc']

                    # Fix strange names / locales returned by NHL
                    away_team_locale = fix_locale(away_team_locale)
                    home_team_locale = fix_locale(home_team_locale)
                    away_team_name = fix_name(away_team_name)
                    home_team_name = fix_name(home_team_name)

                    series_game_number = game_id[-1:]
                    season_stage = game_id[4:6]

                    # Show games from (yesterday and today) or just today
                    if (yesterdays_date in game_clock.title() and not show_today_only) or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:
                        games_today = True
                        header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        
                        # Show the game number of current 7-game series if it's playoff time
                        if game_id[4:6] == '03':
                            header_text += ' -- Game ' + series_game_number
                        
                        # Different displays for different states of game:
                        # Game from yesterday, ex: on YESTERDAY, MONDAY 4/20 (FINAL 2nd OT)
                        # Game from today finished, ex: TODAY (FINAL 2nd OT)
                        if 'FINAL' in status:
                            if yesterdays_date in game_clock.title():
                                header_text += '\nYESTERDAY '
                            elif todays_date in game_clock.title() or 'TODAY' in game_clock:
                                header_text += '\nTODAY '
                            header_text += '(' + status + ')'

                        # Upcoming game, ex: TUESDAY 4/21, 7:00 PM EST)
                        elif 'DAY' in game_clock:
                            header_text += Fore.YELLOW + '\n(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET

                        # Last 5 minutes of game and overtime, ex: (1:59 3rd PERIOD) *in red font*
                        elif 'critical' in game_stage:
                            header_text += Fore.RED + '\n(' + game_clock + ' PERIOD)' + Fore.RESET

                        

                        # Any other time in game, ex: (10:34 1st PERIOD)
                        else:
                            header_text += Fore.YELLOW + '\n(' + game_clock + Style.RESET_ALL
                            if 'PRE GAME' not in game_clock:
                                header_text += Fore.YELLOW + ' PERIOD'

                            # Display a countdown for 18 minutes of intermission (regular periods)
                            #     or 15 minutes of intermission (OVERTIME)
                            if 'END ' in game_clock and 'final' not in status:
                                header_text += Fore.YELLOW + ', ' + str(intermission_clock) + ' minutes remaining in the intermission'
                                intermission_clock -= 1
                                if intermission_clock < 0:
                                    if 'END 3rd' in game_clock or 'OT' in game_clock:
                                        intermission_clock = 15
                                    else:
                                        intermission_clock = 18

                            header_text += Fore.YELLOW + ')' + Style.RESET_ALL

                        print header_text


                        # Highlight the winner of finished games in blue, and games underway in green:
                        # Away team wins
                        if away_team_result == 'winner':
                            print Style.BRIGHT + Fore.BLUE + away_team_name + ': ' + away_team_score + Style.RESET_ALL
                            print home_team_name + ': ' + home_team_score

                        # Home team wins
                        elif home_team_result == 'winner':
                            print away_team_name + ': ' + away_team_score
                            print Style.BRIGHT + Fore.BLUE + home_team_name + ': ' + home_team_score + Style.RESET_ALL

                        # Game still underway
                        elif 'progress' in game_stage or 'critical' in game_stage:
                            print Fore.GREEN + away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score + Fore.RESET
                        
                        # elif todays_date not in game_clock.title() and yesterdays_date not in game_clock.title():
                        #     if show_today_only:
                        #          print '\nThere are no games today.'
                        #      else:
                        #         '\nThere are no games today.\nNext games:\n'
                        #         for day in next_two_weeks:
                        #             print away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        #             print Fore.YELLOW + '(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET
                        #             print away_team_name + ': ' + away_team_score
                        #             print home_team_name + ': ' + home_team_score

                        # Game hasn't yet started
                        else:
                            print away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score

                        print ''
                    elif games_today == False:
                        if show_today_only:
                            print '\nThere are no games today.'
                        else:
                            header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        # Show the game number of current 7-game series if it's playoff time
                            if game_id[4:6] == '03':
                                header_text += ' -- Game ' + series_game_number
                            print header_text
                            print Fore.YELLOW + '(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET
                            print away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score
                            print ""
                            
                        
                    
                    
    
                    # 
                    #       print   print "\nThere are no games today or tomorrow.\nNext games:\n"
                    #     if any day in game_clock.title() and not show_today_only:
                    #     # for day in next_two_weeks:
                    #         print away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                    #         print Fore.YELLOW + '(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET
                    #         print away_team_name + ': ' + away_team_score
                    #         print home_team_name + ': ' + home_team_score


        # Perform the sleep
        time.sleep(refresh_time)


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def print_help():
    print 'By default games from yesterday and today will be displayed.'
    print ''
    print 'If you want to see games from just today run the program with '
    print 'the "--today-only" flag.'


def get_address(game_id, season):
    prefix = 'http://live.nhle.com/GameData/'
    suffix = '/gc/gcsb.jsonp'
    game_url = prefix + season + str(game_id) + suffix

    return game_url


def fix_locale(team_locale):
    # NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
    if 'NY ' in team_locale:
        return 'New York'
    # 
    if 'Montr' in team_locale:
        return u'Montréal'
        
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


def print_schedule():
    for day in next_two_weeks:
        print away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
        print Fore.YELLOW + '(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET
        print away_team_name + ': ' + away_team_score
        print home_team_name + ': ' + home_team_score
        print "\n"

# def get_series_score(scoreboard_url):
# see http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/
#
# def get_category_winner(category_url):
#     html = urlopen(scoreboard_url).read()
#     soup = BeautifulSoup(html, "lxml")
#     category = soup.find("h1", "headline").string
#     winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
#     runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
#     return {"category": category,
#             "category_url": category_url,
#             "winner": winner,
#             "runners_up": runners_up}

def parse_arguments(arguments):
    global show_today_only
    for x in range(1, len(arguments)):
        argument = arguments[x]

        if argument == '--help' or argument == '-h':
            print_help()
            sys.exit(0)
        elif argument == '--today-only':
            show_today_only = True


if __name__ == '__main__':
    # Initialize Colorama
    init()

    # Parse any arguments provided
    parse_arguments(sys.argv)

    # Start the main loop
    main()
