#!/usr/bin/env python

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
#| @contact  : android-hooker@amossys.fr                                                         |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports
#+---------------------------------------------------------------------------+
import pygeoip

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger
from hooker_common.elasticsearch.Es import Es
from hooker_common.elasticsearch.EsInterrogator import EsInterrogator

#ES_IP = "192.168.0.16"
ES_IP = "127.0.0.1"
ES_PORT = 9200
logger = Logger.getLogger(__name__)

def eventToString(event):
    result = []

    result.append("Event {0}".format(event.HookerName))
    result.append("ClassName: {0}".format(event.ClassName))
    result.append("MethodName: {0}".format(event.MethodName))
    result.append("InstanceID: {0}".format(event.InstanceID))
    if event.Parameters is not None and len(event.Parameters) > 0:
        result.append("Parameters:")
        for parameter in event.Parameters:
            if parameter is not None and "ParameterType" in parameter.keys() and "ParameterValue" in parameter.keys():
                result.append("- {0} ({1})".format(parameter["ParameterValue"], parameter["ParameterType"]))
    if event.Return is not None:
        result.append("Return: {0}".format(event.Return))
    return "\n".join(result)

def filterEvents(events, className=None, methodName=None):
    result = []
    for event in events:
        insert = True
        if className is not None and event.ClassName != className:
            insert = False
        if methodName is not None and event.MethodName != methodName:
            insert = False

        if insert:
            result.append(event)
    return result

def macroAnalyzeTelephony(esInterrogator):
    logger.warn("Macro Analysis of Telephony")
    logger.warn("------------------------------------------------")

    telEvents = esInterrogator.getAllEvents(HookerName="Telephony")
    telPerXP = dict()
    for event in telEvents:
        method = event.MethodName
        if method not in telPerXP:
            telPerXP[method]=[]
        if event.Parent not in telPerXP[method]:
            telPerXP[method].append(event.Parent)
        
    logger.info("{0} events related to Telephony".format(len(telEvents)))
    for method, occ in telPerXP.iteritems():
        logger.info("{0}\t\t\t:{1}".format(method, len(occ)))

def macroAnalyzeNetwork(esInterrogator):
    logger.warn("Macro Analysis of Network")
    logger.warn("------------------------------------------------")

    telEvents = esInterrogator.getAllEvents(HookerName="Network")
    telPerXP = dict()
    for event in telEvents:
        method = event.MethodName
        if method not in telPerXP:
            telPerXP[method]=[]
        if event.Parent not in telPerXP[method]:
            telPerXP[method].append(event.Parent)
        
    logger.info("{0} events related to Network".format(len(telEvents)))
    for method, occ in telPerXP.iteritems():
        logger.info("{0}\t\t\t:{1}".format(method, len(occ)))


def macroAnalyzeIPC(esInterrogator):
    logger.warn("Macro Analysis of IPC")
    logger.warn("------------------------------------------------")

    telEvents = esInterrogator.getAllEvents(HookerName="IPC", ClassName="android.content.intent", MethodName="Intent")
    for event in telEvents:
        if len(event.Parameters)>=1 and "ParameterType" in event.Parameters[0].keys() and event.Parameters[0]['ParameterType'] == "java.lang.String":
            logger.info(eventToString(event))


def macroAnalyzeX509CustomVerification(esInterrogator):
    logger.warn("Macro Analysis of x509 custom verification")
    logger.warn("------------------------------------------------")

    initEvents = esInterrogator.getAllEvents(HookerName="Network", ClassName="javax.net.ssl.SSLContext", MethodName="init")
    customTrustManagers = dict()
    
    for event in initEvents:
        logger.debug(eventToString(event))
        if len(event.Parameters)>=1 and len(event.Parameters)<4:
            if "ParameterType" in event.Parameters[1].keys() and event.Parameters[1]['ParameterType'] == "[Ljavax.net.ssl.TrustManager;":
                tmp_trustManager = event.Parameters[1]['ParameterValue']
                
                trustManager = tmp_trustManager.split('{')[1].split('}')[0].split('@')[0]

                
                logger.warn(trustManager)
                if not "org.apache.harmony" in trustManager:
                    if trustManager not in customTrustManagers.keys():
                        customTrustManagers[trustManager] = []
                    if event.Parent not in customTrustManagers[trustManager]:
                        customTrustManagers[trustManager].append(event.Parent)
                        
                    logger.fatal("Found custom TrustManager: {0}".format(eventToString(event)))
                else:
                    logger.info("Found apache TrustManager: {0}".format(eventToString(event)))
    for k, v in customTrustManagers.iteritems():
        logger.warn("TrustManager: {0}".format(k))
        for w in v:
            apk = esInterrogator.getAPKInXP(w)
            logger.info("APK : {0}, market={1}, sha1={2}".format(apk.Name, apk.Market, apk.Filesha1))
        # # Finally, check if first and last parameters are different from null
        # if len(event.Parameters[0]) > 0:
        #     logger.info("Found client authentication: {0}".format(eventToString(event)))
        # if len(event.Parameters[2]) > 0:
        #     logger.info("Found random different from default: {0}".format(eventToString(event)))


