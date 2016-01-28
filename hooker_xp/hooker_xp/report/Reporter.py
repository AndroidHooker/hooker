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
import uuid

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger
from hooker_common.elasticsearch.Es import Es
from hooker_common.elasticsearch.EsInterrogator import EsInterrogator

from hooker_common.APK import APK


class Reporter(object):
    """
    Ensures the creation of an experiment report following
    the configuration provided by user on startup.
    """

    def __init__(self, reportingConfiguration):
        self._logger = Logger.getLogger(__name__)
        self.reportingConfiguration = reportingConfiguration
        self.__initializeReporters()
        if self.reportingConfiguration.elasticsearchMode:
            self.esInterrogator = EsInterrogator(self.es)

    def createReport(self, idXp, emulatorName, author, packageName, filename, filesha1, typeAnalysis, descAnalysis):
        """Creates a new report to collect events produced while executing experiment IdXp"""
        if idXp is None:
            raise Exception("Cannot create a report if no IdXP is provided.")

        if packageName is not None:
            self.__packageName = packageName

        # Checks if we have an APK associated with IDXP in ES
        if self.es is not None:
            if self.esInterrogator is not None:
                try:
                    self.esInterrogator.getAPKInXP(idXp)
                    self._logger.info("APK found associated with IDXP {0}, continuing".format(idXp))
                except Exception:
                    self._logger.info("No APK found associated with IDXP {0}".format(idXp))
                    apkid = str(uuid.uuid4())
                    apk = APK(apkid, filename, filename, "no-market/"+filename)
                    if apk is not None:
                        self.es.insertAPK(apk, "no-market")
                        self._logger.info("APK {0} with ID {1} has been assiocated to IDXP in ES cluster".format(filename, apkid))
                    else:
                        self._logger.error("APK has not been instanciated")
                   

        # Create a new experiment in the ES
        if self.es is not None:
            self.es.insertNewExperiment(idXp, emulatorName, author, packageName, filename, filesha1, typeAnalysis, descAnalysis)        

    def reportEvent(self, idXp, sourceEvent, actionEvent, paramsEvent=None):
        """Insert in the report a new event."""
        
        if idXp is None:
            raise Exception("Cannot create a report if no IdXP is provided.")

        if self.es is not None:
            relTime = 0 # TODO
            # Example: reportEvent(idXp, "Emulator", "Write configuration file")
            self.es.insertExperimentSteps(idXp, relTime, emulator=sourceEvent, description=actionEvent)

    def reportStaticEvent(self, idXp, filename, packageName, androidVersionName, androidVersionCode, minSDKVersion, maxSDKVersion, mainActivity, activities, providers, libraries, services, receivers, permissions):
        """Insert in the report a new static event."""
        
        if idXp is None:
            raise Exception("Cannot create a report if no idXp is provided.")

        if self.es is not None:
            self.es.insertStaticEventInformationOnAPK(idXp, filename, packageName, androidVersionName, androidVersionCode, minSDKVersion, maxSDKVersion, mainActivity, activities, providers, libraries, services, receivers, permissions)

    def __initializeReporters(self):
        """Initialize the ES and/or the file report if requested"""
        if self.reportingConfiguration is None:
            raise Exception("Cannot initialize the reporters as no reporting Configuration exists")

        # Initialize ES (if requested)
        if self.reportingConfiguration.elasticsearchMode:
            self._logger.debug("Initialize the Elasticsearch reporter")
            self.es = Es([{"host":self.reportingConfiguration.elasticsearchIp, 'port':self.reportingConfiguration.elasticsearchPort}])
        else:
            self.es = None
        
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
    def es(self):
        """The elasticsearch access
        """
        return self.__es

    @es.setter
    def es(self, es):
        self.__es = es
