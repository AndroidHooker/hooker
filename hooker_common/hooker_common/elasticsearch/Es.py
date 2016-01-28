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
from elasticsearch import Elasticsearch
import time

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger


class Es(object):
    """This class allows to insert and fetch required information
    to build an experimentation report in an elasticsearch cluster.
    """

    # Name of the hooker index in the Es cluster
    ES_INDEX_NAME_HOOKER = "hooker_test"
    ES_DOCTYPE_EXPERIMENT_HOOKER = "experiment"
    ES_DOCTYPE_PYTHON_HOOKER = "python"
    ES_DOCTYPE_STATIC_HOOKER = "static"
    ES_DOCTYPE_EVENT_HOOKER = "event"
    ES_DOCTYPE_APK_HOOKER = "apk"    
    

    def __init__(self, esNodes):
        """Creates and initializes the connection to the specified elasticsearch cluster.
        The esNodes attributes refers to a list of nodes we should connect to."""
        
        self._logger = Logger.getLogger(__name__)
        self.esNodes = esNodes
        self.__initializeConnection()
        

    def insertNewExperiment(self, idXp, emulator, author, packageName, filename, filesha1, analysis, description=None):
        """Inserts in ES Cluster the new specified experiment."""

        acceptedAnalysisValues = ["automatic", "manual"]

        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if emulator is None or len(emulator) == 0:
            raise Exception("Emulator cannot be null.")
        if author is None or len(author) == 0:
            author = "Unknown"
        if packageName is None or len(packageName) == 0:
            raise Exception("PackageName cannot be null.")
        if filename is None or len(filename) == 0:
            raise Exception("Filename cannot be null.")
        if filesha1 is None or len(filesha1) == 0:
            raise Exception("Filesha1 cannot be null.")
        if analysis is None or analysis not in acceptedAnalysisValues:
            raise Exception("Analysis cannot be null and should take its value in '{0}'".format(acceptedAnalysisValues))
        
        if self.esInstance is None:
            raise Exception("Cannot insert new experiment since no ES cluster available.")

        # checks if the experiment already exists
        if self.isExperimentExists(idXp):
            raise Exception("Experiment with ID '{0}' already exists, cannot duplicate it.".format(idXp))

        currentDate = int(round(time.time() * 1000))
        
        createBody = {
            "IDXP": idXp,
            "PackageName": packageName,        
            "Analyzed": False,
            "Filename": filename,
            "Filesha1": filesha1,
            "Timestamp": currentDate,
            "RelativeTimestamp": 0,
            "Emulator": emulator,
            "Author": author,
            "Description": description
        }
            
        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_EXPERIMENT_HOOKER, body=createBody)
        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this experiment.")
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this experiment.")

        self._logger.debug("The experiment '{0}' has successfuly been inserted into ES cluster.".format(idXp))
        
        
    def insertExperimentSteps(self, idXp, relTime, emulator, description):
        """Inserts in ES Cluster the new specified experiment."""

        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if emulator is None or len(emulator) == 0:
            raise Exception("Emulator cannot be null.")
        if description is None or len(description) == 0:
            raise Exception("Description cannot be null.")
            
        if self.esInstance is None:
            raise Exception("Cannot insert new experiment since no ES cluster available.")

        # checks if the experiment exists
        if not self.isExperimentExists(idXp):
            raise Exception("Experiment with ID '{0}' doesn't exists, create it before inserting a static event.".format(idXp))
            
        currentDate = int(round(time.time() * 1000))
        
        createBody = {
            "Timestamp": currentDate,
            "RelativeTimestamp": relTime,
            "Emulator": emulator,
            "Description": description
        }
            
        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_PYTHON_HOOKER, body=createBody, parent=idXp)
        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this experiment.")
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this experiment.")

        self._logger.debug("The experiment '{0}' has successfuly been inserted into ES cluster.".format(idXp))
        

    def insertStaticInformationOnAPK(self, idXp, filename, filesha1, packageName, androidVersionCode, androidVersionName, minSDKVersion, maxSDKVersion, mainActivity, activities, providers, libraries, services, receivers, permissions):
        """Inserts into the current ES cluster, the provided static information about an APK"""

        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if packageName is None or len(packageName) == 0:
            raise Exception("PackageName cannot be null.")
        if filename is None or len(filename) == 0:
            raise Exception("Filename cannot be null.")
        if filesha1 is None or len(filesha1) == 0:
            raise Exception("Filesha1 cannot be null.")

        if self.esInstance is None:
            raise Exception("Cannot insert new experiment since no ES cluster available.")

        # checks if the experiment exists
        if not self.isExperimentExists(idXp):
            raise Exception("Experiment with ID '{0}' doesn't exists, create it before inserting a static event.".format(idXp))

        currentDate = int(round(time.time() * 1000))

        createBody = {
            "Timestamp": currentDate,
            "Filename": filename,
            "Filesha1": filesha1,
            "PackageName": packageName,
            "Android Version Code": androidVersionCode,
            "Android Version Name": androidVersionName,
            "Min SDK Version": minSDKVersion,
            "Max SDK Version": maxSDKVersion,
            "Main Activity": mainActivity,
            "Activities": activities,
            "Providers": providers,
            "Libraries": libraries,
            "Services": services,
            "Receivers": services,
            "Permissions": permissions
        }

        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_STATIC_HOOKER, body=createBody, parent=idXp)
        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this static information.")
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this static information.")

        self._logger.debug("The static information of experiment '{0}' has successfuly been inserted into ES cluster.".format(idXp))

    def insertEventInformationOnAPK(self, idXp, relTime, hookerName, packageName, className, methodName, params=None):
        """Inserts into the current ES cluster, the provided static information about an APK"""

        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if packageName is None or len(packageName) == 0:
            raise Exception("PackageName cannot be null.")
        if hookerName is None or len(hookerName) == 0:
            raise Exception("HookerName cannot be null.")

        if self.esInstance is None:
            raise Exception("Cannot insert new experiment since no ES cluster available.")

        # checks if the experiment exists
        if not self.isExperimentExists(idXp):
            raise Exception("Experiment with ID '{0}' doesn't exists, create it before inserting an event.".format(idXp))

        currentDate = int(round(time.time() * 1000))

        createBody = {
            "Timestamp": currentDate,
            "RelativeTimestamp": relTime,
            "HookerName": hookerName,
            "IntrusiveLevel": 0,
            "PackageName": packageName,
            "ClassName": className,
            "MethodName": methodName,
            "Parameters": params,
            "Return": None,
            "Data": None
        }

        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_EVENT_HOOKER, body=createBody, parent=idXp)

        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this event information.")            
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this event information.")            

        self._logger.debug("The event information of experiment '{0}' has successfuly been inserted into ES cluster.".format(idXp))

    def insertStaticEventInformationOnAPK(self, idXp, filename, packageName, androidVersionName, androidVersionCode, minSDKVersion, maxSDKVersion, mainActivity, activities, providers, libraries, services, receivers, permissions):
        """Inserts into the current ES cluster, the provided static information about an APK"""

        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if packageName is None or len(packageName) == 0:
            raise Exception("PackageName cannot be null.")
        if filename is None or len(filename) == 0:
            raise Exception("Filename cannot be null.")

        if self.esInstance is None:
            raise Exception("Cannot insert new experiment since no ES cluster available.")

        # checks if the experiment exists
        if not self.isExperimentExists(idXp):
            raise Exception("Experiment with ID '{0}' doesn't exists, create it before inserting a static event.".format(idXp))

        currentDate = int(round(time.time() * 1000))

        json_activities = []
        for activity in activities:
            json_activities.append({"Activity":activity})

        json_providers = []
        for provider in providers:
            json_providers.append({"Provider":provider})

        json_libraries = []
        for library in libraries:
            json_libraries.append({"Library":library})

        json_services = []
        for service in services:
            json_services.append({"Service":service})

        json_receivers = []
        for receiver in receivers:
            json_receivers.append({"Receiver":receiver})
            
        json_permissions = []
        for permission in permissions:
            json_permissions.append({"Permission":permission})

        createBody = {
            "Timestamp": currentDate,
            "Filename": filename,
            "PackageName": packageName,
            "Android Version Code": androidVersionCode,
            "Android Version Name": androidVersionName,
            "Min SDK Version": minSDKVersion,
            "Max SDK Version": maxSDKVersion,
            "Main Activity": mainActivity,
            "Activities": json_activities,
            "Providers": json_providers,
            "Libraries": json_libraries,
            "Services": json_services,
            "Receivers": json_receivers,
            "Permissions": json_permissions
        }
        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_STATIC_HOOKER, body=createBody, parent=idXp)
        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this static event information.")
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this static event information.")

        self._logger.debug("The static event information of experiment '{0}' has successfuly been inserted into ES cluster.".format(idXp))
        

    def insertAPK(self, apk, marketName):
        """Inserts into the current ES cluster, the provided APK with its market name"""

        if apk is None:
            raise Exception("APK cannot be null")

        if self.esInstance is None:
            raise Exception("Cannot insert new APK since no ES cluster available.")

        currentDate = int(round(time.time() * 1000))
        
        createBody = {
            "IDAPK": apk.APKID,            
            "Timestamp": currentDate,
            "Filename": apk.filename,
            "Filesha1": apk.sha1,
            "Name": apk.name,
            "Url": apk.url,
            "Version": apk.version,
            "Market": marketName,            
            "Author": apk.author,
            "Category": apk.category,
            "Description": apk.description,
            "Filesize": int(apk.filesize)
        }
        result = self.esInstance.create(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_APK_HOOKER, body=createBody)

        if result is None:
            raise Exception("The ES cluster did not accept our data.")                    
        elif "created" in result.keys():
            if not result["created"]:
                raise Exception("The ES cluster did not accept the creation of this event information.")                
        elif "ok" in result.keys():
            if not result["ok"]:
                raise Exception("The ES cluster did not accept the creation of this event information.")                                

        self._logger.debug("The APK '{0}' has successfuly been inserted into ES cluster.".format(apk.name))

    def deleteAPK(self, apk):
        """Delete from the current ES cluster, the provided APK"""

        if apk is None:
            raise Exception("APK cannot be null")

        if self.esInstance is None:
            raise Exception("Cannot delete APK since no ES cluster available.")

        result = self.esInstance.delete(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_APK_HOOKER, id=apk.IDAPK)
            
        if result is None:
            raise Exception("The ES cluster did not accept our request.")

        if not "found" in result.keys():
            self._logger.debug(result)
            raise Exception("An error occured while executing the request.")
        if not result["found"]:
            self._logger.debug(result)
            raise Exception("No apk deleted.")
            
        self._logger.debug("The APK '{0}' has successfuly been removed from ES cluster.".format(apk.Name))

    def isExperimentExists(self, idXp):
        """Checks if an experiment with the specified idXp is already registered in Es"""
        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if self.esInstance is None:
            raise Exception("Cannot checks if experiment exists since no ES cluster available.")

        return self.esInstance.exists(index=Es.ES_INDEX_NAME_HOOKER, doc_type=Es.ES_DOCTYPE_EXPERIMENT_HOOKER, id=idXp)

    
    def __initializeConnection(self):
        """Initialize the connection to the self.nodes attributes. It creates, if required the
        document structure."""
        self._logger.debug("Initializes connection with the elasticsearch database.")
        try:
            self.esInstance = Elasticsearch(self.esNodes)
        except Exception,e:
            raise Exception("Cannot connect to the elasticsearch cluster '{0}': {1}".format(self.esNodes, e))

        # Check connectivity
        if self.esInstance is None or not self.esInstance.ping():
            raise Exception("Cluster is not reachable.")
        else:
            self._logger.debug("Cluster seems to be reachable.")

        # Checks required index exist and creates it if not
        if not self.__isHookerIndexExists():
            self._logger.warning("Hooker index '{0}' in elasticsearch doesn't seem to exist.".format(Es.ES_INDEX_NAME_HOOKER))
            self.__createHookerIndex()

    def __isHookerIndexExists(self):
        """Checks if the index in the current ES cluster exists"""
        if self.esInstance is None:
            raise Exception("No current instance of the cluster exists.")

        esIndices = self.esInstance.indices
        esIndices.clear_cache()
        
        return esIndices.exists(index=[Es.ES_INDEX_NAME_HOOKER])

    def __createHookerIndex(self):
        """Creates the hooker index in current ES cluster"""
        if self.esInstance is None:
            raise Exception("No current instance of the cluster exists.")
        if self.__isHookerIndexExists():
            raise Exception("Cannot create the index '{0}' since it already exists.".format(Es.ES_INDEX_NAME_HOOKER))

        self._logger.info("Creating the index '{0}' in the ES cluster".format(Es.ES_INDEX_NAME_HOOKER))
        self.esInstance.indices.create(index=Es.ES_INDEX_NAME_HOOKER, body=Es.__getBodyIndex())

        time.sleep(1)
        
    @staticmethod
    def __getBodyIndex():
        return {
            "settings" : {
                "number_of_shards" : 1
            },
            "mappings": {
                Es.ES_DOCTYPE_EXPERIMENT_HOOKER: {
                    "_id": {
                        "path": "IDXP"
                    },
                    "_timestamp": {
                        "enabled": "true",
                        "path": "Timestamp"
                    },
                    "properties": {
                        "IDXP": {"type": "string", "index": "not_analyzed"},
                        "Emulator": {"type": "string", "index": "not_analyzed"},
                        "Author": {"type": "string", "index": "not_analyzed"},
                        "Analyzed": {"type": "boolean", "index": "not_analyzed"},
                        "Timestamp": {"type": "date"},
                        "RelativeTimestamp": {"type": "long"},
                        "PackageName": {"type": "string", "index": "not_analyzed"},
                        "Description": {"type": "string", "index": "not_analyzed"},
                        "Filename": {"type": "string"},
                        "Filesha1": {"type": "string", "index": "not_analyzed"},
                        "Analysis": {"type": "string"}
                    }
                },
                Es.ES_DOCTYPE_PYTHON_HOOKER: {
                    "_parent": {
                        "type": "experiment"
                    },
                    "_timestamp": {
                        "enabled": "true",
                        "path": "Timestamp"
                    },
                    "properties": {
                        "Emulator": {"type": "string", "index": "not_analyzed"},
                        "Timestamp": {"type": "date"},
                        "RelativeTimestamp": {"type": "long"},
                        "Description": {"type": "string", "index": "not_analyzed"}
                    }
                },
                Es.ES_DOCTYPE_APK_HOOKER: {
                    "_id": {
                        "path": "IDAPK"
                    },
                    "_timestamp": {
                        "enabled": "true",
                        "path": "Timestamp"
                    },
                    "properties": {
                        "IDAPK": {"type": "string"},
                        "Timestamp": {"type": "date"},
                        "Filename": {"type": "string"},
                        "Filesha1": {"type": "string"},
                        "Name": {"type": "string"},
                        "Url": {"type": "string"},                        
                        "Version": {"type": "string"},
                        "Market": {"type": "string"},
                        "Author": {"type": "string"},
                        "Category": {"type": "string"},
                        "Description": {"type": "string"},
                        "Filesize": {"type": "long"}
                    }
                },
                Es.ES_DOCTYPE_STATIC_HOOKER: {
                    "_parent": {
                        "type": "experiment"
                    },
                    "_timestamp": {
                        "enabled": "true",
                        "path": "Timestamp"
                    },
                    "properties": {
                        "Timestamp": {"type": "date"},
                        "Filename": {"type": "string", "index": "not_analyzed"},
                        "PackageName": {"type": "string"},
                        "Android Version Code": {"type": "string"},
                        "Android Version Name": {"type": "string"},
                        "Min SDK Version": {"type": "string"},
                        "Max SDK Version": {"type": "string"},
                        "Main Activity": {"type": "string"},
                        "Activities": {
                            "type": "nested",
                            "properties": {
                                "Activity": {"type":"string"},                                
                            }                            
                        },
                        "Providers": {
                            "type": "nested",
                            "properties": {
                                "Provider": {"type":"string"},                                
                            }
                        },                            
                        "Libraries": {
                            "type": "nested",
                            "properties": {
                                "Library": {"type":"string"},                                
                            }
                        },
                        "Services": { 
                            "type": "nested",
                            "properties": {
                                "Service": {"type":"string"},
                            }
                        },
                        "Receivers": {
                            "type": "nested",
                            "properties": {
                                "Receiver": {"type":"string"},
                            }
                        },
                        "Permissions": {
                            "type": "nested",
                            "properties": {
                                "Permission": {"type":"string"},
                            }
                        }
                    }
                },
                Es.ES_DOCTYPE_EVENT_HOOKER: {
                    "_parent": {
                        "type": "experiment"
                    },
                    "_timestamp": {
                        "enabled": "true",
                        "path": "Timestamp"
                    },
                    "properties": {
                        "Timestamp": {"type": "date"},
                        "RelativeTimestamp": {"type": "long"},
                        "HookerName": {"type": "string", "index": "not_analyzed"},
                        "IntrusiveLevel": {"type": "short"},
                        "PackageName": {"type": "string"},
                        "ClassName": {"type": "string"},
                        "MethodName": {"type": "string"},
                        "Parameters": {"type": "nested"},
                        "Return": {
                            "properties": {
                                "ParameterType": {"type": "string"},
                                "ParameterValue": {"type": "string"}
                            }
                        },
                        "Data": {
                            "properties": {
                                "DataName": {"type": "string"},
                                "DataValue": {"type": "string"}
                        }
                    }
                }
            }
        }
    }   


    @property
    def esNodes(self):
        """The definitions of es nodes
        """
        return self.__esNodes

    @esNodes.setter
    def esNodes(self, configuration):
        self.__esNodes = configuration

    @property
    def esInstance(self):
        """The definitions of the current es instance 
        """
        return self.__esInstance

    @esInstance.setter
    def esInstance(self, instance):
        self.__esInstance = instance

