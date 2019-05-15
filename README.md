# Ticker [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef9487b975fc4a048cbf6878b8297fe1)](https://www.codacy.com/app/scaryghosty/Ticker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=scaryghosty/Ticker&amp;utm_campaign=Badge_Grade)

A Python HTTP/JSON script to display the score of today's NHL hockey games.  When run in persistent mode, information is downloaded directly from the NHL website every 20 seconds.

<img src="https://github.com/stvhwrd/Ticker/blob/master/Screenshots/screenshot.png?raw=true" width="360">


## Requirements

* Linux machine (not yet Windows compatible)

* [Python 3.6<sup>+</sup>](https://www.python.org/downloads/release/python-3)
    * `python3 --version`


Additional requirements can be installed with [pip](https://pip.pypa.io/en/stable/) - there is a `requirements.txt` file provided that allows you to simply run `pip3 install -r requirements.txt`.  Included in this file are the following packages:

* [Requests](https://pypi.python.org/pypi/requests)
    * `pip3 install requests`
* [Colorama](https://pypi.python.org/pypi/colorama)
    * `pip3 install colorama`


## Usage

```
usage: python3 ticker.py [-h] [-p]

optional arguments:
  -h, --help     show this help message and exit
  -p, --persist  live-update scores on persistent scoreboard
```

Once you've installed the requirements (`pip3 install -r requirements.txt`), permit the script to execute:

`chmod u+x ticker.py`

Then run the script:

`python3 ticker.py`

This will run the script once, simply outputting the current scores.

If you wish to run the script persistently and have the scores auto-update every 20 seconds, add the `--persist` flag:

`python3 ticker.py -p`

To **quit**, press `Enter`. Alternatively, `Ctrl-C` works as well (but try to avoid this if you can).


**IMPORTANT:** All game times are displayed in PST.

## Data Source

* [NHL livescore JSON](http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp) (There is a [newer API](https://statsapi.web.nhl.com/api/v1/schedule), but I'm too lazy to change this fork over.)

## License

Copyright 2019 [Greg Hennis](https://github.com/scaryghosty), [Stevie Howard](https://github.com/stvhwrd).

[MIT License](http://opensource.org/licenses/MIT)
