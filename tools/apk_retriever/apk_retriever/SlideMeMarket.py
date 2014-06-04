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
#| @contact  : @todo                                                         |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#+---------------------------------------------------------------------------+

from apk_retriever.Market import Market
from hooker_common.APK import APK
from collections import deque
import urllib2
from bs4 import BeautifulSoup
import os


class SlideMeMarket(Market):

    NAME = "SlideMe"
    URL = "http://www.slideme.org/"
    DESC = "SlideME is the best alternative to Google Play, which offers a wide range of free and premium android Apps from application developers all around the world."
    
    def __init__(self):
        super(SlideMeMarket, self).__init__(SlideMeMarket.NAME, SlideMeMarket.URL, SlideMeMarket.DESC)
        self.__APKsInPage = deque()
        self.__currentPage = -1 # first page is 0

        
    def beforeDownload(self, APKID):
        if len(self.__APKsInPage) == 0:
            return self.__parseNextPage()
        return True

    def download(self, APKID, outputDirectory):
        self.logger.info("Download APK {0} from slideMe market in {1}".format(APKID, outputDirectory))

        apkURL = self.__APKsInPage.popleft()
        response = urllib2.urlopen(apkURL)

        html_page = response.read()
        soup = BeautifulSoup(html_page)
        response.close()
   
        for link in soup.find_all('a'):
            if(".apk" in link.get('href')):
                app_path = link.get('href')
                
                self.logger.debug("APK path has been found: {0}".format(app_path))
                #Extract app name
                _list = apkURL.rsplit('/')
                apkName = _list[4]
                if "?id=" in apkName:
                    # Slideme modification detected on 11/04/2014
                    apkName = apkName.split("?id=")[1]                
                
                apkOutputPath = outputDirectory+"/"+APKID+".apk"
                
                if os.path.exists(apkOutputPath):
                    self.logger.error("File {0} already exists, don't make this twice...".format(apkOutputPath))
                else:
                    self.logger.debug("Downloading APK {0} from {1}".format(apkName, app_path))
                    try:
                        tmp = urllib2.urlopen("http://slideme.org/"+app_path)
                        self.logger.debug("Downloading APK... ")
                        if 200==tmp.code:
                            apk_bytes = tmp.read()
                            #Write into file
                            f = open(apkOutputPath, 'wb')
                            f.write(apk_bytes)
                            f.close()
                            self.logger.debug("Downloading {0}: OK!".format(apkName))
                            return APK(APKID, apkOutputPath, apkName, "http://slideme.org"+app_path)
                        else:
                            self.logger.error("APK response code is not 200 but: {0}".format(tmp.code))
                        tmp.close()
                    except IOError:
                        self.logger.error("IOError: File {0} has not been saved.".format(apkOutputPath))
                    except urllib2.URLError:
                        self.logger.error("Cannot download file.")
                
        return None

    def __parseNextPage(self):
        url_begin = "http://slideme.org/applications?page="
        url_end = "&solrsort=tfs_price%20asc"

        self.__currentPage += 1
        if self.__currentPage > 2139:
            self.logger.info("No more available pages.")
            return False

        url = "{0}{1}{2}".format(url_begin, self.__currentPage, url_end)
        
        self.logger.info("Getting APKs from page {0} ({1})".format(self.__currentPage, url))

        response = urllib2.urlopen(url)

        html_page = response.read()
        soup = BeautifulSoup(html_page)
        response.close()
   
        for link in soup.find_all('a'):
            if("application/" in link.get('href')):
                app_path = link.get('href')
                if("http" in app_path):
                    self.logger.debug("Wrong app_path: "+app_path) #This should be done in a better way...
                else:
                    apkUrl = "http://slideme.org"+app_path
                    self.logger.debug("Identified APK {0}".format(apkUrl))
                    self.__APKsInPage.append(apkUrl)
        
        
