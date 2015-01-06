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
from hooker_xp.device.AndroidDevice import AndroidDevice

class AVDEmulator(AndroidDevice):
    """
    Manage an Android Virtual Device Emulator    
    """

    def __init__(self, emulatorId, name, mainConfiguration):
        self._logger = Logger.getLogger(__name__)
        super(AVDEmulator, self).__init__(5554 + (int(emulatorId) * 2), name, mainConfiguration)
        self.__emulatorProcess = None
        self.emulatorId = emulatorId
        self.__duplicateAVD()

        self.serialNumber = "emulator-{0}".format(self.adbPort)
        if self.mainConfiguration.typeOfDevice!='emulated':
            raise Exception("Type of device is not emulated, please check your configuration")
        
    def start(self):
        """Starts the emulator"""
        if self.state != AndroidDevice.STATE_PREPARED:
            raise Exception("Cannot start the emulator. (expected state was {0}, current state is {1})".format(AndroidDevice.STATE_PREPARED, self.state))

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
            str(self.adbPort)
        ]
        
        self.__emulatorProcess = OSCommand.executeAsyncCommand(cmd)
        
        self.state = AndroidDevice.STATE_STARTING
        
        # Waits for device to be ready
        self._waitForDeviceToBeReady()

        # Checks that APKInstrumenter is install
        self.checkAPKInstrumenter()
        

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


    def waitToBeClosed(self):
        """Waits for the emulator to be closed by the user."""
        if self.state != AndroidDevice.STATE_STARTED or self.__emulatorProcess is None:
            raise Exception("The emulator is not started, cannot wait for the user to close it.")

        self._logger.debug("Waiting for the device to finish.")
        self.__emulatorProcess.wait()


        
    def reboot(self):
        """Reboot the emulator"""
        self._logger.info("Rebooting AVD listening on port {0}".format(self.serialNumber))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "setprop",
            "ctl.restart",
            "zygote"
        ]
        OSCommand.executeAsyncCommand(cmd)
        time.sleep(5)

        self.state = AndroidDevice.STATE_STARTING
        # waits for device to be ready
        self._waitForDeviceToBeReady()
        

    def stop(self):
        """ Stop the emulator"""
        self._logger.info("Stopping AVD listening on port {0}".format(self.serialNumber))

        if self.__emulatorProcess is None:
            raise Exception("Emulator process is null, cannot stop emulator on port {0}".format(self.serialNumber))                
        # Clean the SD card
        self.__removeDirectoryHookerFromAVD()
        self.__emulatorProcess.kill()
            

    @staticmethod
    def createTemplates(mainConfiguration, analysisConfiguration):
        """Duplicates the initial template, one for each emulator"""
        
        refAVDName = os.path.split(mainConfiguration.referenceAVD)[1]
        refAvdConfigFile = "{0}.ini".format(mainConfiguration.referenceAVD)
        refAVDDir = os.path.join(mainConfiguration.virtualDevicePath, "{0}.avd/".format(refAVDName))
        for emulatorId in range(analysisConfiguration.maxNumberOfEmulators):
            newAvdConfigFile = "{0}_{1}.ini".format(mainConfiguration.referenceAVD, emulatorId)
            newAVDDir = os.path.join(mainConfiguration.virtualDevicePath, "{0}_{1}.avd/".format(refAVDName, emulatorId))

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
        avdConfigFile = "{0}_{1}.ini".format(self.mainConfiguration.referenceAVD, self.emulatorId)
        
        newConfigFile = os.path.join(self.mainConfiguration.virtualDevicePath, "{0}.ini".format(self.name))
        referenceAVDDir = os.path.join(self.mainConfiguration.virtualDevicePath, "{0}_{1}.avd/".format(refAVDName, self.emulatorId))
        newAVDDir = os.path.join(self.mainConfiguration.virtualDevicePath, "{0}.avd/".format(self.name))
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

        self.state = AndroidDevice.STATE_PREPARED

            
    def __replaceContentInFile(self, fileName, contentToReplace, replacementContent):
        """Replaces the specified pattern by a specified value in the specified file"""
        
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
        self._logger.debug("Deleting {0} directory on emulator {1}".format(self._hookerDir, self.serialNumber))
        cmd = [
            self.mainConfiguration.adbPath,
            "-s",
            self.serialNumber,
            "shell",
            "rm",
            "-rf",
            self._hookerDir
        ]
        OSCommand.executeCommand(cmd)
