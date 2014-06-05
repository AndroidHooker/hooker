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
import shutil
import time

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common.OSCommand import OSCommand
from hooker_common import Logger

class AVDEmulator(object):
    """Manage and Android Virtual Device Emulator    
    """

    # Various states the Emulator can take
    STATE_NOT_PREPARED = 0 # The emulator doesn't exist yet (FS)
    STATE_PREPARED = 1 # The emulator exists from a FS perspective
    STATE_STARTING = 2 # The emulator is starting
    STATE_STARTED = 3 # The emulator is started
    
    def __init__(self, emulatorNumber, name, mainConfiguration):        
        self._logger = Logger.getLogger(__name__)
        self.name = name
        self.state = AVDEmulator.STATE_NOT_PREPARED
        self.mainConfiguration = mainConfiguration
        self.emulatorNumber = emulatorNumber
        self.emulatorPort = 5554 + (self.emulatorNumber*2)
        self.emulatorSerialNumber = "emulator-{0}".format(self.emulatorPort)
        self.__emulatorProcess = None
        self.__duplicateAVD()
        
    def start(self):
        """Starts the emulator"""

        if self.state != AVDEmulator.STATE_PREPARED:
            raise Exception("Cannot start the emulator. (expected state was {0}, current state is {1})".format(AVDEmulator.STATE_PREPARED, self.state))

        # clean the temporary directory
        self.__cleanTemporaryDirectory()

        cmd = [
            self.mainConfiguration.emulatorPath,
            "@{0}".format(self.name),
            "-no-snapshot-save",
            "-netspeed",
            "full",
            "-netdelay",
            "none",
            "-port",
            str(self.emulatorPort)
        ]
    
        self.__emulatorProcess = OSCommand.executeAsyncCommand(cmd)
        self.state = AVDEmulator.STATE_STARTING
        
        # waits for device to be ready
        self.__waitForDeviceToBeReady()
    
    def __cleanTemporaryDirectory(self):
        """Clean oldest temporary directories"""

        tmpDir = self.mainConfiguration.androidTemporaryPath

        # list sub-directories by creation date
        mtime = lambda f: os.stat(os.path.join(tmpDir, f)).st_mtime
        subDirs = list(sorted(os.listdir(tmpDir), key=mtime))
        if len(subDirs)>20:
            for dirToDelete in subDirs[:5]:
                fullPath = os.path.join(tmpDir, dirToDelete)
                self._logger.info("Deleting old emulator in cache at {0}".format(fullPath))
                os.remove(fullPath)            
                 
    def installAPK(self, apkFilename):
        """Installs the specified APK on the emulator"""

        if self.state != AVDEmulator.STATE_STARTED:
            raise Exception("Cannot install the application since the emulator is not started.")

        if apkFilename is None or len(apkFilename)==0:
            raise Exception("Cannot install an application that has no name.")

        self._logger.info("Installing APK {0} on emulator {1}".format(apkFilename, self.name))
        
        # $ adb install file.apk
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "install",
            apkFilename
        ]
        OSCommand.executeCommand(cmd)

    def startActivity(self, activity):
        """Starts the specified activity on the emulator"""

        if self.state != AVDEmulator.STATE_STARTED:
            raise Exception("Cannot start an activity since the emulator is not started.")

        if activity is None or len(activity)==0:
            raise Exception("Cannot start an activity that has no name.")

        if not self.__checkADBRecognizeEmu():
            # self.__restartADBServer() # We cannot do that if we have multiple emulators...
            raise Exception("ADB didn't find {0}".format(self.name))

        self._logger.info("Starting activity {0} on emulator {1}".format(activity, self.name))

        activityPackage = '.'.join(activity.split('.')[:-1])
        activityName = ''.join(activity.split('.')[-1:])
                
        # $ adb shell am start -n activityPackage/activity
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "am",
            "start",
            "-n",
            "{0}/.{1}".format(activityPackage, activityName)
        ]
        
        OSCommand.executeAsyncCommand(cmd)


    def startActivityFromPackage(self, packageName, activityName):
        """
        Starts the specified activity from the specified package name on the emulator.
        This method has to be called when package name is different from main activity.
        """

        if self.state != AVDEmulator.STATE_STARTED:
            raise Exception("Cannot start an activity since the emulator is not started.")

        if activityName is None or len(activityName)==0:
            raise Exception("Activity name is null.")

        if packageName is None or len(packageName)==0:
            raise Exception("Package name is null.")

        if not self.__checkADBRecognizeEmu():
            # self.__restartADBServer() # We cannot do that if we have multiple emulators...
            raise Exception("ADB didn't find {0}".format(self.name))
            
        self._logger.info("Starting activity {0}/{1} on emulator {2}".format(packageName, activityName, self.name))

        # $ adb shell am start -n activityPackage/activity
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "am",
            "start",
            "-n",
            "{0}/{1}".format(packageName, activityName)
        ]
        
        OSCommand.executeAsyncCommand(cmd)


    def __checkADBRecognizeEmu(self):
        """
        Checks that ADB recognizes the emulator. Returns True if device is recognized by ADB, False otherwise.
        """
        
        if self.state != AVDEmulator.STATE_STARTED:
            raise Exception("Cannot check ADB connectivity if the emulator is not started.")

        self._logger.info("Checking if ADB recognizes emulator...")
            
        cmd = [
            self.mainConfiguration.adbPath,
            "devices"
        ]
        
        output = OSCommand.executeCommand(cmd)
        
        if self.emulatorSerialNumber in output:
            self._logger.debug("Emulator has been find!")
            return True

        self._logger.error("Emulator has not been found.")
        return False


    def __restartADBServer(self):
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
        

    def waitToBeClosed(self):
        """Waits for the emulator to be closed by the user."""
        if self.state != AVDEmulator.STATE_STARTED or self.__emulatorProcess is None:
            raise Exception("The emulator is not started, cannot wait for the user to close it.")

        self._logger.debug("Waiting for the emulator to finish.")
        
        self.__emulatorProcess.wait()


    def __waitForDeviceToBeReady(self):
        """Analyzes the emulator and returns when it's ready."""
        
        if self.state != AVDEmulator.STATE_STARTING:
            raise Exception("Cannot wait of a device if its not started, its current state is '{0}'".format(self.state))
        
        self._logger.debug("Waiting for device {0} to be ready.".format(self.emulatorSerialNumber))
        
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "wait-for-device"
        ]
        OSCommand.executeCommand(cmd)
        
        self._logger.debug("Waiting for the emulator to be ready")
        self._logger.debug(" - (dev.bootcomplete)")
        ready = False
        while not ready:
            cmd = [
                self.mainConfiguration.adbPath,
                "-s",
                self.emulatorSerialNumber,
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
                self.emulatorSerialNumber,
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
                self.emulatorSerialNumber,
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
        self._logger.debug("Emulator {0} is ready !".format(self.emulatorSerialNumber))
        self.state = AVDEmulator.STATE_STARTED


    def writeContentOnSdCard(self, filename, fileContent):
        """Create (or replace) the filename related to the hooker path
        on the sdcard of the emulator with the specified fileContent."""

        hookerDir = "/mnt/sdcard/hooker/"
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "mkdir",
            hookerDir
        ]
        OSCommand.executeCommand(cmd)

        filePath = os.path.join(hookerDir, filename)
        self._logger.debug("Writing content on '{0}'".format(filePath))
                          
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "touch",
            filePath
        ]
        OSCommand.executeCommand(cmd)            
            
        cmd = '{0} -s {1} shell echo "{2}" > {3}'.format(
            self.mainConfiguration.adbPath, self.emulatorSerialNumber,fileContent, filePath)
        
        OSCommand.executeCommand(cmd)


    def rebootAVD(self):
        """Reboot the emulator"""
        self._logger.info("Rebooting AVD listening on port {0}".format(self.emulatorSerialNumber))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "setprop",
            "ctl.restart",
            "zygote"
        ]
        OSCommand.executeAsyncCommand(cmd)

        self.state = AVDEmulator.STATE_STARTING
        # waits for device to be ready
        self.__waitForDeviceToBeReady()
        

    def stopAVD(self):
        """ Stop the emulator"""
        self._logger.info("Stopping AVD listening on port {0}".format(self.emulatorSerialNumber))

        if self.__emulatorProcess is None:
            raise Exception("Emulator process is null, cannot stop emulator on port {0}".format(self.emulatorSerialNumber))

        # First clean the SD card
        self.__removeDirectoryHookerFromAVD()

        # Kill process
        self.__emulatorProcess.kill()
        

    def stimulateWithMonkey(self, packageName):
        """Stimulates application with monkey"""

        if self.state != AVDEmulator.STATE_STARTED:
            raise Exception("Emulator is not started.")

        if packageName is None or len(packageName)==0:
            raise Exception("Cannot stimulate package that has no name.")

        self._logger.info("Stimulating package {0} with monkey.".format(packageName))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
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
        OSCommand.executeAsyncCommand(cmd) 
        
    @staticmethod
    def createTemplates(mainConfiguration, analysisConfiguration):
        """Duplicates the initial template, one for each emulator"""
        
        refAVDName = os.path.split(mainConfiguration.referenceAVD)[1]
        refAvdConfigFile = mainConfiguration.referenceAVD+".ini"
        refAVDDir = os.path.join(mainConfiguration.virtualDevicePath, refAVDName+".avd/")
        for emulatorNumber in range(analysisConfiguration.maxNumberOfEmulators):
            newAvdConfigFile = mainConfiguration.referenceAVD+"_"+str(emulatorNumber)+".ini"            
            newAVDDir = os.path.join(mainConfiguration.virtualDevicePath, refAVDName+"_"+str(emulatorNumber)+".avd/")
            # delete old versions
            if os.path.exists(newAvdConfigFile):
                os.remove(newAvdConfigFile)

            if os.path.isdir(newAVDDir):
                shutil.rmtree(newAVDDir) 
            
            shutil.copyfile(refAvdConfigFile, newAvdConfigFile)

            cmd = "cp -R {0} {1}".format(refAVDDir, newAVDDir)
            OSCommand.executeCommand(cmd)

    def __duplicateAVD(self):
        """Creates a new emulator based on a reference one."""
        self._logger.debug("Duplicate AVD '{0}'.".format(self.mainConfiguration.referenceAVD))

        # clean/delete if new emulator already exists
        self.__deleteEmulatorFS()

        refAVDName = os.path.split(self.mainConfiguration.referenceAVD)[1]
        avdConfigFile = self.mainConfiguration.referenceAVD+"_"+str(self.emulatorNumber)+".ini"
        newConfigFile = os.path.join(self.mainConfiguration.virtualDevicePath, self.name+".ini")
        referenceAVDDir = os.path.join(self.mainConfiguration.virtualDevicePath, refAVDName+"_"+str(self.emulatorNumber)+".avd/")
        newAVDDir = os.path.join(self.mainConfiguration.virtualDevicePath, self.name+".avd/")
        hwQemuConfigFile = os.path.join(newAVDDir, "hardware-qemu.ini")
        defaultSnapshotConfigFile = os.path.join(newAVDDir, "snapshots.img.default-boot.ini")

        # First we copy the template       
        self._logger.debug("Copy AVD reference config file '{0}' in '{1}'...".format(avdConfigFile, newConfigFile))
        shutil.copyfile(avdConfigFile, newConfigFile)

        # Copy the internal files of the reference avd
        self._logger.debug("Duplicate the AVD internal content from '{0}' in '{1}'...".format(referenceAVDDir, newAVDDir))
        # we use the internal linux 'cp' command for performance issues (shutil is too long)
        # shutil.copytree(referenceAVDDir, newAVDDir)
        cmd = "cp -R {0} {1}".format(referenceAVDDir, newAVDDir)
        OSCommand.executeCommand(cmd)

        # Than adapt the content of the copied files
        self.__replaceContentInFile(newConfigFile, refAVDName, self.name)
        self.__replaceContentInFile(hwQemuConfigFile, refAVDName, self.name)
        self.__replaceContentInFile(defaultSnapshotConfigFile, refAVDName, self.name)

        self.state = AVDEmulator.STATE_PREPARED
        
    def __replaceContentInFile(self, fileName, contentToReplace, replacementContent):
        """Replaces the specified motif by a specified value in the specified file"""
        
        self._logger.debug("Replacing '{0}' with '{1}' in '{2}'".format(contentToReplace, replacementContent, fileName))
        newLines = []
        with open(fileName, 'r') as fd:
            lines = fd.readlines()
            for line in lines:
                newLines.append(line.replace(contentToReplace, replacementContent))

        with open(fileName, 'w') as fd:
            fd.writelines(newLines)
            

    def __deleteEmulatorFS(self):
        """Deletes any trace of an emulator that would have the same name as the one of the current emulator."""
        
        avdConfigFile = os.path.join(self.mainConfiguration.virtualDevicePath, self.name+".ini")
                           
        if os.path.exists(avdConfigFile):
            self._logger.debug("Deleting old emulator config file '{0}'".format(avdConfigFile))
            os.remove(avdConfigFile)

        avdDir = os.path.join(self.mainConfiguration.virtualDevicePath, self.name+".avd/")
        if os.path.isdir(avdDir):
            self._logger.debug("Deleting old emulator FS '{0}'".format(avdDir))
            shutil.rmtree(avdDir)            


    def __removeDirectoryHookerFromAVD(self):
        """Removes directory on the emulator where hooker has copied files.
        """
        hookerDir = "/mnt/sdcard/hooker/"
        self._logger.debug("Deleting {0} directory on emulator {1}".format(hookerDir, self.emulatorSerialNumber))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.emulatorSerialNumber,
            "shell",
            "rm",
            "-rf",
            hookerDir
        ]
        OSCommand.executeCommand(cmd)


    @property
    def name(self):
        """The name of the emulator
        """
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise Exception("An emulator cannot have a null name.")
        self.__name = name

    @property
    def state(self):
        """The state of the emulator
        """
        return self.__state

    @state.setter
    def state(self, state):
        if state is None:
            raise Exception("An emulator cannot have a null state.")
        self.__state = state

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
    def emulatorNumber(self):
        """The emulator number
        """
        return self.__emulatorNumber

    @emulatorNumber.setter
    def emulatorNumber(self, emulatorNumber):
        if emulatorNumber is None:
            raise Exception("No emulator number provided.")
        self.__emulatorNumber = emulatorNumber

    @property
    def emulatorSerialNumber(self):
        """The emulator serial number
        """
        return self.__emulatorSerialNumber

    @emulatorSerialNumber.setter
    def emulatorSerialNumber(self, emulatorSerialNumber):
        if emulatorSerialNumber is None:
            raise Exception("No emulator serial number provided.")
        self.__emulatorSerialNumber = emulatorSerialNumber
        
