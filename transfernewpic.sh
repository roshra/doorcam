#!/bin/bash
now=$(ls -ltrh /media/usb | cut -d " " -f 10 | tail -1)
scp /media/usb/$now pi@192.168.1.28:/media/recentimage