def macroAnalyzeWebview(esInterrogator):
    logger.warn("Macro Analysis of Webview components")
    logger.warn("------------------------------------------------")
    eventsPerXP = []
    
    initEvents = esInterrogator.getAllEvents(HookerName="Network", ClassName="android.webkit.WebView", MethodName="addJavascriptInterface")
    for event in initEvents:
        if event.Parent not in eventsPerXP:
            eventsPerXP.append(event.Parent)        
        logger.info(eventToString(event))
    logger.warn("List of XP :")
    for xp in eventsPerXP:
        apk = esInterrogator.getAPKInXP(xp)
        logger.warn("{0}: {1} {2} ({3})".format(xp, apk.Name, apk.Market, apk.Filesha1))
    logger.warn("{0} XP founds.".format(len(eventsPerXP)))


def macroAnalyzeSocketListening(esInterrogator):
    logger.warn("Macro Analysis of socket listening on network")
    logger.warn("------------------------------------------------")
    eventsPerXP = []
    
    initEvents = esInterrogator.getAllEvents(HookerName="Network", ClassName="java.net.SocketServer", MethodName="SocketServer")
    for event in initEvents:
        if event.Parent not in eventsPerXP:
            eventsPerXP.append(event.Parent)        
        logger.info(eventToString(event))
    logger.warn("List of XP :")
    for xp in eventsPerXP:
        apk = esInterrogator.getAPKInXP(xp)
        logger.warn("{0}: {1} {2} ({3})".format(xp, apk.Name, apk.Market, apk.Filesha1))
    logger.warn("{0} XP founds.".format(len(eventsPerXP)))

def macroAnalyzeGeolocation(esInterrogator):
    logger.warn("Macro Analysis of geolocation requests")
    logger.warn("------------------------------------------------")
    eventsPerXP = []
    
    initEvents = esInterrogator.getAllEvents(HookerName="Geolocation", ClassName="android.location.locationmanager", MethodName="getlastknownlocation")
    for event in initEvents:
        if event.Parent not in eventsPerXP:
            eventsPerXP.append(event.Parent)        
        logger.info(eventToString(event))

    initEvents = esInterrogator.getAllEvents(HookerName="Geolocation", ClassName="android.location.location", MethodName="getlongitude")
    for event in initEvents:
        if event.Parent not in eventsPerXP:
            eventsPerXP.append(event.Parent)        
        logger.info(eventToString(event))
    
    initEvents = esInterrogator.getAllEvents(HookerName="Geolocation", ClassName="android.location.location", MethodName="getlatitude")
    for event in initEvents:
        if event.Parent not in eventsPerXP:
            eventsPerXP.append(event.Parent)        
        logger.info(eventToString(event))


    logger.warn("List of XP :")
    for xp in eventsPerXP:
        apk = esInterrogator.getAPKInXP(xp)
        logger.warn("{0}: {1} ({2})".format(xp, apk.Name, apk.Filesha1))
    logger.warn("{0} XP founds.".format(len(eventsPerXP)))


