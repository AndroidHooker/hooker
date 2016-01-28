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

class AndroidDevice(object):
    """
    The mother of any Android device, emulated or physical.
    """

    # States the device can take
    # These are defined for additionnal checks
    STATE_NOT_PREPARED = 0 # The device doesn't exist yet (FS)
    STATE_PREPARED = 1     # The device exists from a FS perspective (for emulators only)
    STATE_STARTING = 2     # The device is starting
    STATE_STARTED = 3      # The device is started

    def __init__(self, adbPort, name, mainConfiguration):
        self._logger = Logger.getLogger(__name__)
        self.name = name
        self.mainConfiguration = mainConfiguration
        self.adbPort = adbPort
        self._hookerDir = "/mnt/sdcard/hooker/"
        self.serialNumber = ''
        self.state = AndroidDevice.STATE_NOT_PREPARED

        
    def start(self):
        """Starts the device"""
        self._logger.info("Device starting...")
        if not self.__checkADBRecognizeDevice():
            raise Exception("ADB didn't find device {0}".format(self.name))

            
    def installAPK(self, apkFilename):
        """Installs the specified APK on the device"""

        if self.state != AndroidDevice.STATE_STARTED:
            raise Exception("Cannot install the application since the device is not started.")

        if apkFilename is None or len(apkFilename)==0:
            raise Exception("Cannot install an application that has no name.")

        self._logger.info("Installing APK {0} on device {1}".format(apkFilename, self.name))
        
        # $ adb install file.apk
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "install",
            apkFilename
        ]
        OSCommand.executeCommand(cmd)

    def startActivity(self, activity):
        """Starts the specified activity on the device"""
        if self.state != AndroidDevice.STATE_STARTED:
            raise Exception("Cannot start an activity since the device is not started.")

        if activity is None or len(activity)==0:
            raise Exception("Cannot start an activity that has no name.")

        self._logger.info("Starting activity {0} on device {1}".format(activity, self.name))

        activityPackage = '.'.join(activity.split('.')[:-1])
        activityName = ''.join(activity.split('.')[-1:])
                
        # $ adb shell am start -n activityPackage/activity
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "am",
            "start",
            "-n",
            "{0}/.{1}".format(activityPackage, activityName)
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug("{}".format(res))


    def checkAPKInstrumenter(self):
        """Checks that APKInstrumenter application is installed on the device"""
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "pm",
            "list",
            "packages",
            "com.amossys.hooker"
        ]
        ret = OSCommand.executeCommand(cmd)
        if ret is None or len(ret)==0 or 'hooker' not in ret:
            raise Exception("APKInstrumenter application is not installed on your device. Please set up your device properly (see README file)")
        self._logger.info("ApkInstrumenter application is installed on device")
        

    def startActivityFromPackage(self, packageName, activityName):
        """
        Starts the specified activity from the specified package name on the device.
        This method has to be called when package name is different from main activity.
        """
        if self.state != AndroidDevice.STATE_STARTED:
            raise Exception("Cannot start an activity since the device is not started.")

        if activityName is None or len(activityName)==0:
            raise Exception("Activity name is null.")

        if packageName is None or len(packageName)==0:
            raise Exception("Package name is null.")

        self._logger.info("Starting activity {0}/{1} on device {2}".format(packageName, activityName, self.name))

        # $ adb shell am start -n activityPackage/activity
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "am",
            "start",
            "-n",
            "{0}/{1}".format(packageName, activityName)
        ]
        p = OSCommand.executeAsyncCommand(cmd)
        stdout,stderr = p.communicate()
        self._logger.debug("{0}".format(stdout))


    def _restartADBServer(self):
        """
        Restarts ADB server. This function is not used because we have to verify we don't have multiple devices.
        """
        self._logger.info("Restarting ADB server...")
            
        cmd = [
            self.mainConfiguration.adbPath,
            "kill-server"
        ]
        OSCommand.executeCommand(cmd)
        self._logger.info("ADB server has been killed.")

        cmd = [
            self.mainConfiguration.adbPath,
            "start-server"
        ]
        OSCommand.executeCommand(cmd)
        self._logger.info("ADB server has been restarted.")
        
    def _waitForDeviceToBeReady(self):
        """Analyzes the device state and returns when it's ready."""
        if self.state != AndroidDevice.STATE_STARTING:
            raise Exception("Cannot wait of a device if its not started, its current state is '{0}'".format(self.state))
        
        self._logger.debug("Waiting for device {0} to be ready.".format(self.serialNumber))
        
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "wait-for-device"
        ]
        OSCommand.executeCommand(cmd)
        
        self._logger.debug("Waiting for the device to be ready")
        self._logger.debug(" - (dev.bootcomplete)")
        ready = False
        while not ready:
            cmd = [
                self.mainConfiguration.adbPath,
                "-s",
                self.serialNumber,
                "shell",
                "getprop",
                "dev.bootcomplete"
                ]
            result = OSCommand.executeCommand(cmd)
            if result is not None and result.strip() == "1":
                ready = True
            else:
                time.sleep(1)            

        self._logger.debug("- (sys_bootcomplete)")
        ready = False
        while not ready:
            cmd = [
                self.mainConfiguration.adbPath,
                "-s",
                self.serialNumber,
                "shell",
                "getprop",
                "sys.boot_completed"
                ]
            result = OSCommand.executeCommand(cmd)
            if result is not None and result.strip() == "1":
                ready = True
            else:
                time.sleep(1)
            
            self._logger.debug(" - (init.svc.bootanim)")
            ready = False
            while not ready:
                cmd = [
                    self.mainConfiguration.adbPath,
                    "-s",
                    self.serialNumber,
                    "shell",
                    "getprop",
                    "init.svc.bootanim"
                ]
                result = OSCommand.executeCommand(cmd)
                if result is not None and result.strip() == "stopped":
                    ready = True
                else:
                    time.sleep(1)

        time.sleep(5)
        self._logger.debug("Device {0} seems to be ready".format(self.serialNumber))
        self.state = AndroidDevice.STATE_STARTED
        

    def writeContentOnSdCard(self, filename, fileContent):
        """Create (or replace) the filename related to the hooker path
        on the sdcard of the device with the specified fileContent."""       
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "mkdir",
            self._hookerDir
        ]
        OSCommand.executeCommand(cmd)

        filePath = os.path.join(self._hookerDir, filename)
        self._logger.debug("Writing content on '{0}'".format(filePath))
                          
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "touch",
            filePath
        ]
        OSCommand.executeCommand(cmd)            
            
        cmd = [
            self.mainConfiguration.adbPath, "-s", self.serialNumber, "shell",
            "echo", "\"{}\"".format(fileContent), ">", filePath
        ]
        OSCommand.executeCommand(cmd)


    def _pullResults(self):
        """Pull results of analysis"""
        self._logger.info("Pulling results of analysis")
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "pull",
            "/sdcard/hooker/events.logs",
            "{0}{1}-events.logs".format(self.mainConfiguration.androidTemporaryPath,
                            datetime.datetime.now().strftime("%Y-%m-%d-%H:%M"))
        ]
        p = OSCommand.executeAsyncCommand(cmd)
        stdout, stderr = p.communicate()
        self._logger.debug("{0}".format(stdout))

        self._logger.info("Event logs has been pulled in {0}".format(self.mainConfiguration.androidTemporaryPath))


    def __checkADBRecognizeDevice(self):
        """
        Checks that ADB recognizes the device. Returns True if device is recognized by ADB, False otherwise.
        """
        self._logger.info("Checking if ADB recognizes device...")
            
        cmd = [
            self.mainConfiguration.adbPath,
            "devices"
        ]
        
        output = OSCommand.executeCommand(cmd)

        if self.serialNumber in output:
            self._logger.debug("Device has been find!")
            return True

        self._logger.error("Device has not been found.")
        return False

        
    def stimulateWithMonkey(self, packageName):
        """Stimulates application with monkey"""
        if self.state != AndroidDevice.STATE_STARTED:
            raise Exception("Device is not started.")

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

        
    @property
    def name(self):
        """The name of the device
        """
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise Exception("An device cannot have a null name.")
        self.__name = name

    @property
    def mainConfiguration(self):
        """The main configuration
        """
        return self.__mainConfiguration

    @mainConfiguration.setter
    def mainConfiguration(self, configuration):
        if configuration is None:
            raise Exception("No main configuration provided.")
        self.__mainConfiguration = configuration

    @property
    def adbPort(self):
        """The device number
        """
        return self.__adbPort

    @adbPort.setter
    def adbPort(self, adbPort):
        if adbPort is None:
            raise Exception("No device number provided.")
        self.__adbPort = adbPort

    @property
    def serialNumber(self):
        """The device serial number
        """
        if self.__serialNumber is None:
            raise Exception("SerialNumber is None")
        return self.__serialNumber

    @serialNumber.setter
    def serialNumber(self, serialNumber):
        if serialNumber is None:
            raise Exception("No device serial number provided.")
        self.__serialNumber = serialNumber

    @property
    def state(self):
        """The state of the device
        """
        return self.__state

    @state.setter
    def state(self, state):
        if state is None:
            raise Exception("A device cannot have a null state.")
        self.__state = state

