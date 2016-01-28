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

#+---------------------------------------------------------------------------+
# Imports
#+---------------------------------------------------------------------------+

from hooker_common import Logger
logger = Logger.getLogger(__name__)

import traceback

from hooker_xp.cli.CommandLine import CommandLine
from hooker_xp.ManualAnalysis import ManualAnalysis
from hooker_xp.AutomaticAnalysis import AutomaticAnalysis

def main():
    """Global entry point"""
    # Initiates the command line parser
    commandLineParser = CommandLine()

    # Prepare the proper kind of analysis based on user args.
    analysis = None
    if commandLineParser.manualAnalysisRequested:
        # Manual analysis
        analysis = ManualAnalysis(commandLineParser)
        
    elif commandLineParser.automaticAnalysisRequested:
        # Automated analysis
        analysis = AutomaticAnalysis(commandLineParser)
    else:
        # No analysis specified
        logger.warning("No analysis requested.")

    # Executes the prepared analysis
    if analysis is not None:
        analysis.start()

# CLI entry point        
if __name__ == "__main__":
    
    try:
        main()
    except Exception, e:
        tb = traceback.format_exc()
        logger.error(tb)
        #raise e




