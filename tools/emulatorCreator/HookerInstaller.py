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

import os
import sys
import time
import traceback
import subprocess
import fileinput
import argparse
import datetime

from hooker_common.OSCommand import OSCommand
from hooker_common import Logger

class HookerInstaller(object):
    """
    Let you install Hooker the easy way.
    """

    def __init__(self, avdName, avdDir, sdkPath):
        self._logger = Logger.getLogger(__name__)
        self.__avdName = avdName
        self.__sdkPath = sdkPath
        self.__avdDir = avdDir
        self.__adbPath = "{}/platform-tools/adb".format(self.__sdkPath)
        self.__emulatorPath = "{}/tools/emulator".format(self.__sdkPath)
        self.__android_path = "{}/tools/android".format(self.__sdkPath)
        self.__emulatorProcess = None
        self.__arch = None

    def checkEnvironment(self, arch):
        self._logger.info("Checking environment.")
        if not os.path.exists(self.__adbPath):
            raise Exception("ADB path does not exist: {}".format(self.__adbPath))
        if not os.path.exists(self.__emulatorPath):
            raise Exception("Emulator path is not valid: {}".format(self.__emulatorPath))
        if not os.path.exists("HookerInstaller.py"):
            raise Exception("You must execute script within {} directory".format(os.path.join("Hooker", "tools", "emulatorCreator")))
        if arch is None:
            raise Exception("Architecture cannot be None")
        if not os.path.exists(os.path.join("SuperSU-chainfire", arch)):
            raise Exception("Cannot find architecture folder {}".format(os.path.join("SuperSU-chainfire", arch)))
        self.__arch = arch

    def createAvd(self, sd_size, target, ramSize, vm_heapsize, partition_size):
        self._logger.info("Creating AVD.")
        self.__partitionSize = str(partition_size)
        
        if self.__arch == "armv7":
            abi = "default/armeabi-v7a"
        elif self.__arch == "x86":
            abi = "default/x86"
        else:
            raise Exception("ABI for architecture {} is not support".format(self.__arch))

        self.__ramSize = ramSize
        self.__heapSize = vm_heapsize
        
        # Check if AVD already exists
        avdPath = os.path.join(self.__avdDir, "{}.avd".format(self.__avdName))
        if os.path.exists(avdPath):
            raise Exception("AVD already exists: {}".format(avdPath))
        if os.path.exists(os.path.join(self.__avdDir, "{}.ini".format(self.__avdName))):
            raise Exception("File ini already exists: {}".format(os.path.join(self.__avdDir, "{}.ini".format(self.__avdName))))
        # Create AVD
        cmd = [
            self.__android_path, "create", "avd", "--name", self.__avdName,
            "--snapshot", "--sdcard", "{}".format(sd_size), "--target", target, "--path", avdPath, "--abi", abi
        ]
        self._logger.debug(cmd)
        p1 = subprocess.Popen(["echo", "no"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        result = p2.communicate()[0]

        #self._logger.warning(result)
        if "Error" in result:
            raise Exception(traceback.format_exc())

        # Replace heapSize and ramSize values in config.ini
        self._logger.info("Replacing heapSize and ramSize values in config.ini file")
        self.__replace(os.path.join(avdPath, "config.ini"))
        
        
    def stopAvd(self):
        if self.__emulatorProcess is not None:
            self.__emulatorProcess.kill()
            self._logger.warning("AVD has been closed.")
        else:
            self._logger.warning("AVD is already closed.")
            
    def startInstaller(self):
        self._logger.info("Starting installer.")
        if self.__checkAvdExist():
            self._logger.info("Starting AVD... This can take some time, be patient and check your process if in doubt.")
            self.__emulatorProcess = self.__startAvd()
            time.sleep(2)
            if self.__emulatorProcess.poll() is not None:
                raise Exception(self.__emulatorProcess.communicate())

            time.sleep(5)

            self._waitForDeviceToBeReady()
            self._logger.info("Ready to begin install")
            
            localTime = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
            cmd = [
                self.__adbPath, "-s", "emulator-5554", "shell", "date", "-s", localTime
            ]
            self._logger.debug(OSCommand.executeCommand(cmd))
            
            # Install applications on device
            self.__installApk()
            # Print instructions to guide user to click on "Link Substrate Files" and "Restart System Soft"
            self._logger.info("----------------------------------------------------------")
            self._logger.info("You can now:")
            self._logger.info("* Open SuperSU app, click on \"Continue\" to update SU binary, choose the \"Normal\" installation mode, wait a bit. Click on \"OK\" (NOT \"Reboot\"!) and exit the application.")
            self._logger.info("* Open Substrate app, click \"Link Substrate Files\", allow Substrate, and reclick again on \"Link Substrate Files\".")
            self._logger.info("* Install APK-instrumenter APK: {} install ../../APK-instrumenter/bin/ApkInstrumenterActivity-debug.apk".format(self.__adbPath))
            self._logger.info("* Click on \"Restart System (Soft)\"".format(self.__adbPath))
            self._logger.info("* Wait for the system to restart and disable the lockscreen security: `Menu > System Settings > Security > Screen lock > None`")
            self._logger.info("* Close the emulator")
            self._logger.info("----------------------------------------------------------")
                

    def __replace(self, filepath):
        # Replace wanted parameters
        self._logger.debug("Replacing parameters in file: {}".format(filepath))
        
        if not os.path.exists(filepath):
            raise Exception("File: {} does not exist".format(filepath))

        for line in fileinput.input(filepath, inplace=1):
            if "hw.ramSize" in line:
                line = "hw.ramSize = {}\n".format(self.__ramSize)
            elif "vm.heapSize"in line:
                line = "vm.heapSize = {}\n".format(self.__heapSize)
            sys.stdout.write(line)
            
    def __installApk(self):
        """
        Installs APK within the AVD.
        """
        
        binsuPath = os.path.join("SuperSU-chainfire", self.__arch, "su")
        substratePath = "com.saurik.substrate_0.9.4010.apk"
        suApkPath = os.path.join("SuperSU-chainfire", "common", "Superuser.apk")
                
        if not os.path.exists(binsuPath):
            raise Exception("BinSU path is not valid: {}".format(binsuPath))
        if not os.path.exists(suApkPath):
            raise Exception("SuperUser APK path is not valid: {}".format(suApkPath))
        if not os.path.exists(substratePath):
            raise Exception("Substrate path is not valid: {}".format(substratePath))

        # Parse result of mount command to extract /system partition options
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "shell", "mount"
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)
        partition = None
        for line in res.split('\n'):
            if "/system" in line:
                partition = line.split(' ')
                break
        if partition is None:
            raise Exception("No /system partition has been found")

        partition_block = partition[0]
        partition_type = partition[2]
        self._logger.debug("Found /system partition of type: {} and block: {}".format(partition_type, partition_block))

        # Mount /system as RW
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "shell", "mount", "-o", "rw,remount", "-t",
            partition_type, partition_block, "/system"
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)
        time.sleep(1) 
        
        # Get Android version
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "shell", "getprop", "ro.build.version.release"
        ]
        version = OSCommand.executeCommand(cmd)
        self._logger.warning("Android version: {}".format(version))

        # Push SU binary
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "push", binsuPath, "/system/xbin/su"
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)
        
        # Set SU execution rights
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "shell", "chmod", "06755", "/system/xbin/su"
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)

        cmd = [
            self.__adbPath, "-s", "emulator-5554", "install", suApkPath
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)
        
        if ("4.1" in version) or ("4.2" in version):
            self._logger.debug("Nothing special to do for these versions of Android")
        
        elif ("4.3" in version) or ("4.4" in version) or ("5.0" in version):
            if True:
                raise Exception("Android version {} is not supported.".format(version))
            else:
                # This is a try to prepare emulator for higher versions, but is not working for now
                # Launch su as a deamon
                cmd = [
                    self.__adbPath, "-s", "emulator-5554", "shell", "/system/xbin/su", "-d", "&"
                ]
                res = OSCommand.executeCommand(cmd)
                
                if "4.4" in version:
                    # Upload SELinux policy and library
                    libsupolPath = os.path.join("SuperSU-chainfire", self.__arch, "libsupol.so")
                    supolicyPath = os.path.join("SuperSU-chainfire", self.__arch, "supolicy")
                    if not os.path.exists(libsupolPath):
                        raise Exception("Libsupol.so path is not valid: {}".format(libsupolPath))
                    if not os.path.exists(supolicyPath):
                        raise Exception("Supolicy path is not valid: {}".format(supolicyPath))
                    cmd = [
                        self.__adbPath, "-s", "emulator-5554", "push", supolicyPath, "/system/xbin/supolicy"
                    ]
                    res = OSCommand.executeCommand(cmd)
                    self._logger.debug(res)
                    
                    cmd = [
                        self.__adbPath, "-s", "emulator-5554", "shell", "chmod", "06755", "/system/xbin/supolicy"
                    ]
                    res = OSCommand.executeCommand(cmd)
                    self._logger.debug(res)
                    
                    cmd = [
                        self.__adbPath, "-s", "emulator-5554", "push", libsupolPath, "/system/lib/libsupol.so"
                    ]
                    res = OSCommand.executeCommand(cmd)
                    self._logger.debug(res)
                
        else:
            raise Exception("Android version {} is not supported.".format(version))
        
        # Install substrate application
        cmd = [
            self.__adbPath, "-s", "emulator-5554", "install", substratePath
        ]
        res = OSCommand.executeCommand(cmd)
        self._logger.debug(res)

        self._logger.info("Installation of APK has finished.")

                
    def __checkAvdExist(self):
        """Checks if AVD exist"""
        res = OSCommand.executeCommand("{} -list-avds".format(self.__emulatorPath))
        if self.__avdName in res:
            self._logger.info("Device {} found".format(self.__avdName))
            return True

        self._logger.error("Device {} not found.".format(self.__avdName))
        return False

    def __startAvd(self):
        """ Starts AVD """
        cmd = [
            self.__emulatorPath, "-avd", self.__avdName, "-partition-size", self.__partitionSize
        ]
        return OSCommand.executeAsyncCommand(cmd)


    def _waitForDeviceToBeReady(self):
        """Analyzes the device state and returns when it's ready."""
        
        self._logger.debug("Waiting for device to be ready.")

        cmd = [
            self.__adbPath, "-s", "emulator-5554", "wait-for-device"
        ]
        OSCommand.executeCommand(cmd)
        
        self._logger.debug("Waiting for the device to be ready")
        self._logger.debug(" - (dev.bootcomplete)")
        ready = False
        while not ready:
            cmd = [
                self.__adbPath, "-s", "emulator-5554", "shell", "getprop", "dev.bootcomplete"
            ]
            result = OSCommand.executeCommand(cmd)
            if result is not None and result.strip() == "1":
                ready = True
            else:
                time.sleep(2)

        self._logger.debug("- (sys_bootcomplete)")
        ready = False
        while not ready:
            cmd = [
                self.__adbPath, "-s", "emulator-5554", "shell", "getprop", "sys.boot_completed"
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
                    self.__adbPath, "-s", "emulator-5554", "shell", "getprop", "init.svc.bootanim"
                ]
                result = OSCommand.executeCommand(cmd)
                if result is not None and result.strip() == "stopped":
                    ready = True
                else:
                    time.sleep(1)

        time.sleep(5)
        self._logger.info("Device seems to be ready!")


        