def macroAnalyzeConnectTo(esInterrogator):
    logger.warn("Macro Analysis of IP where APK are connecting")
    logger.warn("------------------------------------------------")

    connectIPs = dict()
    connectPorts = dict()
    connectURLs = dict()
    
    initEvents = esInterrogator.getAllEvents(HookerName="Network", ClassName="java.net.Socket", MethodName="connect")
    for event in initEvents:
        if "ParameterType" in event.Parameters[0].keys() and event.Parameters[0]['ParameterType'] == "java.net.InetSocketAddress":
            tmp = event.Parameters[0]['ParameterValue'].split('/')
            url = tmp[0]
            tmp = tmp[1].split(':')
            ip = tmp[0]
            port = tmp[1]
            #logger.info("url: {0}, ip: {1}, port: {2}".format(url, ip, port))
            # Get URLs
            if url not in connectURLs:
                connectURLs[url] = []
            if event.Parent not in connectURLs[url]:
                connectURLs[url].append(event.Parent)
            # Get IPs
            if ip not in connectIPs:
                connectIPs[ip] = []
            if event.Parent not in connectIPs[ip]:
                connectIPs[ip].append(event.Parent)
            # Get ports
            if port not in connectPorts:
                connectPorts[port] = []
            if event.Parent not in connectPorts[port]:
                connectPorts[port].append(event.Parent)
            
    logger.warn("------------------------------------------------")
    logger.warn("List of URLs and number XP associated :")
    for url, xp in connectURLs.iteritems():
        logger.info("URL: {0} -> number of xp: {1}".format(url, len(xp)))

    logger.warn("------------------------------------------------")
    logger.warn("List of ports and number XP associated :")
    for port, xp in connectPorts.iteritems():
        logger.info("Port: {0} -> number of xp: {1}".format(port, len(xp)))
        if port!='80' and port !='443':
            for _xp in xp:
                apk = esInterrogator.getAPKInXP(_xp)
                logger.warn("Port {0} APK: {1} {2} {3}".format(port, apk.Name, apk.Market, apk.Filesha1))
        
    logger.warn("------------------------------------------------")
    gic = pygeoip.GeoIP('GeoLiteCity.dat')
    connectCities = dict()
    for ip, xp in connectIPs.iteritems():
        city = gic.time_zone_by_addr(ip)
        if city not in connectCities:
            connectCities[city] = []
        if xp not in connectCities[city]:
            connectCities[city].append(xp)
    
    logger.warn("List of cities and XP associated :")
    for city, xp in connectCities.iteritems():
        logger.info("{0} -> number of xp: {1}".format(city, len(xp)))

    
def macroAnalyzeDeviceLockBypass(esInterrogator):
    logger.warn("Macro Analysis of Device Lock Bypass (CVE-2013-6271)")
    logger.warn("------------------------------------------------")

    initEvents = esInterrogator.getAllEvents(HookerName="IPC", ClassName="android.content.intent", MethodName="putExtra")
    for event in initEvents:
        
        if len(event.Parameters)==2:
            # TODO : do this better if we have interesting results...
            if "ParameterType" in event.Parameters[0].keys() and event.Parameters[0]['ParameterType'] == "java.lang.String":
                param = event.Parameters[0]['ParameterValue']
                if "command" in param or "imei" in param or "sms" in param or "PrivateUrls" in param:                    
                    logger.info(eventToString(event))
                # if "confirm_credentials" in params:
                #     # TODO if necessary: check value of the second param
                #     logger.fatal(eventToString(event))


def macroAnalyzeCrypto(esInterrogator):
    logger.warn("Macro Analysis of Crypto Events")
    logger.warn("------------------------------------------------")    
    
    logger.warn("------------------------------------------------")
    logger.warn("Base 64")
    logger.warn("------------------------------------------------")            
    b64Events = esInterrogator.getAllEvents(HookerName="Crypto", ClassName="android.util.Base64")
    for event in b64Events:
        logger.info(eventToString(event))
    logger.info("{0} events related to Base 64".format(len(b64Events)))

    logger.warn("------------------------------------------------")
    logger.warn("Cipher")
    logger.warn("------------------------------------------------")

    # Retrieves all the events related to the getInstance call in javax.Crypto.Cipher Class
    cipherEvents = esInterrogator.getAllEvents(HookerName="Crypto", ClassName="javax.crypto.Cipher", MethodName="getInstance")
    algosPerXP = dict()
    for event in cipherEvents:
        # Stores the firt parameter of this method call (the algorithm used)
        algo = event.Parameters[0]["ParameterValue"]
        if algo not in algosPerXP:
            algosPerXP[algo]=[]
            
        if event.Parent not in algosPerXP[algo]:
            algosPerXP[algo].append(event.Parent)

    # List the Android applications that triggered each type of Cipher algorithm
    for algo, xps in algosPerXP.iteritems():
        apks = [esInterrogator.getAPKInXP(xp) for xp in xps]
        logger.warn("{0} ({1} apks): ".format(algo, len(xps)))
        for apk in apks:
            logger.info("\t- {0} ({1})".format(apk.Name, apk.Filesha1))

    logger.warn("------------------------------------------------")
    logger.warn("Mac")
    logger.warn("------------------------------------------------")            
    cipherEvents = esInterrogator.getAllEvents(HookerName="Crypto", ClassName="javax.crypto.Mac", MethodName="getInstance")
    algosPerXP = dict()
    for event in cipherEvents:
        algo = event.Parameters[0]["ParameterValue"]
        if algo not in algosPerXP:
            algosPerXP[algo]=[]
        if event.Parent not in algosPerXP[algo]:
            algosPerXP[algo].append(event.Parent)
        
    logger.info("{0} events related to Mac".format(len(cipherEvents)))
    for algo, occ in algosPerXP.iteritems():
        logger.info("{0}\t\t\t:{1}".format(algo, len(occ)))

    logger.warn("------------------------------------------------")
    logger.warn("MessageDigest")
    logger.warn("------------------------------------------------")            
    cipherEvents = esInterrogator.getAllEvents(HookerName="Crypto", ClassName="java.security.MessageDigest", MethodName="getInstance")
    algosPerXP = dict()
    for event in cipherEvents:
        algo = event.Parameters[0]["ParameterValue"]
        if algo not in algosPerXP:
            algosPerXP[algo]=[]
        if event.Parent not in algosPerXP[algo]:
            algosPerXP[algo].append(event.Parent)
        
    logger.info("{0} events related to MessageDigest".format(len(cipherEvents)))
    # List the Android applications that triggered each type of Cipher algorithm
    for algo, xps in algosPerXP.iteritems():
        apks = [esInterrogator.getAPKInXP(xp) for xp in xps]
        logger.warn("{0} ({1} apks): ".format(algo, len(xps)))
        for apk in apks:
            logger.info("\t- {0} ({1})".format(apk.Name, apk.Filesha1))
    for algo, occ in algosPerXP.iteritems():
        logger.info("{0}\t\t\t:{1}".format(algo, len(occ)))
    

