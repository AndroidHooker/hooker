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
import random
import shutil
import traceback

from multiprocessing import Pool, Manager, TimeoutError

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger
from hooker_xp.analysis.Analysis import Analysis
from hooker_xp.analysis.AutomaticAnalysisConfiguration import AutomaticAnalysisConfiguration
from hooker_xp.report.Reporter import Reporter
from hooker_xp.report.ReportingConfiguration import ReportingConfiguration
from hooker_xp.analysis.MainConfiguration import MainConfiguration
from hooker_xp.analysis.StaticAnalysis import StaticAnalysis
from hooker_xp.device.TelnetEmulation import TelnetEmulation

def executeExperiment(args):
    """
    Executes the analysis for an application.
    The analysis depends of the scenario the user as defined in configuration.
    """
    logger = Logger.getLogger(__name__)
    (listOfAPKs, iEmulator, mainConfiguration, analysisConfiguration, reportingConfiguration) = args
    reporter = Reporter(reportingConfiguration)
    
    logger.warning("Execute experiment with scenario: [{0}]".format(', '.join(analysisConfiguration.scenario)))

    # When you play with emulators, you can modify this variable to sleep a bit longer.
    # Default has to be >1
    SLEEP_FACTOR=1
    if mainConfiguration.typeOfDevice == 'emulated':
        SLEEP_FACTOR = 5
    if SLEEP_FACTOR < 1:
        raise Exception("SLEEP_FACTOR variable cannot be less than 1.")

    while True:
        # Pick one APK to analyse
        try:
            apkToAnalyze = listOfAPKs.get() # 0xFFFF
            logger.info("APK to analyze : {0}".format(apkToAnalyze))
            
            # Build the identifier experiment
            idXp = Analysis.generateIdXp([apkToAnalyze])

            # Build the emulator name
            if mainConfiguration.typeOfDevice=='emulated':
                emulatorName = "Emulator_{0}".format(iEmulator)
            else:
                emulatorName = mainConfiguration.deviceId

            # Create a new report for this analysis
            logger.debug("Create report.")
            Analysis.createReport(reporter, idXp, emulatorName, "unknown", apkToAnalyze, "automatic", mainConfiguration.name) 
        
            # Execute static analysis
            logger.debug("Executing the Static Analysis")
            staticAnalysis = StaticAnalysis(apkToAnalyze, mainConfiguration, reporter, idXp)
            staticAnalysis.execute()
            logger.info(staticAnalysis)

            # Create the emulator
            if mainConfiguration.typeOfDevice=='emulated':
                device = Analysis.createEmulator(iEmulator, emulatorName, mainConfiguration, analysisType="automatic")
            else:
                device = Analysis.createDevice(iEmulator, mainConfiguration.deviceId, mainConfiguration, analysisConfiguration.backupDirectory, analysisType="automatic")
            
            if device is None:
                raise Exception("Something has prevented the creation of an device.")

            # Starts the device
            Analysis.reportEvent(reporter, idXp, emulatorName, "Start device")
            device.start()

            # Install et execute preparation applications
            if mainConfiguration.typeOfDevice=='emulated':
                for prepareAPK in analysisConfiguration.prepareAPKs:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Install preparation APK", prepareAPK)
                    device.installAPK(prepareAPK)

                # Execute preparation applications
                for prepareAPK in analysisConfiguration.prepareAPKs:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Start activity", os.path.basename(prepareAPK)[:-4])
                    device.startActivity(os.path.basename(prepareAPK)[:-4])

            # Writes the experiment configuration on the device
            Analysis.reportEvent(reporter, idXp, emulatorName, "Write configuration file")
            Analysis.writeConfigurationOnEmulator(device, idXp, reportingConfiguration)

            if mainConfiguration.typeOfDevice=='emulated':
                sleepDuration = 30
                logger.debug("Waiting {0} seconds for the device to prepare...".format(sleepDuration))
                time.sleep(sleepDuration)

            # Install the targeted application
            Analysis.reportEvent(reporter, idXp, emulatorName, "Install target APK", apkToAnalyze)
            device.installAPK(apkToAnalyze)
            time.sleep(5*SLEEP_FACTOR/5)

            # We then follow the scenario user has filled in configuration
            for order in analysisConfiguration.scenario:
                if "execute" == order:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Launching main activity", staticAnalysis.mainActivity)
                    logger.info("Starting main activity: {0}".format(staticAnalysis.mainActivity))
                    device.startActivityFromPackage(staticAnalysis.packageName, staticAnalysis.mainActivity)
                    time.sleep(5*SLEEP_FACTOR)
                elif "stimulate" == order:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Stimulating package with monkey", staticAnalysis.packageName)
                    logger.info("Stimulating with monkey: {0}".format(staticAnalysis.packageName))
                    device.stimulateWithMonkey(staticAnalysis.packageName)
                    time.sleep(10*SLEEP_FACTOR)
                elif "externalStimulation" == order:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Stimulating phone with external conditions")
                    logger.info("Stimulating phone with external conditions...")
                    externalStimulation = TelnetEmulation(reporter, idXp, device)
                    externalStimulation.start()
                    time.sleep(10*SLEEP_FACTOR)
                elif "reboot" == order:
                    Analysis.reportEvent(reporter, idXp, emulatorName, "Rebooting device")
                    logger.info("Rebooting device.")
                    device.reboot()
                    time.sleep(5*SLEEP_FACTOR)

            Analysis.reportEvent(reporter, idXp, emulatorName, "Analysis has finished", apkToAnalyze)
            
            logger.info("Analysis of APK {0} has been finished.")
            Analysis.reportEvent(reporter, idXp, emulatorName, "Emulator closed")
            device.stop()

        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt caught\n")
            # Try to stop device if necessary
            if device is not None:
                device.stop()
            break
        except Exception, e:
            logger.error("Exception while executing an experiment : {0}".format(e))
            tb = traceback.format_exc()
            logger.error(tb)
            try:
                device.stop()
            except Exception:
                logger.error("Cannot stop the AVD, quitting experience.")
                break

    return True
    

