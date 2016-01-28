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

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+

class ManualAnalysisConfiguration(object):
    """A container that stores all the parameters of a manual analysis
    """

    def __init__(self, apkFiles, maxNumberOfEmulators=1, prepareAPKs=None, backupDirectory=None):
        self.apkFiles = apkFiles
        self.prepareAPKs = prepareAPKs
        self.maxNumberOfEmulators = maxNumberOfEmulators
        self.backupDirectory = backupDirectory

    def __str__(self):
        """toString method"""
        lines = [
            "Manual Analysis Conf.:",
            "\t- APKs\t\t\t{0}".format(','.join(self.apkFiles)),
            "\t- Nb Emulators\t\t{0}".format(self.maxNumberOfEmulators),
            "\t- Preparation APKs\t{0}".format(','.join(self.prepareAPKs)),
            "\t- Backup directory\t{0}".format(self.backupDirectory)
            ]
        return '\n'.join(lines)
        
    @property
    def apkFiles(self):
        """The apk files that must be analyzed
        """
        return self.__apkFiles

    @apkFiles.setter
    def apkFiles(self, apkFiles):
        if len(apkFiles)==0:
            raise Exception("At least one apk must be specified.")
        self.__apkFiles = apkFiles
        
    @property
    def maxNumberOfEmulators(self):
        """The maximum number of emulators started
        """
        return self.__maxNumberOfEmulators

    @maxNumberOfEmulators.setter
    def maxNumberOfEmulators(self, maxNumberOfEmulators):
        if maxNumberOfEmulators is None:
            raise Exception("The android temporary path cannot be null.")
        self.__maxNumberOfEmulators = maxNumberOfEmulators

    @property
    def prepareAPKs(self):
        """The prepareAPKs of the analysis
        """
        return self.__prepareAPKs

    @prepareAPKs.setter
    def prepareAPKs(self, prepareAPKs):
        if prepareAPKs is None:
            prepareAPKs = []
        self.__prepareAPKs = prepareAPKs
        
    @property
    def backupDirectory(self):
        """The backup directory for the analysis
        """
        return self.__backupDirectory

    @backupDirectory.setter
    def backupDirectory(self, backupDirectory):
        self.__backupDirectory = backupDirectory
