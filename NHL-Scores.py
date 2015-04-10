# Author: John Freed
# Python Version 2.7

import urllib2
import time
from bs4 import BeautifulSoup

refresh_time = 10  # Refresh time (Seconds)
score_url = 'http://www.nhl.com/ice/scores.htm'

def main():
    while True:
        print 'Getting page...'
        page = urllib2.urlopen(score_url)
        page_html = page.read()
        print page_html

        time.sleep(refresh_time)


if __name__ == '__main__':
    main()