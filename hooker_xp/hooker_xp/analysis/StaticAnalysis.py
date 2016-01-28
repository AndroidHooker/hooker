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
import sys
import os
import time

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger


class StaticAnalysis(object):
    """
    Static analysis of Android applications.
    """

    def __init__(self, apkToAnalyze, mainConfiguration, reporter, idXp):
        self._logger = Logger.getLogger(__name__)
        self.apkToAnalyze = os.path.abspath(apkToAnalyze)
        self.androguardPath = mainConfiguration.androguardPath
        self.reporter = reporter
        self.idXp = idXp

    def execute(self):
        """ 
        Executes the static analysis of APK using the androguard framework.
        First parses the APK the get corresponding python object.
        Then calls the androguard methods on the built object.
        """
        sys.path.append(self.androguardPath)
        from androguard.core.bytecodes import apk

        self._logger.info("Analyzing {0} with androguard...".format(self.apkToAnalyze))
        
        # Parse APK
        parsedAPK = apk.APK(self.apkToAnalyze)
        if parsedAPK is None:
            raise Exception("Parsed APK is null, quitting StaticAnalysis.")

        # Info: setters are dealing with None returns
        try:
            self.androidVersionCode = parsedAPK.get_androidversion_code()
            self.androidVersionName = parsedAPK.get_androidversion_name()
            self.mainActivity = parsedAPK.get_main_activity()
            self.maxSDKVersion = parsedAPK.get_max_sdk_version()
            if self.maxSDKVersion == "n/c":
                self.maxSDKVersion = -1
                
            self.minSDKVersion = parsedAPK.get_min_sdk_version()
            if self.minSDKVersion == "n/c":
                self.minSDKVersion = -1
                
            self.packageName = parsedAPK.get_package()
            self.timestamp = str(int(round(time.time() * 1000)))
            self.activities = parsedAPK.get_activities()
            self.permissions = parsedAPK.get_permissions()
            self.providers = parsedAPK.get_providers()
            self.receivers = parsedAPK.get_receivers()
            self.services = parsedAPK.get_services()
            self.libraries = parsedAPK.get_libraries()
        except Exception,e:
            self._logger.warn("An error occured while executing the static analysis of APK {0}: {1}".format(self.apkToAnalyze, e))

        self.__saveResultsInESCluster()            

    def __saveResultsInESCluster(self):
        """
        Saves result of the analysis into ES cluster.
        """
        self.reporter.reportStaticEvent(self.idXp, self.apkToAnalyze, self.packageName, self.androidVersionName, self.androidVersionCode, self.minSDKVersion, self.maxSDKVersion, self.mainActivity, self.activities, self.providers, self.libraries, self.services, self.receivers, self.permissions)        

    def __str__(self):
        """toString method"""
        lines = [
            "Static Analysis results:",
            "\t- APK:\t\t{0}".format(self.apkToAnalyze),
            "\t- Version code:\t{0}".format(self.androidVersionCode),
            "\t- Version name:\t{0}".format(self.androidVersionName),
            "\t- Main act.:\t{0}".format(self.mainActivity),
            "\t- Max SDK:\t{0}".format(self.maxSDKVersion),
            "\t- Min SDK:\t{0}".format(self.minSDKVersion),
            "\t- Package name:\t{0}".format(self.packageName),
            "\t- Timestamp:\t{0}".format(self.timestamp),
            "\t- Activities:\t[{0}]".format(', '.join(self.activities)),
            "\t- Permissions:\t[{0}]".format(', '.join(self.permissions)),
            "\t- Providers:\t[{0}]".format(', '.join(self.providers)),
            "\t- Receivers:\t[{0}]".format(', '.join(self.receivers)),
            "\t- Services:\t[{0}]".format(', '.join(self.services)),
            "\t- Libraries:\t[{0}]".format(', '.join(self.libraries)),
        ]
        return '\n'.join(lines)

    @property
    def androguardPath(self):
        """Path to androguard framework"""
        return self.__androguardPath

    @androguardPath.setter
    def androguardPath(self, androguardPath):
        if androguardPath is None:
            raise Exception("Androguard path must be provided.")
        self.__androguardPath = androguardPath

    @property
    def apkToAnalyze(self):
        """The application to analyze"""
        return self.__apkToAnalyze

    @apkToAnalyze.setter
    def apkToAnalyze(self, apk):
        if apk is None:
            raise Exception("You must provide an APK to analyze")
        self.__apkToAnalyze = apk

    @property
    def activities(self):
        """Activities of application"""
        return self.__activities

    @activities.setter
    def activities(self, activities):
        self.__activities = []
        for act in activities:
            if not act is None:
                self.__activities.append(act)
        
    @property
    def androidVersionCode(self):
        """Android version code"""
        return self.__androidVersionCode

    @androidVersionCode.setter
    def androidVersionCode(self, versionCode):
        if versionCode is None:
            self.__androidVersionCode = "n/c"
        else:
            self.__androidVersionCode = versionCode

    @property 
    def androidVersionName(self):
        """Android version name"""
        return self.__androidVersionName

    @androidVersionName.setter
    def androidVersionName(self, androidVersionName):
        if androidVersionName is None:
            self.__androidVersionName = "n/c"
        else:
            self.__androidVersionName = androidVersionName

    @property
    def mainActivity(self):
        """Main activity of APK"""
        return self.__mainActivity

    @mainActivity.setter
    def mainActivity(self, mainActivity):
        if mainActivity is None:
            self.__mainActivity = "n/c"
        else:
            self.__mainActivity = mainActivity

    @property
    def maxSDKVersion(self):
        """Maximum SDK version"""
        return self.__maxSDKVersion

    @maxSDKVersion.setter
    def maxSDKVersion(self, maxSDKVersion):
        if maxSDKVersion is None: 
            self.__maxSDKVersion = "n/c"
        else:
            self.__maxSDKVersion = maxSDKVersion

    @property
    def minSDKVersion(self):
        """Minimum SDK version"""
        return self.__minSDKVersion

    @minSDKVersion.setter
    def minSDKVersion(self, minSDKVersion):
        if minSDKVersion is None:
            self.__minSDKVersion = "n/c"
        else:
            self.__minSDKVersion = minSDKVersion

    @property
    def packageName(self):
        """Package name of APK"""
        return self.__packageName

    @packageName.setter
    def packageName(self, packageName):
        if packageName is None: 
            self.__packageName = "n/c"
        else:
            self.__packageName = packageName

    @property
    def permissions(self):
        """List of permissions asked by the APK"""
        return self.__permissions

    @permissions.setter
    def permissions(self, permissions):
        self.__permissions = []
        for perm in permissions:
            if not permissions is None:
                self.__permissions.append(perm)

    @property
    def providers(self):
        """List of providers of the APK"""
        return self.__providers
    
    @providers.setter
    def providers(self, providers):
        self.__providers = []
        for prov in providers:
            if not prov is None:
                self.__providers.append(prov)

    @property
    def receivers(self):
        """List of receivers declared by the APK"""
        return self.__receivers
    
    @receivers.setter
    def receivers(self, receivers):
        self.__receivers = []
        for rec in receivers:
            if not rec is None:
                self.__receivers.append(rec)

    @property
    def services(self):
        """List of services"""
        return self.__services
    
    @services.setter
    def services(self, services):
        self.__services = []
        for serv in services:
            if not serv is None:
                self.__services.append(serv)

    @property
    def libraries(self):
        """List of native libraries"""
        return self.__libraries

    @libraries.setter
    def libraries(self, libraries):
        self.__libraries = []
        for lib in libraries:
            if not lib is None:
                self.__libraries.append(lib)

    @property
    def timestamp(self):
        """Timestamp of the static analysis"""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if timestamp is None:
            self.__timestamp = "n/c"
        else:
            self.__timestamp = timestamp

    @property
    def reporter(self):
        """Reporter of the static analysis"""
        return self.__reporter

    @reporter.setter
    def reporter(self, reporter):
        if reporter is None:
            raise Exception("A reporter must be provided")
        self.__reporter = reporter

    @property
    def idXp(self):
        """IdXp of the experiment"""
        return self.__idXp

    @idXp.setter
    def idXp(self, idXp):
        if idXp is None:
            raise Exception("An idXp must be provided")
        self.__idXp = idXp



