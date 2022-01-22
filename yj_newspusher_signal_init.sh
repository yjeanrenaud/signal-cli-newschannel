#! /bin/sh

### BEGIN INIT INFO
# Provides:          signal-cli-newschannel
# Required-Start:    $network
# Required-Stop:     $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting yj newspusher bot in screen"
    /usr/bin/screen -dmS signal /usr/local/bin/yj_newspusher_signal_wrapper.sh &
    ;;
  stop)
    echo "Stopping yj newspusher bot"
    pkill -f /usr/local/bin/yj_newspusher_signal_wrapper.sh
    ;;
  *)
    echo "Usage: /etc/init.d/yj_newspusher_signal_init.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
