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
import subprocess
import shlex

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger

class OSCommand(object):
    """Tool class that provides common methods to execute commands on the OS
    """

    @staticmethod
    def executeAsyncCommand(commandAndArgs):
        logger = Logger.getLogger(__name__)
        logger.debug("Executing Asynchronous command {0}".format(commandAndArgs))
        return subprocess.Popen(commandAndArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #return subprocess.Popen(commandAndArgs)

    @staticmethod
    def executeCommand(commandAndArgs):
        logger = Logger.getLogger(__name__)

        if isinstance(commandAndArgs, str):
            commandAndArgs = shlex.split(commandAndArgs)
        
        logger.debug("Executing command {0}".format(commandAndArgs))
        return subprocess.check_output(commandAndArgs, stderr=subprocess.STDOUT)

