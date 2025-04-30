#!/bin/bash
set -e


/usr/bin/websockify --web=/usr/share/novnc 6080 localhost:5900 &
novnc=$!

/usr/sbin/nginx -c /etc/nginx/nginx.conf


[ -f /tmp/.X99-lock ] && rm -f /tmp/.X99-lock

_kill_procs() {
  kill -TERM $node
  kill -TERM $xvfb
}

trap _kill_procs SIGTERM SIGINT


if [ -z "$DISPLAY" ]
then
  Xvfb :99 -screen 0 1024x768x16 -nolisten tcp -nolisten unix &
  xvfb=$!
  export DISPLAY=:99
fi


python app/main.py "$@" &
node=$!

wait $node

if [ ! -z "$xvfb" ]
then
  wait $xvfb
fi