def deleteDuplicatedAPK(esInterrogator):
    logger.info("Register unknown APK")

    # search for all the experiments
    experiments = esInterrogator.getAllExperiments()
    logger.debug("{0} experiments found".format(len(experiments)))

    errorXp = []

    experimentToAPK = dict()
    # check if an apk is registered for each experiment
    for experiment in experiments:
        apk = esInterrogator.getAPKInXP(experiment.IDXP)
        experimentToAPK[experiment] = apk
        if apk is None:
            errorXp.append(experiment)
    for experiment, apk in experimentToAPK.iteritems():
        if apk is None:
            raise "An APK is missing."
        elif isinstance(apk, list):
            # multiple apk, we delete last inserted
            logger.debug(apk)
            toDeleteApk = []
            keptApk = None
            for a in apk:
                if keptApk is None or a.Timestamp < keptApk.Timestamp:
                    if keptApk is not None:
                        toDeleteApk.append(keptApk)
                    keptApk = a
                else:
                    toDeleteApk.append(a)
            logger.warn("We delete the APK : ")
            logger.warn(toDeleteApk)
            for apk in toDeleteApk:
                try:
                    esInterrogator.es.deleteAPK(apk)
                except Exception, e:
                    logger.warn("An occured and prevented the suppression of the APK, {0}".format(e))
        
        logger.debug("{0}: {1}".format(experiment.IDXP, apk))
    logger.warn("{0} experiment has an invalid number of APK".format(len(errorXp)))

            
