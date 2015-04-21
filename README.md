# NHL Scores
[![Join the chat at https://gitter.im/jtf323/NHL-Scores](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jtf323/NHL-Scores?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python script to display the score of current and recently finished NHL games so as to be useful in programs like [Conky](http://conky.sourceforge.net/) and [GeekTool](http://projects.tynsoe.org/en/geektool/).  

The winners of completed games are displayed in green and the losers in red, while games in progress have both teams highlighted in yellow.  

![Example of finished games](https://github.com/jtf323/NHL-Scores/blob/master/Screenshots/CompletedGames.png)

## Requirements
* Python 2.7
* Requests
    * `pip install requests`
* Colorama
    * `pip install colorama`

## Usage

To launch the script, ensure your system meets the requirements, open a terminal window and run

`python /path/NHL-Scores.py`
                                        
example:
                                        
`python ~/GitHub/NHL-Scores/NHL-Scores.py`

<br>
<br>

######Tested on
* Apple MacBook Pro (Late 2011) running OS X 10.10.3 with Python 2.7.9
* Windows 7 x64 with Python 2.7.9
* Ubuntu 14.04 x32 with Python 2.7.6
