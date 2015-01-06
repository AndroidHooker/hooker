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
import argparse
import os
from ConfigParser import ConfigParser

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_xp import release
from hooker_common import Logger

class CommandLine(object):
    """Reads, validates and parses the command line arguments provided by
    users"""

    def __init__(self):
        self._logger = Logger.getLogger(__name__)
        self.parser = None
        self.manualAnalysisRequested = False
        self.automaticAnalysisRequested = False
        self.mainOptions = dict()
        self.manualOptions = dict()
        self.automaticOptions = dict()
        self.reportingOptions = dict()
        
        self.usage = "usage: %prog [options]"
        self.__parse()
        
    def __parse(self):
        """Read and parse the provided arguments and options"""        
        parser = argparse.ArgumentParser(prog=release.appname, description=release.description)

        parser.add_argument("-c", "--c", nargs=1, required=True, help="configuration file of the analysis")        
        namespace = parser.parse_args()
        configFile = namespace.c

        try:
            self.__parseConfigFile(configFile[0])
        except Exception, e:
            self._logger.fatal("An error occured while parsing the configuration file: {0}".format(e))
        
    def __parseConfigFile(self, configFile):
        """Parses and set the appropriate attributes once
        having parsed the specified configuration file."""
        if not os.path.exists(configFile):
            raise Exception("configuration file '{0}' doesn't exist.".format(configFile))
        
        config = ConfigParser()
        
        try:
            # reads the config file
            config.read(configFile)

            # parse sections
            sections = config.sections()
        except:
            raise Exception("Configuration file is not readable.")
        
        
        # reads the main entry
        if "main" in sections:
            for k, v in self.__parseConfigSection(config, "main").iteritems():
                self.mainOptions[k]=v

        # reads the reporting entry
        if "reporting" in sections:
            for k, v in self.__parseConfigSection(config, "reporting").iteritems():
                self.reportingOptions[k]=v

        # reads the analysis entry
        if "analysis" in sections:
            options = self.__parseConfigSection(config, "analysis")

            # the type option            
            if not "type" in options.keys():
                raise Exception("No analysis 'type' option is specified.")

            typeValue = options["type"].lower()
            if typeValue == "manual":
                self.__prepareForManualAnalysis(options)
            elif typeValue == "automatic":
                self.__prepareForAutomaticAnalysis(options)
            else:
                raise Exception("The specified type of analysis is not supported. Specify either 'manual' or 'automatic', {0} is not valid.".format(typeValue))            

    def __parseConfigSection(self, config, section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
            except:
                dict1[option] = None
        return dict1


    def __prepareForManualAnalysis(self, options):
        """Parse the specified options in the case of a manual
        analysis request. If everything is ok, it sets to True the flags
        self.manualAnalysisRequested
        """

        for k, v in options.iteritems():
            self.manualOptions[k]=v
        
        self.manualAnalysisRequested = True


    def __prepareForAutomaticAnalysis(self, options):
        """Parse the specified options in the case of a automatic
        analysis request. If everything is ok, it sets to True the flags
        self.automaticAnalysisRequested
        """

        for k, v in options.iteritems():
            self.automaticOptions[k]=v
        
        self.automaticAnalysisRequested = True


    @property
    def manualAnalysisRequested(self):
        """A flag indicating a manual analysis is requested and ready.
        :type : a boolean
        """
        return self.__manualAnalysisRequested

    @manualAnalysisRequested.setter
    def manualAnalysisRequested(self, flag):
        if flag is None:
            self.__manualAnalysisRequested = False
        else:
            self.__manualAnalysisRequested = flag

    @property
    def automaticAnalysisRequested(self):
        """A flag indicating a automatic analysis is requested and ready.
        :type : a boolean
        """
        return self.__automaticAnalysisRequested

    @automaticAnalysisRequested.setter
    def automaticAnalysisRequested(self, flag):
        if flag is None:
            self.__automaticAnalysisRequested = False
        else:
            self.__automaticAnalysisRequested = flag
