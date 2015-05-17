# NHL Scoreline

A simple Python script to display the score of current and recently finished NHL games.  When no games have been played in the last two days, the upcoming schedule will be displayed instead.

![Finished games (example)](https://github.com/stvhwrd/NHL-Scoreline/blob/master/Screenshots/CompletedGames.png)

## Requirements
* Python 2.7
    * `python --version`
* Requests
    * `pip install requests`
* Colorama
    * `pip install colorama`

## Usage

Once you've ensured that your system meets the requirements, open a terminal window and execute

`python /your/path/to/NHL-Scoreline.py`

To see games for today **only**, you can run the sript with the `--today-only` flag

`python /your/path/to/NHL-Scoreline.py --today-only`


<br>
<br>

## Tested on

* OS X 10.10.3 with Python 2.7.9
* Windows 7 x64 with Python 2.7.9
* Ubuntu 14.04 x64 with Python 2.7.6

## License

[GNU GENERAL PUBLIC LICENSE](http://choosealicense.com/licenses/gpl-3.0/#)     -- Version 3, 29 June 2007