if __name__ == "__main__":

    logger = Logger.getLogger(__name__)
    
    # Check params
    parser = argparse.ArgumentParser(prog='HookerInstaller')
    # Mandatory args
    parser.add_argument("-s", "--sdk-path", nargs=1, required=True, help="Path to your SDK directory")
    parser.add_argument("-a", "--avd-name", nargs=1, required=True, help="Name of the AVD you want to create")
    parser.add_argument("-t", "--android-target", nargs=1, required=True, help="Android target you want to create. Use $SDK/tools/android list target to get a list of possible targets")
    parser.add_argument("-d", "--avd-directory", nargs=1, required=True, help="Directory path to your Android AVD")
    # Optional args
    parser.add_argument("-sd", "--sd-size", nargs=1, help="Size of the SD card")
    parser.add_argument("-p", "--partition-size", nargs=1, type=int, help="Size of the system partition in MB")
    parser.add_argument("-ram", "--ram-size", nargs=1, type=int, help="Size of the RAM in MB")
    parser.add_argument("-vm", "--vm-heap-size", nargs=1, type=int, help="Size of the VM heap")
    parser.add_argument("-arch", "--architecture_type", nargs=1, help="Architecture of the emulator (default is armv7)")
    args = parser.parse_args()

    sd_size = args.sd_size
    partition_size = args.partition_size
    ram = args.ram_size
    vm_heapsize = args.vm_heap_size
    arch = args.architecture_type
    
    if sd_size is None:
        logger.info("Setting SD size to default: 500 Mb")
        sd_size = ["500M"]
    if ram is None:
        logger.info("Setting RAM size to default: 1024 Mb")
        ram = ["1024"] # in Mb
    if partition_size is None:
        logger.info("Setting partition size to default: 256 Mb")
        partition_size = ["256"] # in Mb
    if vm_heapsize is None:
        logger.info("Setting VM heap size to default: 64")
        vm_heapsize = ["64"]
    if arch is None:
        logger.info("Setting architecture to armv7")
        arch = ["armv7"]
        
    try:
        installer = HookerInstaller(args.avd_name[0], args.avd_directory[0], args.sdk_path[0])
        installer.checkEnvironment(arch[0])
        installer.createAvd(sd_size[0], args.android_target[0], ram[0], vm_heapsize[0], partition_size[0])
        installer.startInstaller()

    except Exception, e:
        logger.error(e)
        if installer is not None:
            installer.stopAvd()
            
