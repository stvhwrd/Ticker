[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cafaa3346fe54f58924aa5a9ab6e4eca)](https://app.codacy.com/app/stvhwrd/Ticker?utm_source=github.com&utm_medium=referral&utm_content=stvhwrd/Ticker&utm_campaign=badger) [![Build Status](https://travis-ci.org/stvhwrd/Ticker.svg?branch=master)](https://travis-ci.org/stvhwrd/Ticker)
# Ticker

A Python HTTP/JSON script to display the score of today's NHL hockey games.  When run in persistent mode, information is downloaded directly from the NHL website every 20 seconds.

<img src="https://github.com/stvhwrd/Ticker/blob/master/Screenshots/screenshot.png?raw=true" width="360">


## Requirements

* [Python 3.6<sup>+</sup>](https://www.python.org/downloads/release/python-3)
    * `python3 --version`


Additional requirements can be installed with [pip](https://pip.pypa.io/en/stable/) - there is a `requirements.txt` file provided that allows you to simply run `pip3 install -r requirements.txt`.  Included in this file are the following packages:

* [Requests](https://pypi.python.org/pypi/requests)
    * `pip3 install requests`
* [Colorama](https://pypi.python.org/pypi/colorama)
    * `pip3 install colorama`


## Usage

```
usage: ticker.py [-h] [-p]

optional arguments:
  -h, --help     show this help message and exit
  -p, --persist  live-update scores on persistent scoreboard
```

Once you've installed the requirements (`pip3 install -r requirements.txt`), permit the script to execute:

`chmod u+x ticker.py`

Then run the script:

`ticker.py`

This will run the script once, simply outputting the current scores.

If you wish to run the script persistently and have the scores auto-update every 20 seconds, add the `--persist` flag:

`ticker.py -p`

To **quit**, press `Ctrl + C`

## Data Source

* [NHL livescore JSON](http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp) (There is a [newer API](https://statsapi.web.nhl.com/api/v1/schedule), but I prefer the way this one is laid out for simple scoreboard use)

## License

Copyright 2018 [Stevie Howard](https://github.com/stvhwrd).

[MIT License](http://opensource.org/licenses/MIT)
