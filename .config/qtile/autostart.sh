#!/bin/sh
xrandr --output eDP-1 --mode 1920x1080 --output HDMI-1-0 --mode 1920x1080 --right-of eDP-1 &
nitrogen --restore &
picom --experimental-backends --backend glx --xrender-sync-fence &

