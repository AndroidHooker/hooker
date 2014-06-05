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
from hooker_common import Logger
from hooker_common.elasticsearch.Es import Es


class EsInterrogator(object):
    """This class provides various methods to retrieve stored in an ES database."""

    EXPERIMENT_FIELDS = "Description,Filesha1,Author,Analyzed,Timestamp,PackageName,IDXP,Emulator,Filename"
    APK_FIELDS = "Category,IDAPK,Name,Author,Url,Filename,Version,Filesize,Description,Filesha1,Timestamp,Market"            
    EVENT_FIELDS = "Timestamp,InstanceID,RelativeTimestamp,HookerName,IntrusiveLevel,PackageName,ClassName,MethodName,Parameters,Return"
    
    def __init__(self, es):
        self.es = es
        self._logger = Logger.getLogger(__name__)

    def getExperimentsWithAPKSha1(self, sha1):
        values = self._getExperimentsWithAPKSha1(sha1)
        
        # now we transform the returned json into class
        experiments = []
        for value in values:
            experiment = self._json_to_obj("Experiment", value)
            experiments.append(experiment)
        return experiments

    def _getExperimentsWithAPKSha1(self, sha1):
        """Retrieve all the Experiments listed in the ES"""
        if self.es is None:
            raise Exception("Cannot retrieve all the Experiments since no ES cluster available.")
        if sha1 is None or len(sha1) == 0:
            raise Exception("No sha1 provided.")

        getBody = {
            "query": {
                "term" : {"Filesha1": sha1} 
            }
        }

        queryFields = EsInterrogator.EXPERIMENT_FIELDS
            
        return self._executeSearchQuery(Es.ES_DOCTYPE_EXPERIMENT_HOOKER, getBody, queryFields)        

    def getAllExperiments(self):
        values = self._getAllExperiments()
        
        # now we transform the returned json into class
        experiments = []
        for value in values:
            experiment = self._json_to_obj("Experiment", value)
            experiments.append(experiment)
        return experiments

    def _getAllExperiments(self):
        """Retrieve all the Experiments listed in the ES"""
        if self.es is None:
            raise Exception("Cannot retrieve all the Experiments since no ES cluster available.")

        getBody = {
            "query": {
                "match_all" : {} 
            }
        }

        queryFields = EsInterrogator.EXPERIMENT_FIELDS
            
        return self._executeSearchQuery(Es.ES_DOCTYPE_EXPERIMENT_HOOKER, getBody, queryFields)        
    

    def getAllAPKs(self):
        values = self._getAllAPKs()
        
        # now we transform the returned json into class
        apks = []
        for value in values:
            apk = self._json_to_obj("APK", value)
            apks.append(apk)
        return apks

    def _getAllAPKs(self):
        """Retrieve all the APKs listed in the ES"""
        if self.es is None:
            raise Exception("Cannot retrieve all the APKs since no ES cluster available.")

        getBody = {
            "query": {
                "match_all" : {} 
            }
        }

        queryFields = EsInterrogator.APK_FIELDS

        return self._executeSearchQuery(Es.ES_DOCTYPE_APK_HOOKER, getBody, queryFields)

    def getAPKInXP(self, xp):

        experiment = self.getExperiment(xp)

        filesha1 = experiment.Filesha1
        
        if filesha1 is not None and len(filesha1)>0:
            getBody = {
                "query": {
                    "term" : {"Filesha1": filesha1} 
                }
            }
            queryFields = EsInterrogator.APK_FIELDS
            values = self._executeSearchQuery(Es.ES_DOCTYPE_APK_HOOKER, getBody, queryFields)
            if len(values)!=1:
                print ("!! {0} APK found with IDXP {1}".format(len(values), xp))
                apks = []
                for ival, val in enumerate(values):
                    a = self._json_to_obj("APK", val)
                    apks.append(a)
                return apks

            # now we transform the returned json into class
            return self._json_to_obj("APK", values[0])
        else:
            raise Exception("Returned filesha1 {0} associated with IDXP {1}".format(filesha1, xp))

    def getExperiment(self, xp):
        # retrieve the xp object
        getBody = {
            "query": {
                "term" : {"IDXP": xp} 
            }
        }

        queryFields = EsInterrogator.EXPERIMENT_FIELDS
            
        values = self._executeSearchQuery(Es.ES_DOCTYPE_EXPERIMENT_HOOKER, getBody, queryFields)
        if len(values) != 1:
            raise Exception("{0} experiments found with XP {0}".format(len(values), xp))
        # now we transform the returned json into class
        return self._json_to_obj("Experiment", values[0])


    def getAllEventsByHooker(self):
        """Returns a dict that associate the hooker type with all its events"""

        events = self.getAllEvents()

        result = dict()
        for event in events:
            if event.HookerName not in result.keys():
                result[event.HookerName] = []

            result[event.HookerName].append(event)
        return result

    def getAllEvents(self, HookerName=None, ClassName=None, MethodName=None):
        values = self._getAllEvents(HookerName=HookerName,ClassName=ClassName, MethodName=MethodName)
        
        # now we transform the returned json into class
        events = []
        for value in values:
            event = self._json_to_obj("Event", value)
            events.append(event)
        return events

        
    def _getAllEvents(self, HookerName=None, ClassName=None, MethodName=None):

        query = []
        query.append("{")
        query.append('"query":{')
        query.append('"bool":{')
        query.append('"must": [')
        if HookerName is None and ClassName is None and MethodName is None:
            query.append('{"match_all":{}}')
        else:
            filters = []
            if HookerName is not None:
                filters.append('{"term":{"event.HookerName": "'+HookerName+'"}}')
            if ClassName is not None:
                filters.append('{"term":{"event.ClassName": "'+ClassName.lower()+'"}}')
            if MethodName is not None:
                filters.append('{"term":{"event.MethodName": "'+MethodName.lower()+'"}}')
            query.append(','.join(filters))
            
        query.append(']')
        query.append('}')
        query.append('}')
        query.append('}')
        getBody = ''.join(query)
        self._logger.debug(getBody)

