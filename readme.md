# raspberrypi doorcam 
  componenets:
  doorcam = raspberry pi 4 with external USB formated with FAT to store images
  WD cloud drive mounted to rasoberry pi 4 doorcam
  PI camera module
  PI camera cable
  raspberrypi touch = Touch screen with inbuilt raspberry pi 3 model 

# code running at rasberry pi with doorcam 
  pic.sh - Triggers a still pic in jpg format and also triggers transfernewpic.sh, runs with service called doorcam.service
  transfernewpic.sh - Transfers pics to raspitouch
  compress.py - compress the files to zip and transfers the file to WD cloud, runs with a cronjob
  It will avoid un-necessary pile up of the jpg files on the mounted USB

# USB post its formated with FAT, mount the USB on raspberry pi 4 aka doorcam
  fdidk -l 
  Disk /dev/sda: 115.7 GiB, 124218507264 bytes, 242614272 sectors
  Disk model: Ultra Fit
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x00000000
  root@raspberrypi:/home/pi/doorcam# blkid /dev/sda
  /dev/sda: UUID="5E78-8B4F" TYPE="vfat"
  Post you have plugged in USB, fdisk -l will give the /dev is and 
  
  mount the USB device to the local directory  
  sudo mount /dev/sda /media/usb -o uid=pi,gid=pi


# WD cloud configuration
  WD cloud dont support a linux backup from GUI, but we can mount the NFS to the doorcam aka raspberry pi and use for backup
  Connect the WD to router and get the local static IP
  showmount -e <local stativ IP>
  sudo mkdir /home/pi/wdcloudnfsshare/
  sudo mount -o rw,hard,intr,nfsvers=3 192.168.1.6:/nfs /home/pi/wdcloudnfsshare/


# Persist in fstab to re-mount on reboot at raspberry pi
  cat /etc/fstab
  To auto-mount USB place this code in /etc/fstab
  UUID=5E78-8B4F /media/usb vfat auto,nofail,noatime,users,rw,uid=pi,gid=pi 0 0
  To auto-mount the WD cloud place this code in /etc/fstab
  192.168.1.6:/nfs /home/pi/wdcloudnfsshare nfs rw,hard,intr,rsize=8192,wsize=8192,timeo=14 00

