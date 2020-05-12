#!/usr/bin/python3
import fnmatch
import glob, os
from datetime import date
import zipfile
import shutil
import subprocess
import time
import sys
import logging
logging.basicConfig(filename="journal.log",format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',level=logging.DEBUG)
path = "/media/usb/"
archive_path = "/home/pi/wdcloudnfsshare/Public/doorcam/"
today = date.today()
os.chdir("/media/usb")
date = today.strftime("%Y-%m-%d")
search_param=date+"*.jpg"
file_list=[]
cmd_doorcamstop = "sudo systemctl stop doorcam.service"
cmd_doorcamstart = "sudo systemctl start doorcam.service"
cmd_zip_delete = "sudo rm -f *.zip"
cmd_delete_jpg = "sudo rm -f *.jpg"
subprocess.call(cmd_doorcamstop, shell=True)

for file_name in os.listdir('.'):
    if fnmatch.fnmatch(file_name,search_param):
        file_list.extend([file_name])

try:
    date_with_sec = time.strftime("%y-%m-%d-%H-%M-%S")
    zip_name=date_with_sec+".zip"
    print(zip_name)
    with zipfile.ZipFile(zip_name, mode = 'w', allowZip64 = True) as zip_my_files:
        for name in file_list:
            zip_my_files.write(name)
        zip_my_files.close()
except IOError:
    print("zip failed")
    subprocess.call(cmd_doorcamstart, shell=True)
    logging.debug("Initial zip has failed for date")
    sys.exit("starting doorcam service and exiting program as initial zip has failed")
else:
    try:
        print("zip is successful")
        logging.debug("zip successful dated:{} filename:{}".format(date_with_sec,zip_name))
        pigz_zip_name = archive_path + zip_name + ".tar.gz"
        subprocess.call('tar cf - ' + zip_name + '|' + 'pigz -9 -p 32 >' +  pigz_zip_name, shell=True) 
    except IOError:
        print("pigz failed to move archive to cloud")
        logging.debug("pigz failed to move dated:{} filename:{} to WD cloud".format(date_with_sec,pigz_zip_name))

        subprocess.call(cmd_doorcamstart, shell=True)
        sys.exit("Starting doorcam service and exiting program because we dont want to delete unarchived jpg files now")
        logging.debug("retaining the jpg dates:{} and starting doorcam service".format(date_with_sec))
    else:
        print("successfully archived files to WD cloud for date {}".format(date_with_sec))
        logging.debug("archived filename:{} to WD cloud".format(pigz_zip_name))
        try:
            subprocess.call(cmd_delete_jpg, shell=True)
            subprocess.call(cmd_zip_delete, shell=True)
            subprocess.call(cmd_doorcamstart, shell=True)
        except IOError:
            print("delete old jpg, delete old zip, starting doorcam service failed")
            logging.debug("Its exception, we are retaining old jpg dated:{} and starting doorcam service".format(date_with_sync))
        else:
            print("successfully completed program - archive done to cloud")
            logging.debug("successfully pushed filename:{} to WD cloud".format(pigz_zip_name))
