#!/bin/bash
set -e

[ ! -d /root/.vnc ] && mkdir  /root/.vnc
[ -f /tmp/.X99-lock ] && rm -f /tmp/.X99-lock
[ -f /tmp/.X0-lock ] && rm -f /tmp/.X0-lock

_kill_procs() {
  kill -TERM $xvfb
}

trap _kill_procs SIGTERM SIGINT

Xvfb :0 -screen 0 1920x1080x16 &
xvfb=$!
echo "Xvfb started on display 1920x1080x16 :0"
export DISPLAY=:0
sleep 5

cd /app

x11vnc -storepasswd 12345678 /root/.vnc/passwd
x11vnc -display $DISPLAY -bg -forever -usepw -quiet -rfbport 5901 -xkb
echo "x11vnc started on port 5901"

# uvicorn main:app --host 0.0.0.0 --port 8000 &
fastapi dev main.py &
echo "FastAPI started on port 8000"

/usr/sbin/nginx
echo "Nginx started port 3000"

if [ ! -z "$xvfb" ]
then
  wait $xvfb
fi