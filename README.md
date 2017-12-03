# Ticker [![Build Status](https://travis-ci.org/stvhwrd/Ticker.svg?branch=master)](https://travis-ci.org/stvhwrd/Ticker)


A Python web scraper built to display the score of current and recently finished NHL games.  The score is scraped directly from the NHL website every 30 seconds.

<img src="https://github.com/stvhwrd/Ticker/blob/master/Screenshots/screenshot.png?raw=true" width="360">


## Requirements

* [Python 3.6<sup>+</sup>](https://www.python.org/downloads/release/python-3)
    * `python3 --version`

> <sup>(It actually works just as well with Python 2, you'd just need to remove the `3` from all the commands provided in (a) this README and (b) `requirements.txt`)</sup>

Additional requirements can be installed with [pip](https://pip.pypa.io/en/stable/) - there is a `requirements.txt` file provided that allows you to simply run `pip3 install -r requirements.txt`.  Included in this file are the following packages:

* [Requests](https://pypi.python.org/pypi/requests)
    * `pip3 install requests`
* [Colorama](https://pypi.python.org/pypi/colorama)
    * `pip3 install colorama`
* [Pytz](https://pypi.python.org/pypi/pytz)
    * `pip3 install pytz`

## Usage

Once you've ensured that your system meets the requirements, open a terminal window and execute

`python3 your/path/to/ticker.py`


## Data Source

* NHL livescore JSON:
   * http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp (old one)
   * https://statsapi.web.nhl.com/api/v1/schedule (much richer "new" one, will move to this in future)

In future, I plan to support other leagues, likely startin with MLB:
* MLB livescore JSON:
   * http://gd2.mlb.com/components/game/mlb/year_2015/month_08/day_02/master_scoreboard.json
   
## License

Copyright 2016 [John Freed](https://github.com/jtf323) and [Stevie Howard](https://github.com/stvhwrd).

[MIT License](http://opensource.org/licenses/MIT)