class AutomaticAnalysis(Analysis):
    """
    Executes automatic analysis of Android applications.
    """

    def __init__(self, commandLineParser):
        super(AutomaticAnalysis, self).__init__(MainConfiguration.build(commandLineParser), ReportingConfiguration.build(commandLineParser))
        self._logger = Logger.getLogger(__name__)
        self.analysisConfiguration = self.__prepareAnalysis(commandLineParser)

    def test(self):
        device = Analysis.createDevice(0, self.mainConfiguration.deviceId, self.mainConfiguration, 
                                        self.analysisConfiguration.backupDirectory, analysisType="automatic")
        if device is None:
            raise Exception("Something has prevented the instanciation of the device.")

        # Starts the device
        device.start()
        #device.restoreSDCard()
        time.sleep(5)
        device.stop()
        exit()
        
    def start(self):
        """Starts an automatic analysis"""

        if self.mainConfiguration is None:
            raise Exception("The main configuration of the manual analysis has failed, cannot start it.")                    
        if self.reportingConfiguration is None:
            raise Exception("No reporting configuration found, cannot start the analysis.")
        if self.analysisConfiguration is None:
            raise Exception("The configuration of the manual analysis has failed, cannot start it.")

        self._logger.info(str(self))

        # For test purpose
        #self.test()
 
        if self.mainConfiguration.typeOfDevice=='emulated':
            # first step is to create templates if we have lots of emulators
            # We create one template for 4 devices
            # Attention: this has been commented in version 0.2 since it does not work properly.
            # You however may have to reimplement this if you want to run Hooker with a lot of AVD.
            #nb_templates = int(self.analysisConfiguration.maxNumberOfEmulators / 4)
            #for i in xrange(nb_templates):
            #    self._logger.debug("Create {} templates, one for each emulator".format(nb_templates))
            #    AVDEmulator.createTemplates(self.mainConfiguration, nb_templates)
       
            # Create a queue of threads
            distributedQueueManager = Manager()
            listOfAPKs = distributedQueueManager.Queue()

        # If we have a real device in automatic mode, we have to push backup to sdcard, and push TWRP script to /cache/recovery/
        # at each experiment. This is done in AVD logic.
        else: 
            # Create a queue of threads
            distributedQueueManager = Manager()
            listOfAPKs = distributedQueueManager.Queue()
            self.analysisConfiguration.maxNumberOfEmulators = 1
            
        pool = Pool(processes=self.analysisConfiguration.maxNumberOfEmulators)

        # Tell threads to analyze APKs which are push to the queue
        workerArgs = [(listOfAPKs, iEmulator, self.mainConfiguration, self.analysisConfiguration, self.reportingConfiguration) for iEmulator in range(self.analysisConfiguration.maxNumberOfEmulators)]

        try:
            r = pool.map_async(executeExperiment, workerArgs)
            # Continuously scan the directory and add identified APKs to ensure at least next emulators round is ready
            while True:
                if listOfAPKs.qsize() > self.analysisConfiguration.maxNumberOfEmulators*2:
                    #self._logger.debug("List of APK is superior to number of emulators")
                    #time.sleep(5)
                    try:
                        if r.get(5):
                            self._logger.info("Threads have returned, quitting")
                            break
                    except TimeoutError:
                        continue
                
                for directory in self.analysisConfiguration.apkFiles:
                    filenames = os.listdir(directory)

                    if len(filenames) == 0:
                        self._logger.debug("All APKs have been pushed to the analyzing queue, sleeping 5 secs...")
                        #time.sleep(5)
                        try:
                            if r.get(5):
                                self._logger.info("Threads have returned, quitting")
                                break
                        except TimeoutError:
                            continue
                    else:
                        apkFileName = random.choice(filenames)
                        apkFileInputPath = os.path.join(directory, apkFileName)

                        if not os.access(apkFileInputPath, os.R_OK):
                            self._logger.error("You don't have read access to file {0}, not pushing file to queue.".format(apkFileInputPath))
                            continue

                        # compute Sha1 and name the file with it
                        sha1 = self._computeSha1(apkFileInputPath)
                        apkFileOutputPath = os.path.join(self.analysisConfiguration.outputDirectory, sha1+".apk")

                        # move APK to output dir
                        shutil.move(apkFileInputPath, apkFileOutputPath)
                        self._logger.info("Pushing APK {0} in queue.".format(apkFileOutputPath))
                        listOfAPKs.put(apkFileOutputPath)
        except KeyboardInterrupt:
            self._logger.error("Automatic analysis interrupted by a keyboard Exception.\n")
        except Exception, e:
            self._logger.error(e)
            
    def __prepareAnalysis(self, commandLineParser):
        """Configures the class attributed through
        parameters stored in the command line parser.
        Returns the configuration
        """

        if commandLineParser is None:
            raise Exception("Cannot build the analysis configuration if no commandLineParser is provided")

        analysisOptions = commandLineParser.automaticOptions
        
        if not 'apks' in analysisOptions.keys():
            raise Exception("The apks configuration entry is missing.")

        apkFiles = []
        for apkFile in analysisOptions['apks'].split(","):
            if apkFile is not None and len(apkFile)>0:
                if not os.path.isdir(apkFile):
                    raise Exception("'{0}' is not a directory, you must provide one in automatic mode.".format(apkFile))
                if not os.access(apkFile, os.R_OK):
                    raise Exception("You don't have read access to directory {0}.".format(apkFile))
                apkFiles.append(apkFile)

        if len(apkFiles)==0:
            raise Exception("At least one directory must be provided in the 'apks' configuration parameter.")
            

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
                    prepareAPKs.append(prepareAPK)

        scenario = []
        if 'scenario' not in analysisOptions.keys():
            raise Exception("The configuration of an automatic analysis must include the definition of the 'scenario' parameter")
        for order in analysisOptions['scenario'].split(","):
            if order is not None and len(order)>0:
                if 'execute' == order or 'stimulate' == order or 'reboot' == order or 'externalStimulation' == order:
                    if 'stimulate' == order:
                        # Check that previous order is an execute
                        if scenario[-1] != 'execute':
                            raise Exception("Scenario issue: you must have an \'execute\' before a \'stimulate\'.")
                    scenario.append(order)
                else:
                    raise Exception("Order {0} is not valid.".format(order))
        
        if len(scenario)==0:
            raise Exception("At least one valid order must be provided in the 'scenario' configuration parameter.")

        outputDirectory = None
        if 'outputdirectory' in analysisOptions.keys():
            outputDirectory = analysisOptions['outputdirectory']
            if not os.path.isdir(outputDirectory):
                raise Exception("{0} is not a valid directory, you must provide one in automatic mode.".format(outputDirectory))
            if not os.access(outputDirectory, os.W_OK):
                raise Exception("You don't have write access to directory {0}.".format(outputDirectory))

        backupDirectory = None
        if 'backupdirectory' in analysisOptions.keys():
            backupDirectory = analysisOptions['backupdirectory']
            if not os.path.isdir(backupDirectory):
                raise Exception("{0} is not a valid directory, you must provide one in automatic mode.".format(backupDirectory))
            if not os.access(backupDirectory, os.R_OK):
                raise Exception("You don't have read access to directory {0}.".format(backupDirectory))

        self._logger.debug("Configure the automatic analysis.")
        analysis = AutomaticAnalysisConfiguration(apkFiles, prepareAPKs, scenario, outputDirectory, 
                    maxNumberOfEmulators=maxNumberOfEmulators, backupDirectory=backupDirectory)

        return analysis

    def __str__(self):
        """toString method"""
        lines = [
            "Automatic Analysis",
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
