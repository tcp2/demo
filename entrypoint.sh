#!/bin/bash

mkdir ~/.vnc
DISPLAY=:0
export DISPLAY=:0
echo $SCREEN_WIDTH
echo $SCREEN_HEIGHT
echo `echo $SCREEN_WIDTH`x`echo $SCREEN_HEIGHT`x16

cd /opt/orbita
Xvfb $DISPLAY -screen 0 `echo $SCREEN_WIDTH`x`echo $SCREEN_HEIGHT`x16 &
sleep 3
# x11vnc -storepasswd 12345678 ~/.vnc/passwd
x11vnc -display $DISPLAY -nopw -bg -forever -usepw -quiet -rfbport 5901 -xkb

# Khởi động noVNC server
cd /opt/novnc
# Khởi động với websockify và cấu hình đường dẫn web
./utils/launch.sh --vnc localhost:5901 --listen 6080 &
cd /opt/orbita

# Khởi động nginx
/usr/sbin/nginx -c /etc/nginx/nginx.conf
python3 app/main.py 
