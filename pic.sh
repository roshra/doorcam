#!/bin/bash
while :
do
   DATE=$(date +"%Y-%m-%d_%H-%M-%s") 
   raspistill -rot 270 -o /media/usb/$DATE.jpg
   sleep 5
   /home/pi/transfernewpic.sh
done
