# NHL Scores

[![Join the chat at https://gitter.im/jtf323/NHL-Scores](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jtf323/NHL-Scores?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A quick little python script I wrote for getting current NHL scores.

```
                                        .-.-.
                                       /_____\
                                      :._|_|_.:
                                      |/a> a>\|
                                   _.-:  (    ;._
                                 ,'::::\  _  /:::`-._
                                /:::::::`._,'|:::::::`._
                               /:::::_.--`._,'-.::::::::`.
                              :`:::;' \  )SSt(   `':_:;-' \
                              |: `'   : \         \ .   ,-.\
                              |'  --._;.           `:\,' .._\
                              |:.   -.\:          `;:;'.'    :
                              :,----..(:._ ._,---.';'.  `.__.'
                              /\,---.|:':..-(\,-,   `.`..-'
                             /  :.--.'|:'   ;',:.__.-''
                            :   |     |'  ,',' /:/ /
                            :   |,'|.-| ,','  /:/ /
                           /:\  : ,'_,:','   /:/ /
                          /  `:._\,'.`.`, -.';','
                         :`-._`:/ >._>.'   .;\'
                         |`-._`:,',/_     ,'
                         |::::;',' ; `-'':
                         /\:,',|  :`-..-.;
                       _,`,',' ;  ;:::::/
                     ,'`,','.;':_;`-::'/
                    <`,',;::;:-'      /
                    ,','   (  ````  ,'.::::.
                  ,'.'     /`_.__.-'::::'
               _,','         `:::::::'
    _______..-`.,'
  ,' ,----.   ,'
 '---`----'-''
 ```


# Usage

In the `NHL-Scores.py` file you can set up multiple games with the `games` variable.

Example: `games = [['New Jersey', 'Tampa Bay'], ['NY Rangers', 'Ottawa'], ['Minnesota', 'Nashville']]`

The team names must match the team names displayed  on [http://www.nhl.com/ice/scores.htm](http://www.nhl.com/ice/scores.htm)

# Requirements

* Requests
    * `pip install requests`
