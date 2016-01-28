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
from logging import StreamHandler, DEBUG, getLogger as realGetLogger, Formatter

try:
    from colorama import Fore, Back, Style
 
    class ColourStreamHandler(StreamHandler):
        """ A colorized output SteamHandler """
 
        # Some basic colour scheme defaults
        colours = {
            'DEBUG' : Fore.CYAN,
            'INFO' : Fore.GREEN,
            'WARN' : Fore.YELLOW,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRIT' : Back.RED + Fore.WHITE,
            'CRITICAL' : Back.RED + Fore.WHITE
        }
 
        @property
        def is_tty(self):
            """ Check if we are using a "real" TTY. If we are not using a TTY it means that
            the colour output should be disabled.
 
            :return: Using a TTY status
            :rtype: bool
            """
            try: return getattr(self.stream, 'isatty', None)()
            except: return False
 
        def emit(self, record):
            try:
                message = self.format(record)
                
                if not self.is_tty:
                    self.stream.write(message)
                else:
                    self.stream.write(self.colours[record.levelname] + message + Style.RESET_ALL)
                self.stream.write(getattr(self, 'terminator', '\n'))
                self.flush()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)
 
    has_colour = True
except Exception, e:
    print "ERRROR: "+str(e)
    has_colour = False
 
def getLogger(name=None, fmt='[%(processName)s/%(filename)s:%(lineno)s/%(levelname)s] %(relativeCreated)d: %(message)s'):
    """ Get and initialize a colourised logging instance if the system supports
    it as defined by the log.has_colour
 
    :param name: Name of the logger
    :type name: str
    :param fmt: Message format to use
    :type fmt: str
    :return: Logger instance
    :rtype: Logger
    """

    log = realGetLogger(name)
    if not len(log.handlers):
        # Only enable colour if support was loaded properly
        handler = ColourStreamHandler() if has_colour else StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(Formatter(fmt))
        log.addHandler(handler)
        log.setLevel(DEBUG)
        log.propagate = False
    return log
