#!/bin/bash

start() {
   cd /opt/BeSRestApi/beslighthouse-rest-api
   flask run --host="0.0.0.0" --port="5000" &
}

stop() {
    pid=`ps ax | grep "flask run" | awk '{print $1}'`
    if [ ! -z $pid ];then
      kill -9 $pid
    fi
}

case "$1" in 
    start)
       start
       ;;
    stop)
       stop
       ;;
    restart)
       stop
       start
       ;;
    status)
       # code to check status of app comes here 
       # example: status program_name
       ;;
    *)
       echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0 
