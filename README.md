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

## Tested on
* Apple MacBook Pro (Late 2011) running OS X 10.10.3 with Python 2.7.9
* Windows 7 x64 with Python 2.7.9
* Ubuntu 14.04 x32 with Python 2.7.6

## License
The MIT License (MIT)

Copyright (c) 2015 John Freed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.