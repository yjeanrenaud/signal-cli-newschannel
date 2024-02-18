# signal-cli-newschannel
A python script that watches a websites RSS feed and sends it to all signal accounts that subscribed it.
This could be understood as a signal (news) channel.
It now also includes the posts first image as an attachment in the signal message.

The subscribers are expected to be stored in a SQLite database file. Therefore this project is linked to [signal-cli-bot](https://github.com/yjeanrenaud/signal-cli-bot) and depends on [signal-cli](https://github.com/AsamK/signal-cli).

## Installation and Usage
0. Have set up and configured [signal-cli](https://github.com/AsamK/signal-cli) as a dbus service. See the [wiki overthere](https://github.com/AsamK/signal-cli/wiki) for more information
1. Install dependencies
`sudo apt-get install python3 pythjon3-pip`
`sudo pip3 install requests feedparser pprint pydbus sqlite3`
2. Customize [yj_newspusher_signal.py](yj_newspusher_signal.py) to match your needs
3. Run the script, e.g. in a `screen` session: `screen -dmS signal-news python3 yj_newspusher_signal.py`

## Todos and Future Plans
* Work with an encrypted SQlite and other db drivers
* Clean the code, oop n stuff
* Parameterisation of the feed and the subscribers file
