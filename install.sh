#! /bin/sh

set -e

echo "Installing yj_newspusher_signal\n"
sudo cp yj_newspusher_signal.py /usr/local/bin/
sudo chmod a+x /usr/local/bin/ yj_newspusher_signal.py
sudo cp  yj_newspusher_signal_wrapper.sh /usr/local/bin/
sudo chmod a+x /usr/local/bin/ yj_newspusher_signal_wrapper.sh


echo "installing init.d script\n"
sudo cp yj_newspusher_signal_init.sh /etc/init.d/
sudo chmod a+x /etc/init.d/yj_newspusher_signal_init.sh

echho "starting newspusher in a separate screen\n"
sudo update-rc.d yj_newspusher_signal_init.sh defaults
sudo /etc/init.d/yj_newspusher_signal_init.sh start

echo "all done\n"
