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
from hooker_xp.analysis.ManualAnalysisConfiguration import ManualAnalysisConfiguration

class AutomaticAnalysisConfiguration(ManualAnalysisConfiguration):
    """A container that stores all the parameters of an automatic analysis
    """

    def __init__(self, apkFiles, prepareAPKs=None, scenario=None, outputDirectory=None, maxNumberOfEmulators=1, backupDirectory=None):
        super(AutomaticAnalysisConfiguration, self).__init__(apkFiles, maxNumberOfEmulators, prepareAPKs)
        self.scenario = scenario
        self.outputDirectory = outputDirectory
        self.backupDirectory = backupDirectory

    def __str__(self):
        """toString method"""
        lines = [
            "Automatic Analysis Conf.:",
            "\t- APKs\t\t\t{0}".format(','.join(self.apkFiles)),
            "\t- Nb Emulators\t\t{0}".format(self.maxNumberOfEmulators),
            "\t- Preparation APKs\t{0}".format(','.join(self.prepareAPKs)),
            "\t- Scenario\t\t{0}".format(','.join(self.scenario)),
            "\t- Output directory\t{0}".format(self.outputDirectory),
            "\t- Backup directory\t{0}".format(self.backupDirectory)
            ]
        return '\n'.join(lines)
        
    @property
    def scenario(self):
        """The scenario of the analysis
        """
        return self.__scenario

    @scenario.setter
    def scenario(self, scenario):
        if scenario is None:
            raise Exception("You must provide a scenario to execute.")
        self.__scenario = scenario

    @property
    def outputDirectory(self):
        """The output directory for the analysis
        """
        return self.__outputDirectory

    @outputDirectory.setter
    def outputDirectory(self, outputDirectory):
        if outputDirectory is None:
            raise Exception("You must provide an output directory to store analyzed APKs.")
        self.__outputDirectory = outputDirectory

    @property
    def backupDirectory(self):
        """The backup directory for the analysis
        """
        return self.__backupDirectory

    @backupDirectory.setter
    def backupDirectory(self, backupDirectory):
        self.__backupDirectory = backupDirectory
