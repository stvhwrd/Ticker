# NHL Scores

[![Join the chat at https://gitter.im/stvhwrd/NHL-Scores](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jtf323/NHL-Scores?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python script written by [@jtf323](https://www.github.com/jtf323), tailored and tweaked to suit my needs.  I wanted the output display to be very simple so as to be useful in programs like [Conky](http://conky.sourceforge.net/) and [GeekTool](http://projects.tynsoe.org/en/geektool/).  

The winners of completed games are displayed in green and the losers in red, while games in progress have both teams highlighted in yellow.  

![Example of finished games](https://github.com/stvhwrd/NHL-Scores/blob/master/completeGames.png)

## Requirements
* Python 2.7
* Requests
    * `pip install requests`

## Usage

To launch the script, ensure your system meets the requirements, open a terminal window and run

`python /path/NHL-Scores.py`
                                        
example:
                                        
`python ~/GitHub/NHL-Scores/NHL-Scores.py`

<br>
<br>

######tested with Python 2.7.9 on Apple MacBook Pro (Late 2011) running OS X 10.10.3
