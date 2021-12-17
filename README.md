# signal-cli-newschannel
A python script that watches a websites RSS feed and sends it to all signal accounts that subscribed it.
This could be understood as a signal (news) channel. 
The subscribers are expected to be stored in a SQLite database file. Therefore this project is linked to [signal-cli-bot](https://github.com/yjeanrenaud/signal-cli-bot) and depends on [signal-cli](https://github.com/AsamK/signal-cli).

## Installation
0. Have set up and configured [signal-cli](https://github.com/AsamK/signal-cli) as a dbus service. See the [wiki overthere](https://github.com/AsamK/signal-cli/wiki) for more information
1. Install dependencies
`sudo apt-get install python3 pythjon3-pip`
`sudo pip3 install requests feedparser pprint pydbus sqlite3`
2. Customize [yj_newspusher_signal.py](yj_newspusher_signal.py) to match your needs

## Todos and Future Plans
* work with an encrypted SQlite and other db drivers
* clean the code, oop n stuff
* parameterisation of the feed and the subscribers file
