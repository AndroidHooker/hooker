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
import os
import shutil
import uuid

from hooker_common import Logger

ES_HOST = "127.0.0.1"
ES_PORT = 9200

def createDirectory(directory, force=True):
    """Create the specified directory but fails if the directory already
    exists unless force is set to True. In that case, we delete it and re-create it"""
    logger = Logger.getLogger(__name__)
    logger.debug("Create directory {0} (force={1})".format(directory, force))
    
    if os.path.exists(directory):
        if force:
            shutil.rmtree(directory)
        else:
            raise Exception("Specified directoryalready exists, cannot create it.")
    else:
        os.mkdirs(directory)    

def createTemporaryFolder():
    """Create a random named temporary folder."""
    logger = Logger.getLogger(__name__)
    logger.debug("Create temporary directory.")
    
    tmpName = "tmp_"+str(uuid.uuid4())
    createDirectory(tmpName)
    return tmpName    
        
def main(markets, outFolder):
    """Main function"""
    logger = Logger.getLogger(__name__)
    
    if markets is None or len(markets)==0:
        raise Exception("Specify at least one market")

    if outFolder is None:
        raise Exception("Specify the output folder.")

    for market in markets:
        logger.info("Starting Market {0}".format(market))
        market.execute(outFolder, es_host=ES_HOST, es_port=ES_PORT)
    
    logger.info("Downloading APK from {0} markets.".format(len(markets)))
    

if __name__ == "__main__":

    usage = """
===================================================================
APK_Retriever - Automated APK Retriever from Online Android Markets.
===================================================================
@authors: Georges Bossert & Dimitri Kirchner (AMOSSYS)
@version: 0.1

>> USAGE: python apk_retriever.py outputFolder
"""
    logger = Logger.getLogger(__name__)
    if len(sys.argv) != 2:
        logger.info(usage)
        logger.warn("Specify the output folder as an execution parameter.")
        exit(-1)
    
    outputFolder = sys.argv[1]

    from apk_retriever.SlideMeMarket import SlideMeMarket
    
    markets = [
        SlideMeMarket(),
    ]

    
    main(markets=markets, outFolder=outputFolder)
