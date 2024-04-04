#!/bin/bash

start() {
   cd /opt/beslighthouse-rest-api

   pip install -r requirements.txt

   flask run &
}

stop() {
    pid=`ps ax | grep "flask run" | awk '{print $1}'`
    kill -9 $pid
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
