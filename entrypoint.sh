#!/bin/bash
set -e

[ ! -d /root/.vnc ] && mkdir  /root/.vnc
[ -f /tmp/.X99-lock ] && rm -f /tmp/.X99-lock
[ -f /tmp/.X0-lock ] && rm -f /tmp/.X0-lock

_kill_procs() {
  kill -TERM $xvfb
}

trap _kill_procs SIGTERM SIGINT

Xvfb :0 -screen 0 1024x768x16 &
xvfb=$!

echo "Xvfb started on display 1024x768x16 :0"
export DISPLAY=:0
sleep 3

cd /app
echo "Starting VNC server"
x11vnc -storepasswd 12345678 /root/.vnc/passwd
x11vnc -display $DISPLAY -bg -forever -usepw -quiet -rfbport 5901 -xkb
# echo "x11vnc started on port 5901"

# uvicorn main:app --host 0.0.0.0 --port 8000 &
fastapi dev main.py --host 0.0.0.0 --port 9000 &
# echo "FastAPI started on port 8000"

echo "Nginx started port 3000"

dumb-init python start.py

nginx -g 'daemon off;'