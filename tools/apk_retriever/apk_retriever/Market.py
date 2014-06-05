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
#| @contact  : android-hooker@amossys.fr                                     |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+

import sys
import abc
import uuid

from hooker_common import Logger
from hooker_common.elasticsearch.Es import Es
from threading import Thread

import apk_retriever

class Market(Thread):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, name, url, description):
        Thread.__init__(self)
        self.name = name
        self.url = url
        self.description = description
        self.__nbRounds = 0
        self.logger = Logger.getLogger(__name__)

    def __str__(self):
        return "Market {0}".format(self.name)

    #
    # Optional methods to overide
    #
    
    def onStart(self):
        self.logger.debug("[{0}] on start ...".format(self.name))
        return True
    
    def onEnd(self):
        self.logger.debug("[{0}] on end ...".format(self.name))        
        return True

    def beforeDownload(self, APKID):
        self.logger.debug("[{0}] before download ...".format(self.name))        
        return True

    def download(self, APKID):
        self.logger.debug("[{0}] download ...".format(self.name))        
        return True

    def afterDownload(self, APKID):
        self.logger.debug("[{0}] after download ...".format(self.name))                
        return True

    #
    # Main execute method
    #        

    def execute(self, outputDirectory, es_host=None, es_port=None):
        self.outputDirectory = outputDirectory
        self.es_host = es_host
        self.es_port = es_port

        self.start()

    def run(self):        
        finish = False

        if not self.onStart():
            raise Exception("Market {0} has failed on startup.".format(self.name))
        
        while not finish:            
            APKID = self.__generateAPKID()
            
            if not self.beforeDownload(APKID):
                self.__logger.error("Market {0} has failed on round {1} in the beforeDownload step".format(self.name, self.nbRounds))
    
            downloadedAPK = self.download(APKID, self.outputDirectory)
            self.__logger.debug("Downloaded APK: {0}".format(downloadedAPK))
            if downloadedAPK is not None:                
                self.__registerAPK(downloadedAPK)
                self.__logger.info("APK {0} ({1}) has been succesfully downloaded.".format(downloadedAPK.name, downloadedAPK.APKID))

            if not self.afterDownload(APKID):
                self.__logger.error("Market {0} has failed on round {1} in the beforeDownload step".format(self.name, self.nbRounds))

    def __registerAPK(self, APK):
        if APK is not None:
            if self.es_host is not None and self.es_port is not None:
                self.logger.debug("Register {0}".format(APK))            
                es = Es([{"host":self.es_host, 'port':self.es_port}])
                es.insertAPK(APK, self.name)
            else:
                self.logger.warn("Cannot register APK in elasticsearch.")
        else:
            raise Exception("No APK provided")            
        
    def __generateAPKID(self):
        return str(uuid.uuid4())    

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError("Name is Mandatory.")
        self.__name = name

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if url is None:
            raise ValueError("Url is Mandatory.")
        self.__url = url

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def getNbRounds(self):
        return self.__nbRounds

    @property
    def outputDirectory(self):
        return self.__outputDirectory

    @outputDirectory.setter
    def outputDirectory(self, outputDirectory):
        self.__outputDirectory = outputDirectory

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger):
        self.__logger = logger

    @property
    def nbRounds(self):
        return self.__nbRounds

    @nbRounds.setter
    def nbRounds(self, nbRounds):
        self.__nbRounds = nbRounds
    
        
        
    
