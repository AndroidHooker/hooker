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
import time
import traceback

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger
from hooker_xp.analysis.Analysis import Analysis
from hooker_xp.analysis.ManualAnalysisConfiguration import ManualAnalysisConfiguration
from hooker_xp.report.ReportingConfiguration import ReportingConfiguration
from hooker_xp.analysis.MainConfiguration import MainConfiguration
from hooker_xp.analysis.StaticAnalysis import StaticAnalysis


class ManualAnalysis(Analysis):
    """Executes a single analysis of an Android application.
    The user will be prompted to stimulate the application once the
    android emulator is started. The analysis stops when the emulator is closed by the user. A report is then returned.
    """

    def __init__(self, commandLineParser):
        super(ManualAnalysis, self).__init__(MainConfiguration.build(commandLineParser), ReportingConfiguration.build(commandLineParser), )
        self._logger = Logger.getLogger(__name__)
        self.analysisConfiguration = self.__prepareAnalysis(commandLineParser)
        
    def start(self):
        """Starts a manual analysis"""

        if self.mainConfiguration is None:
            raise Exception("No main configuration found, cannot start the analysis..")
        if self.reportingConfiguration is None:
            raise Exception("No reporting configuration found, cannot start the analysis.")
        if self.analysisConfiguration is None:
            raise Exception("No analysis configuration found, cannot start the analysis.")

        self._logger.info(str(self))

        # Build the identifier experiment
        idXp = self._generateIdXp(self.analysisConfiguration.apkFiles)

        # Targeted APK
        analyzedAPKFile = self.analysisConfiguration.apkFiles[0]
        
        # Execute the analysis on the first emulator
        iEmulator = 0
        emulatorName = "Emulator_{0}".format(iEmulator)
        
        # Create a new report for this analysis
        Analysis.createReport(self.reporter, idXp, emulatorName, "unknown", analyzedAPKFile, "manual", self.mainConfiguration.name)

        # Execute static analysis
        staticAnalysis = StaticAnalysis(analyzedAPKFile, self.mainConfiguration, self.reporter, idXp)

        Analysis.reportEvent(self.reporter, idXp, "Analysis", "Executing static analysis on {0}".format(analyzedAPKFile))        
        staticAnalysis.execute()
        self._logger.info(staticAnalysis)
        
        if self.mainConfiguration.typeOfDevice=='emulated':
            device = Analysis.createEmulator(iEmulator, emulatorName, self.mainConfiguration, analysisType="manual")
        else:
            device = Analysis.createDevice(iEmulator, self.mainConfiguration.deviceId, self.mainConfiguration, self.analysisConfiguration.backupDirectory, analysisType="manual")

        if device is None:
            raise Exception("Something has prevented the creation of the device.")

        # Starts the device
        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Start device")
        try:
            device.start()
        except: 
            self._logger.error(traceback.format_exc())
            device.stop()
            return

        # Install preparation applications
        # A real device do not need preparation applications
        if self.mainConfiguration.typeOfDevice=='emulated':
            for prepareAPK in self.analysisConfiguration.prepareAPKs:
                Analysis.reportEvent(self.reporter, idXp, emulatorName, "Install preparation APK", prepareAPK)
                device.installAPK(prepareAPK)

            # Execute preparation applications
            for prepareAPK in self.analysisConfiguration.prepareAPKs:
                Analysis.reportEvent(self.reporter, idXp, emulatorName, "Start activity", os.path.basename(prepareAPK)[:-4])
                device.startActivity(os.path.basename(prepareAPK)[:-4])
        else:
            self._logger.debug("Continuing...")

        # Writes the experiment configuration on the device
        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Write configuration file")
        self._writeConfigurationOnEmulator(device, idXp)

        if self.mainConfiguration.typeOfDevice=='emulated':
            sleepDuration = 30
            self._logger.debug("Waiting {0} seconds for the device to prepare...".format(sleepDuration))
            time.sleep(sleepDuration)
        
        # Install the targeted application
        for analysisAPK in self.analysisConfiguration.apkFiles:
            Analysis.reportEvent(self.reporter, idXp, emulatorName, "Install target APK", analysisAPK)
            device.installAPK(analysisAPK)

        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Launching main activity", staticAnalysis.mainActivity)
        self._logger.info("Starting main activity: {0}".format(staticAnalysis.mainActivity))
        device.startActivityFromPackage(staticAnalysis.packageName, staticAnalysis.mainActivity)

        # The user is now requested to perform any operations he wants
        # this script waits for the device process to be closed
        self._logger.info("Proceed to the stimulation of the environnment.")
        self._logger.info("Once achieved, close the device and waits for the hooker to finish.")
        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Wait for emulator to be closed")
        
        device.waitToBeClosed()
        if self.mainConfiguration.typeOfDevice=='real':
            device.stop(True)
        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Analysis has finished")
        Analysis.reportEvent(self.reporter, idXp, emulatorName, "Emulator closed")
        self._logger.info("Device has finished, IDXP is {0}".format(idXp))
        

    def __prepareAnalysis(self, commandLineParser):
        """Configures the class attributed through
        parameters stored in the command line parser.
        Returns the configuration
        """

        if commandLineParser is None:
            raise Exception("Cannot build the analysis configuration if no commandLineParser is provided")

        analysisOptions = commandLineParser.manualOptions

        if not 'apks' in analysisOptions.keys():
            raise Exception("The apks configuration entry is missing.")

        apkFiles = []
        for apkFile in analysisOptions['apks'].split(","):
            if apkFile is not None and len(apkFile)>0:
                # check the apk exists and is readable
                if not os.path.isfile(apkFile):
                    raise Exception("The apkFile {0} is not a file, we cannot prepare the analysis.".format(apkFile))
                if not os.access(apkFile, os.R_OK):
                    raise Exception("The apkFile {0} cannot be read, check the permissions.".format(apkFile))
                apkFiles.append(apkFile)

        maxNumberOfEmulators = 1
        if 'maxnumberofemulators' in analysisOptions.keys():
            try:
                maxNumberOfEmulators = int(analysisOptions['maxnumberofemulators'])
            except:
                raise Exception("'MaxNumberOfEmulators' in the configuration must be an interger.")            

        prepareAPKs = []
        if 'prepareapks' in analysisOptions.keys():
            for prepareAPK in analysisOptions['prepareapks'].split(","):
                if prepareAPK is not None and len(prepareAPK)>0:
                    # check the apk exists and is readable
                    if not os.path.isfile(prepareAPK):
                        raise Exception("The prepareAPK {0} is not a file, we cannot prepare the analysis.".format(prepareAPK))
                    if not os.access(prepareAPK, os.R_OK):
                        raise Exception("The prepareAPK {0} cannot be read, check the permissions.".format(prepareAPK))
                    prepareAPKs.append(prepareAPK)

        backupDirectory = None
        if 'backupdirectory' in analysisOptions.keys():
            backupDirectory = analysisOptions['backupdirectory']
            if not os.path.isdir(backupDirectory):
                raise Exception("{0} is not a valid directory, you must provide one in automatic mode.".format(backupDirectory))
            if not os.access(backupDirectory, os.R_OK):
                raise Exception("You don't have read access to directory {0}.".format(backupDirectory))
                    
        self._logger.debug("Configure the manual analysis.")
        analysis = ManualAnalysisConfiguration(apkFiles, maxNumberOfEmulators=maxNumberOfEmulators, prepareAPKs=prepareAPKs, backupDirectory=backupDirectory)

        return analysis

    def __str__(self):
        """toString method"""
        lines = [
            "---------------",
            "Manual Analysis",
            "---------------",
            str(self.mainConfiguration),
            str(self.analysisConfiguration),
            str(self.reportingConfiguration),
            "---------------"
        ]
        return '\n'.join(lines) 
        
    @property
    def analysisConfiguration(self):
        """The configuration of the analysis
        """
        return self.__analysisConfiguration

    @analysisConfiguration.setter
    def analysisConfiguration(self, configuration):
        self.__analysisConfiguration = configuration
