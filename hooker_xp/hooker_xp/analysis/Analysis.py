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
import time
import os
import hashlib

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_xp.device.AVDEmulator import AVDEmulator
from hooker_xp.device.PhysicalDevice import PhysicalDevice
from hooker_common import Logger
from hooker_xp.report.Reporter import Reporter


class Analysis(object):
    """The mother of any kind of analysis (manual, automated, ....)
    It provides usefull common methods to manage the emulators, create reports,
    reports events to optional databases...
    
    """

    def __init__(self, mainConfiguration, reportingConfiguration):        
        self._logger = Logger.getLogger(__name__)
        self.mainConfiguration = mainConfiguration
        self.reportingConfiguration = reportingConfiguration
        self.reporter = Reporter(self.reportingConfiguration)
        
    def _createReport(self, idXp, emulatorName, packageName, filename, typeAnalysis, descAnalysis):
        """Creates a new report to collect events produced while executing experiment IdXp"""
        if idXp is None:
            raise Exception("Cannot create a report if no IdXP is provided.")
        
        Analysis.createReport(self.reporter, idXp, emulatorName, packageName, filename, typeAnalysis, descAnalysis)

    @staticmethod
    def createReport(reporter, idXp, emulatorName, packageName, filename, typeAnalysis, descAnalysis):
        """Creates a new report to collect events produced while executing experiment IdXp"""
        if idXp is None:
            raise Exception("Cannot create a report if no IdXP is provided.")
        if reporter is None:
            raise Exception("Reporter is null.")

        # TODO: one day, authors will be stored ;)
        author = None

        # compute file sha1
        fileSha1 = Analysis._computeSha1(filename)

        reporter.createReport(idXp, emulatorName, author, packageName, filename, fileSha1, typeAnalysis, descAnalysis)


    @staticmethod
    def reportEvent(reporter, idXp, sourceEvent, actionEvent, paramsEvent=None):
        """Insert in the report a new event."""
        if reporter is None:
            raise Exception("Reporter is null.")

        reporter.reportEvent(idXp, sourceEvent, actionEvent, paramsEvent)
        

    def _generateIdXp(self, apkFiles):
        """Generates and returns the identifier of the experiment
        based on the provided list of apk following schema:
        md5("".join(sorted(apkFileNames))+currentDate)
        """
        return Analysis.generateIdXp(apkFiles)

    @staticmethod
    def generateIdXp(apkFiles):
        """Generates and returns the identifier of the experiment
        based on the provided list of apk following schema:
        md5("".join(sorted(apkFileNames))+currentDate)
        """
        logger = Logger.getLogger(__name__)
        apkNames = [os.path.basename(apkFile) for apkFile in apkFiles]
        strApkNames = ''.join(sorted(apkNames))
        logger.warning(strApkNames)
        
        currentDate = str(int(round(time.time() * 1000)))

        # builds an IDXP (md5(apkFile+currentDate))
        idXp = str(hashlib.md5(strApkNames+currentDate).hexdigest())

        logger.debug("ID Experiment: {0} (based on {1} and {2})".format(idXp, strApkNames, currentDate))
        
        return idXp

        
    @staticmethod
    def createEmulator(emulatorNumber, emulatorName, mainConfiguration, analysisType):
        """Creates a new emulator and returns it"""
        return Analysis.createDevice(emulatorNumber, emulatorName, mainConfiguration, None, analysisType)

        
    @staticmethod
    def createDevice(adbNumber, name, mainConfiguration, backupDirectory, analysisType):
        logger = Logger.getLogger(__name__)

        if adbNumber is None or int(adbNumber)<0:
            raise Exception("Cannot create a device with an invalid adb number, must be > 0")

        if name is None or len(name)==0:
            raise Exception("Cannot create a device if no name is provided.")
            
        logger.debug("Creation of new device: '{0}'.".format(name))
        
        if mainConfiguration.typeOfDevice=='real':
            return PhysicalDevice(adbNumber, name, mainConfiguration, backupDirectory, analysisType)
        else:
            return AVDEmulator(adbNumber, name, mainConfiguration, analysisType)

            
    def _writeConfigurationOnEmulator(self, emulator, idXP):
        """Creates a configuration for the current analysis
        and deploys it on the provided emulator."""
        Analysis.writeConfigurationOnEmulator(emulator, idXP, self.reportingConfiguration)

        
    @staticmethod
    def writeConfigurationOnEmulator(emulator, idXP, reportingConfiguration):
        logger = Logger.getLogger(__name__)
        configurationContent = """# Hooker Analysis Configuration File
# Network configuration
[elasticsearch]
elasticsearch_mode={0}
elasticsearch_nb_thread={1}
elasticsearch_ip={2}
elasticsearch_port={3}
elasticsearch_index={4}
elasticsearch_doctype={5}

# File configuration
[file]
file_mode={6}
file_name={7}

[analysis]
idXP={8}
""".format(reportingConfiguration.elasticsearchMode,
           1,
           "10.0.2.2",
           reportingConfiguration.elasticsearchPort,           
           reportingConfiguration.elasticsearchIndex,
           reportingConfiguration.elasticsearchDoctype,           
           reportingConfiguration.fileMode,
           "events.logs",
           idXP)
        logger.debug("Deploy the following configuration on emulator {0}: \n{1}".format(emulator.name, configurationContent))

        # Write on the emulator
        emulator.writeContentOnSdCard("experiment.conf", configurationContent)

    @staticmethod
    def _computeSha1(filepath):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
                            
    @property
    def mainConfiguration(self):
        """The main configuration
        """
        return self.__mainConfiguration

    @mainConfiguration.setter
    def mainConfiguration(self, configuration):
        if configuration is None:
            raise Exception("Main configuration cannot be None")

        self.__mainConfiguration = configuration

    @property
    def reportingConfiguration(self):
        """The reporting configuration
        """
        return self.__reportingConfiguration

    @reportingConfiguration.setter
    def reportingConfiguration(self, configuration):
        if configuration is None:
            raise Exception("Reporing configuration cannot be None")
        self.__reportingConfiguration = configuration

    @property
    def reporter(self):
        """The reporter
        """
        return self.__reporter

    @reporter.setter
    def reporter(self, reporter):
        self.__reporter = reporter
        
    @property
    def analysisType(self):
        return self.__analysisType
        
    @analysisType.setter
    def analysisType(self, analysisType):
        if analysisType == "manual":
            self.__analysisType = "manual"
        elif analysisType == "automatic":
            self.__analysisType = "automatic"
        else:
            raise Exception("Analysis type is either manual or automatic, not {}".format(analysisType))
            
