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

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+


class MainConfiguration(object):
    """A container that stores all the parameters required to start an analysis
    """

    def __init__(self, referenceAVD, androidSDKPath, androidTemporaryPath, androguardPath):
        self.referenceAVD = referenceAVD
        self.androidSDKPath = androidSDKPath
        self.androidTemporaryPath = androidTemporaryPath
        self.virtualDevicePath = os.path.dirname(referenceAVD)
        self.emulatorPath = os.path.join(androidSDKPath, "tools/emulator64-arm")
        self.adbPath = os.path.join(androidSDKPath, "platform-tools/adb")
        self.androguardPath = androguardPath
    
    @staticmethod
    def build(commandLineParser):
        """Builds and returns a MainConfiguration based on values
        contained in the specified CommandLineParser"""
        
        if commandLineParser is None:
            raise Exception("Cannot build the main configuration if no commandLineParser is provided")

        mainOptions = commandLineParser.mainOptions
        
        if not 'referenceavd' in mainOptions.keys():
            raise Exception("The referenceAVD configuration entry is missing.")
        refAvdDirectory = mainOptions['referenceavd'] + '.avd/'
        if not os.path.isdir(refAvdDirectory):
            raise Exception("'{0}' is not a directory.".format(refAvdDirectory))
        if not os.access(refAvdDirectory, os.R_OK):
            raise Exception("You don't have read access to directory {0}.".format(refAvdDirectory))
        refAVD = mainOptions['referenceavd']

        if not 'androidsdkpath' in mainOptions.keys():
            raise Exception("The androidSDKPath configuration entry is missing.")
        androidSDKPath = mainOptions['androidsdkpath']
        if not os.path.isdir(androidSDKPath):
            raise Exception("'{0}' is not an existing directory.".format(androidSDKPath))
        if not os.access(androidSDKPath, os.R_OK):
            raise Exception("You don't have read access to directory {0}.".format(androidSDKPath))

        if not 'androidtemporarypath' in mainOptions.keys():
            raise Exception("The androidTemporaryPath configuration entry is missing.")
        androidTemporaryPath = mainOptions['androidtemporarypath']
        if not os.path.isdir(androidTemporaryPath):
            raise Exception("'{0}' is not an existing directory.".format(androidTemporaryPath))
        if not os.access(androidTemporaryPath, os.W_OK):
            raise Exception("You don't have write access to directory {0}.".format(androidTemporaryPath))

        if not 'androguardpath' in mainOptions.keys():
            raise Exception("The androguardPath configuration entry is missing.")
        androguardPath = mainOptions['androguardpath']
        if not os.path.isdir(androguardPath):
            raise Exception("'{0}' is not an existing directory.".format(androguardPath))
        if not os.access(androguardPath, os.R_OK):
            raise Exception("You don't have read access to directory {0}.".format(androguardPath))

        return MainConfiguration(refAVD, androidSDKPath, androidTemporaryPath, androguardPath)

    def __str__(self):
        """toString method"""
        lines = [
            "Main Conf:",
            "\t- SDK\t\t\t{0}".format(self.androidSDKPath),            
            "\t- Ref. AVD\t\t{0}".format(self.referenceAVD),
            "\t- Androguard\t\t{0}".format(self.androguardPath)
            ]
        return '\n'.join(lines)
        
    @property
    def referenceAVD(self):
        """Path to the reference AVD we will use to clone
        """
        return self.__referenceAVD

    @referenceAVD.setter
    def referenceAVD(self, referenceAVD):
        if referenceAVD is None:
            raise Exception("The reference AVD cannot be null.")
            
        self.__referenceAVD = referenceAVD
        
    @property
    def androidSDKPath(self):
        """Path to the android SDK
        """
        return self.__androidSDKPath

    @androidSDKPath.setter
    def androidSDKPath(self, androidSDKPath):
        if androidSDKPath is None:
            raise Exception("The android SDK path cannot be null.")
        self.__androidSDKPath = androidSDKPath
                
    @property
    def androidTemporaryPath(self):
        """Path to the android tempory directory
        """
        return self.__androidTemporaryPath

    @androidTemporaryPath.setter
    def androidTemporaryPath(self, androidTemporaryPath):
        if androidTemporaryPath is None:
            raise Exception("The android temporary path cannot be null.")
        self.__androidTemporaryPath = androidTemporaryPath
                    
    @property
    def androidVirtualDevicePath(self):
        """Path to the android virtual device directory
        """
        return self.__androidVirtualDevicePath

    @androidVirtualDevicePath.setter
    def androidVirtualDevicePath(self, androidVirtualDevicePath):
        if androidVirtualDevicePath is None:
            raise Exception("The android virtual device path cannot be null.")
        self.__androidVirtualDevicePath = androidVirtualDevicePath

    @property
    def emulatorPath(self):
        """Path to the emulator binary in android sdk
        """
        return self.__emulatorPath

    @emulatorPath.setter
    def emulatorPath(self, emulatorPath):
        if emulatorPath is None:
            raise Exception("The android emulator path cannot be null.")
        self.__emulatorPath = emulatorPath

    @property
    def adbPath(self):
        """Path to the adb binary
        """
        return self.__adbPath

    @adbPath.setter
    def adbPath(self, adbPath):
        if adbPath is None:
            raise Exception("The adb binary path cannot be null.")
        self.__adbPath = adbPath
        
    @property
    def androguardPath(self):
        """Path to androguard framework
        """
        return self.__androguardPath

    @androguardPath.setter
    def androguardPath(self, androguardPath):
        if androguardPath is None:
            raise Exception("The androguard path cannot be null.")
        self.__androguardPath = androguardPath