#{query:{bool:{must: [{term:{event.HookerName: Crypto}}]}}}
#{"query":{"bool":{"must":[{"term":{"event.HookerName":"Crypto"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"facets":{}}
        # getBody = {
        #     "query": {
        #         "match_all" : {}
        #         }
        #     }
# {"query":{bool:{must: [{term:{"event.HookerName": "Crypto"}},]}}}

#             query: {
#         bool: {
#             must: [
#                 {
#                     match_all: { }
#                 }
#             ]
#             must_not: [ ]
#             should: [ ]
#         }
#     }

        queryFields = EsInterrogator.EVENT_FIELDS

        return self._executeSearchQuery(Es.ES_DOCTYPE_EVENT_HOOKER, getBody, queryFields)
        

    def getAllEventsOfExperiment(self, idXp):
        values = self._getAllEventsOfExperiment(idXp)
        
        # now we transform the returned json into class
        events = []
        for value in values:
            event = self._json_to_obj("Event", value)
            events.append(event)
        return events
        
        
    def _getAllEventsOfExperiment(self, idXp):
        """Returns all the events related to the idXP"""
        if idXp is None or len(idXp) == 0:
            raise Exception("IdXp cannot be null")
        if self.es is None:
            raise Exception("Cannot retrieve all the events associated with an IdXp since no ES cluster available.")

        getBody = {
            "query": {
            "has_parent" : {
                "type" : Es.ES_DOCTYPE_EXPERIMENT_HOOKER,
                "query" : {
                    "match" : {
                        "IDXP" : idXp
                    }
                }
            }
            }
        }
        print getBody
        

        queryFields = EsInterrogator.EVENT_FIELDS
        print queryFields

        return self._executeSearchQuery(Es.ES_DOCTYPE_EVENT_HOOKER, getBody, queryFields)

    def _executeSearchQuery(self, docType, getBody, queryFields):
        if docType == Es.ES_DOCTYPE_EVENT_HOOKER:
            fields= ["_parent", "_source"]
        else:
            fields= ["_source"]

        results = self.es.esInstance.search(index=Es.ES_INDEX_NAME_HOOKER, doc_type=docType, body=getBody, fields=fields, _source=queryFields, scroll='1m', search_type="scan")

        # we retrieve the scroll id to scan for results
        if results is None:
            raise Exception("The search query failed.")

        # first, we check all the shards were successfuly searched
        shards = results["_shards"]
        if int(shards['total']) == 0:
            raise Exception("No shard were queried.")
        if int(shards['failed']) > 0:
            raise Exception("Some shards were not sucessfuly queries.")
        
        if '_scroll_id' not in results.keys():
            raise Exception("Unable to open a scroll request, no scroll id returned by the Es cluster")
        
        scrollId = results['_scroll_id']
        values = []

        finish = False
        while not finish:
            finish = True
            # scroll accross all the results
            scrollResults = self.es.esInstance.scroll(scroll_id=scrollId, scroll='1m')
            scrollHits = scrollResults['hits']['hits']
            if len(scrollHits) > 0:
                finish = False
            for scrollHit in scrollHits:
                val = {}
                if "fields" in scrollHit.keys() and "_parent" in scrollHit["fields"].keys():
                    val["Parent"]=scrollHit["fields"]["_parent"]
                
                # arbitrary set to None the value of unreturned fields
                for queryField in queryFields.split(","):
                    if queryField in scrollHit["_source"].keys():
                        val[queryField]=scrollHit["_source"][queryField]
                    else:
                        val[queryField]=None
                values.append(val)
                        
            scrollId = scrollResults['_scroll_id']    

        return values

    def _json_to_obj(self, objectName, s):
        def h2o(x):
            if isinstance(x, dict):
                return type(objectName, (), {k: h2o(v) for k, v in x.iteritems()})
            else:
                return x
        return h2o(s)    

    @property
    def es(self):
        """The connection to the es database
        """
        return self.__es

    @es.setter
    def es(self, es):
        if es is None:
            raise Exception("An ES instance must be provided.")
            
        self.__es = es
    
