# Author: John Freed
# Python Version 2.7

import urllib2
import time
import os
from bs4 import BeautifulSoup

refresh_time = 10  # Refresh time (Seconds)
score_url = 'http://www.nhl.com/ice/scores.htm'
teams = ['Ottawa', 'NY Rangers']

def main():
    while True:
        clear_screen()
        print_header()

        page = urllib2.urlopen(score_url)
        page_html = page.read()
        
        soup = BeautifulSoup(page_html)
        
        for team in teams:
            team_list = soup.find('a', text = team)

            try:
                for td in team_list.parent.find_next_siblings('td', class_ = 'total'):
                    current_score = td.text
                    print team + ': ' + current_score
            except:
                print 'Error occured'

        time.sleep(refresh_time)


def print_header():
    print '======================'
    print '= Current NHL Scores ='
    print '======================'


def clear_screen():
    os.system('cls')  # This is windows specific, needs to be changed

if __name__ == '__main__':
    main()