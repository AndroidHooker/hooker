# -*- coding: utf-8 -*-
#+---------------------------------------------------------------------------+
#|                                                                           |
#|                          Android's Hooker                                 |
#|                                                                           |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Dimitri Kirchner                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.amossys.fr                                         |
#| @contact  : android-hooker@amossys.fr                                     |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports
#+---------------------------------------------------------------------------+
import os
import os.path
import time
import datetime

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common.OSCommand import OSCommand
from hooker_common import Logger
from hooker_xp.device.AndroidDevice import AndroidDevice

class PhysicalDevice(AndroidDevice):
    """
    Manage an Android physical device
    """
    def __init__(self, adbPort, name, mainConfiguration, backupDirectory, analysisType):
        super(PhysicalDevice, self).__init__(adbPort, name, mainConfiguration)
        self.__backupDir = backupDirectory
        self._logger = Logger.getLogger(__name__)
        
        # Check if backup directory contains 2 folders named sdcard and partitions
        self.__checkBackupDirectories()
        self.serialNumber = name
        self.analysisType = analysisType
        self.checkAPKInstrumenter()
        # Put the state directly in started, since there is no FS preparation for real device
        self.state = AndroidDevice.STATE_STARTED
            
    
    def __checkBackupDirectories(self):
        """Checks if backup directories exists on local system, print error otherwise"""
        if os.path.exists(self.__backupDir):
            if len(os.listdir(os.path.join(self.__backupDir, 'sdcard')))==0:
                raise Exception("Backup folder: {0} is empty".format(os.path.join(self.__backupDir, 'sdcard')))
                
            if len(os.listdir(os.path.join(self.__backupDir, 'partitions')))==0:
                raise Exception("Backup folder: {0} is empty".format(os.path.join(self.__backupDir, 'partitions')))
                    
        else:
            raise Exception("Backup folder: {0} is empty".format(self.__backupDir))
                        
        
    def waitToBeClosed(self):
        """Waits for the emulator to be closed by the user."""
        try:
            while (True):
                self._logger.debug("Waiting for the device to finish. Press Ctrl-C when you're done.")
                time.sleep(30)
        except KeyboardInterrupt:
            self._logger.debug("User is done.")

            
    def __pushBackup(self):
        """ Pushes backup folder to sdcard """
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "push",
            os.path.join(self.__backupDir, "partitions"),
            os.path.join(self._hookerDir, "backup")
        ]
        OSCommand.executeCommand(cmd)

        
    def __pushRecoveryScript(self):
        """
        Pushes recovery script to TWRP recovery directory.
        This is done is 2 parts: first create the file on /sdcard/, then copy it to /cache/recovery/, using busybox.
        """
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "touch",
            os.path.join(self._hookerDir, "openrecoveryscript")
        ]
        OSCommand.executeCommand(cmd)
            
        cmd = '{0} -s {1} shell echo "restore /sdcard/hooker/backup/" > {2}'.format(self.mainConfiguration.adbPath,
                                                                                    self.serialNumber,
                                                                                    os.path.join(self._hookerDir, "openrecoveryscript"))
        OSCommand.executeCommand(cmd)
        
        cmd = '{0} -s {1} shell su -c \'busybox cp {2} /cache/recovery/openrecoveryscript\''.format(self.mainConfiguration.adbPath,
                                                                                          self.serialNumber,
                                                                                          os.path.join(self._hookerDir, "openrecoveryscript") )
        ret = OSCommand.executeCommand(cmd)
        if len(ret)!=0:
            raise Exception(ret)
            
        
    def reboot(self):
        """Reboot the device"""
        self._logger.info("Rebooting device listening on port {0}".format(self.serialNumber))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "reboot"
        ]
        self._logger.debug(OSCommand.executeCommand(cmd))

        # Real device can take time to reboot
        time.sleep(15)
        # waits for device to be ready
        self._waitForDeviceToBeReady()
        self.state = AndroidDevice.STATE_STARTING

        
    def __restoreSDCard(self):
        """
        Restores the SDCard contents from backup folder.
        Iterates through sdcard folders and deletes files and folders that are not empty.
        Backup folder which contains sdcard initial folders and files will do the restore.
        """
        self._logger.info("Restoring sdcard...")

        ls = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "ls"
        ]
        rm = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "rm",
            "-r"
        ]
        
        result = OSCommand.executeCommand(ls+['/sdcard/'])
        folders = result.split('\r\n')

        for folder in folders:
            if len(folder)!=0:
                # If folder (or file) is not empty, deletes it
                res = OSCommand.executeCommand(ls+['/sdcard/'+folder])
                if len(res)!=0:
                    self._logger.info("Deleting {0}".format('/sdcard/'+folder))
                    OSCommand.executeCommand(rm+['/sdcard/'+folder])
                
        # Push sdcard backup folder
        push = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "push",
            os.path.join(self.__backupDir, 'sdcard/'),
            '/sdcard/'
        ]
        OSCommand.executeCommand(push)
        self._logger.info("SDcard has been restored.")
        
        
    def stop(self, askUser=False):
        """ Stop the device"""
        self._logger.info("Stopping device listening on port {0}".format(self.serialNumber))
        clean = True
        
        # Pull our analysis events
        self._pullResults()

        # Ask user if they want to clean the device
        if askUser:
            answer = raw_input("Do you want to clean your device? [Yes or No] ").lower()
            while answer!='yes' and answer!='no':
                answer = raw_input("Do you want to clean your device? [Yes or No] ").lower()
            if answer=='no':
                clean=False
        
        if clean:
            # If we have a real device we have to push backup to sdcard and push TWRP script to /cache/recovery/
            # at each experiment
            self.__pushBackup()
            self.__pushRecoveryScript()
            
            # reboot into recovery
            cmd = [
                self.mainConfiguration.adbPath,
                "-s",
                self.serialNumber,
                "reboot",
                "recovery"
            ]
            self._logger.debug(OSCommand.executeCommand(cmd))
            
            time.sleep(30)
            self._waitForDeviceToBeReady()
            
            time.sleep(5) # Wait 5 seconds to be sure SDcard will be mounted
            
            # When device is ready, don't forget to restore sdcard
            self.__restoreSDCard()

    def stimulateWithMonkey(self, packageName):
        """Stimulates application with monkey"""

        if packageName is None or len(packageName)==0:
            raise Exception("Cannot stimulate package that has no name.")

        self._logger.info("Stimulating package {0} with monkey.".format(packageName))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "monkey",
            "-p",
            packageName,
            "-v",
            "500",
            "--throttle",
            "6000",
            "--ignore-timeouts"
        ]
        p = OSCommand.executeAsyncCommand(cmd)
        stdout, stderr = p.communicate()
        self._logger.debug("{0}".format(stdout))
        



        
