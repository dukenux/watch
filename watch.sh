#!/bin/bash
cd /home/olimex/scripts
/opt/mjpg-streamer/mjpg_streamer -i "/opt/mjpg-streamer/input_uvc.so -d /dev/video0 -r 1280x720 -f 10" -o "/opt/mjpg-streamer/output_http.so -p 8082" & 
sleep 10
/usr/bin/motion -c /etc/motion/motion.conf &