def main():
    """Main function that execute the various post-analysis functions"""
    logger.info("Execution of the Post-Analysis functions")

    # Initialization of the connection to an ES database
    es = Es([{"host":ES_IP, 'port':ES_PORT}])

    esInterrogator = EsInterrogator(es)

    # ======================================================    
    # Activate here the kind of analysis you want to perform
    # ======================================================

    # macroAnalyzeConnectTo(esInterrogator)    
    # macroAnalyzeCrypto(esInterrogator)
    # macroAnalyzeTelephony(esInterrogator)
    # macroAnalyzeNetwork(esInterrogator)
    # macroAnalyzeIPC(esInterrogator)
    # macroAnalyzeWebview(esInterrogator)
    # macroAnalyzeX509CustomVerification(esInterrogator)
    # macroAnalyzeDeviceLockBypass(esInterrogator)
    # macroAnalyzeGeolocation(esInterrogator)
    
    # # Retrieve all the known APKs (analyzed or not)
    # # =============================================
    # logger.warn("List of APKs")
    # logger.warn("------------------------------------------------")
    # apks = esInterrogator.getAllAPKs()
    # for apk in apks:
    #     logger.info("Name:{0} - Market:{1} - Downloaded Date:{2} - Filesha1:{3} - Filename:{4}".format(apk.Name, apk.Market, apk.Timestamp, apk.Filesha1, apk.Filename))
        
    # logger.warn("> We found {0} apks.".format(len(apks)))
    # logger.warn("------------------------------------------------")

    # # Retrieve all the known experimentations
    # # =======================================
    # logger.warn("List of Experimentations")
    # logger.warn("------------------------------------------------")
    # experiments = esInterrogator.getAllExperiments()
    # for experiment in experiments:
    #     logger.info("IDXP:{0} - Filename:{1} - Filesha1:{2} - Emulator:{3}".format(experiment.IDXP, experiment.Filename, experiment.Filesha1, experiment.Emulator))
        
    # logger.warn("> We found {0} experiments.".format(len(experiments)))
    # logger.warn("------------------------------------------------")

    # Now we list the experimentations that cover each APK
    # ====================================================
    # logger.warn("List of Experimentations per APK")
    # logger.warn("------------------------------------------------")
    # for apk in apks:
    #     logger.info("APK {0} (sha1 = {1})".format(apk.Name, apk.Filesha1))
    #     experiments = esInterrogator.getExperimentsWithAPKSha1(apk.Filesha1)
    #     for experiment in experiments:
    #         events = esInterrogator.getAllEventsOfExperiment(experiment.IDXP)
    #         logger.warn("\t- XP {0} : {1} events captured.".format(experiment.IDXP, len(events)))
    # logger.warn("------------------------------------------------")    

    
    # Retrieve all the events associated with one Experiment
    # ======================================================
    # idXp = "93deb34a13c8a958d75dea4beaea7718"
    # logger.warn("List of events related to XP {0}".format(idXp))
    # logger.warn("------------------------------------------------")    
    # events = esInterrogator.getAllEventsOfExperiment(idXp)
   
    # for event in events:
    #     logger.info("{0} - {1} - {2} - {3}".format(event.HookerName, event.ClassName,  event.MethodName, event.PackageName))
    #     if event.Parameters is not None:
    #         for parameter in event.Parameters:
    #             logger.debug("Parameter: "+str(parameter))
                
    # logger.error("> We found {0} events.".format(len(events)))
    # logger.warn("------------------------------------------------")    

    # logger.warn("Events by Hooker")
    # logger.warn("------------------------------------------------")    
    
    # logger.warn("DynamicCodeLoader Events")
    # logger.warn("------------------------------------------------")            
    # dynEvents = esInterrogator.getAllEvents(HookerName="Account")
    # for event in dynEvents:
    #     logger.info(eventToString(event))

    # logger.warn("Telephony Events")
    # logger.warn("------------------------------------------------")            
    # telephonyEvents = esInterrogator.getAllEvents(HookerName="Telephony")
    # for event in telephonyEvents:
    #     logger.info(eventToString(event))
        
    # logger.warn("Runtime Events")
    # logger.warn("------------------------------------------------")            
    # runtimeEvents = esInterrogator.getAllEvents(HookerName="RunTime")
    # for event in runtimeEvents:
    #     logger.info(eventToString(event))

    # logger.warn("System Events")
    # logger.warn("------------------------------------------------")            
    # systemEvents = esInterrogator.getAllEvents(HookerName="System")
    # for event in systemEvents:
    #     logger.info(eventToString(event))

    # logger.warn("Network Events")
    # logger.warn("------------------------------------------------")            
    # networkEvents = esInterrogator.getAllEvents(HookerName="Network")
    # for event in networkEvents:
    #     logger.info(eventToString(event))
       
    # Lets retrieve only java.net.URL:URL method calss
    # logger.warn("List of URLs")
    # logger.warn("------------------------------------------------")            
    # listOfURLs = dict()
    # urlEvents = esInterrogator.getAllEvents(ClassName="java.net.URL", MethodName="URL")
    # for urlEvent in urlEvents:
    #     if urlEvent.Parameters is not None and len(urlEvent.Parameters) == 1:
    #         url = urlEvent.Parameters[0]["ParameterValue"]
    #         if url not in listOfURLs.keys():
    #             listOfURLs[url] = 0
    #         listOfURLs[url] += 1
    #     else:
    #         logger.warn(eventToString(urlEvent))
    # for url, nbDef in listOfURLs.iteritems():
    #     logger.info("{0} ({1})".format(url, nbDef))
    


        
    # Let's find all the apks
    #apks = es.getAllAPKs()

    


# CLI entry point        
if __name__ == "__main__":
    main()
    
    



