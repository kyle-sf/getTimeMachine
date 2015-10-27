#!/usr/bin/env python

import subprocess
import time
import os
from time import strftime, localtime

######################
# USER SET VARIABLES #
######################

# SSID of network where Network Drive is located
HOME_SSID = "TellMyWiFiLoveHer"

# Path to the mount for the network drive
MOUNT_PATH = "/Volumes/piMount"

# Path to the network drive's mountable partition/section/dir
# Replace user and pass with credentials, IP address of network device and the mountable section name
NETWORK_PATH = "//user:pass@192.168.0.2/Backup"

# Path where you wish to mount your Time Machine Sparesbundle image
TM_MOUNT_PATH = "/Volumes/TimeMachine"

# Path to the Time Machine Sparesebundle image relative to your Network Drive Mount
TM_NETWORK_PATH = "/Volumes/piMount/TimeMachine.sparsebundle"

# Path to airport tool (Below is default as of Mac OS X 10.11)
AIRPORT_MOUNT = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

# Time delay between checks (in seconds)
WAIT_TIME = 600

########################################
# Begin monitoring and mounting script #
########################################

while True:
    print strftime("%a, %d %b %H:%M", localtime())
    if os.path.ismount("/Volumes/piMount") and os.path.ismount("/Volumes/KyleBackup"):
        print "Your pi is mounted!"
    elif os.path.ismount("/Volumes/piMount") and (os.path.ismount("/Volumes/KyleBackup")==False):
        print "Your pi is mounted, but your Time Machine is not, attempting to mount now..."
        subprocess.call(["hdiutil", "attach", "-quiet", "-nobrowse", "-mountpoint", "/Volumes/KyleBackup", "/Volumes/piMount/KyleBackup.sparsebundle"])
    else:
        SSID = ""
        #Use the airport cmd tool to get WiFi details (-I to list all)
        proc = subprocess.Popen([AIRPORT_MOUNT, "-I"], stdout=subprocess.PIPE)

        #Read in the details and get the SSID
        output = proc.stdout.read()
        for line in output.split('\n'):
            if line != "":
                #Look for "SSID" and make sure it isn't blank
                if line.split()[0] == "SSID:" and line != "           SSID: ":
                    SSID = line.split()[1]

        #Check this matches the home SSID, if so mount the smb share and TimeMachine
        if SSID == HOME_SSID:
            #Ensure there is a MOUNT_PATH dir
            subprocess.call(["mkdir", MOUNT_PATH])
            #Mount the Network Drive
            subprocess.call(["mount_smbfs", NETWORK_PATH, MOUNT_PATH])
            #Mount the TimeMachine image
            subprocess.call(["hdiutil", "attach", "-quiet", "-nobrowse", "-mountpoint", TM_MOUNT_PATH, TM_NETWORK_PATH])
            print "Mounted the Network Device"
        else:
            #Not the right SSID, try again later
            print "SSID is:", SSID, "Will try again"
    time.sleep(WAIT_TIME)
