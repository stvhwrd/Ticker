'''This module generates a list of game URLs for accessing the
NHL.com scoreboard.'''

import datetime
# used for getting today's date and generating other dates from that.


SEASON = '20142015'


def make_list():
    '''Return a list of game urls for next 16 days (starting yesterday).'''

    daily_urls = {}

    day_zero = datetime.datetime.now()
    today = format_time(day_zero)
    daily_urls[0] = generate_link(today)

    yesterday = day_zero - datetime.timedelta(days=1)
    yesterday = format_time(yesterday)
    daily_urls[-1] = generate_link(yesterday)

    for index in range(1, 15):
        current_day = day_zero + datetime.timedelta(days=index)
        next_day = format_time(current_day)
        daily_urls[index] = generate_link(next_day)

    return daily_urls


def generate_link(date):
    '''Return an NHL.com url for the given date'''
    return 'http://www.nhl.com/ice/scores.htm?date=' + str(date) \
        + '&season=' + SEASON


def format_time(date):
    '''Return a string formatted as month/day/year for given date'''
    return "%02d/%02d/%d" % (date.month, date.day, date.year)
