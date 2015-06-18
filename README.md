# Ticker

[![Join the chat at https://gitter.im/stvhwrd/Ticker](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/stvhwrd/Ticker?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

<br>

A web scraper built with Python to display the score of current and recently finished NHL games.  The score is scraped directly from the NHL website every 30 seconds.  During intermissions (between periods), a countdown clock is displayed.

![Exhibit A](https://raw.githubusercontent.com/stvhwrd/Ticker/blob/master/Screenshots/IntermissionClock.png)

## Requirements

* Python 2.7
    * `python --version`
* Requests
    * `pip install requests`
* Colorama
    * `pip install colorama`

## Usage
Once you've ensured that your system meets the requirements, open a terminal window and execute
`python /your/path/to/ticker.py`
<br>
<br>

## Tested on

* OS X 10.10.3 with Python 2.7.9
* Windows 8.1 x64 with Python 2.7.9
* Ubuntu 14.04.2 LTS x64 with Python 2.7.6

## Goal
I hope to extend this ticker-type functionality to other sports leagues.  I plan to make the main script generic and then pull in header files for whichever specific league the user chooses at runtime.  Next league I'll implement will probably be MLB since their 162 games * 30 teams allows for a lot of live testing!

## License

[MIT License](http://opensource.org/licenses/MIT)
