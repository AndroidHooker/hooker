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
import telnetlib
import time
import random

#+---------------------------------------------------------------------------+
#| Local imports
#+---------------------------------------------------------------------------+
from hooker_common import Logger
from hooker_xp.analysis.Analysis import Analysis

class TelnetEmulation(object):
    """
    Manage the Telnet emulation in order to emulate phone calls, SMS reception, GPS position, etc.
    This class has to be continued. In particular, things have to be done to make interactions different between each execution.
    """

    def __init__(self, reporter, idXp, emulator, host="127.0.0.1"):
        self._logger = Logger.getLogger(__name__)
        self.emulator = emulator
        self.emulatorNumber = emulator.emulatorId
        self.reporter = reporter
        self.idXp = idXp
        self.__telnetPort = 5554 + (self.emulatorNumber*2)
        self.__host = host
        
        if emulator.mainConfiguration.typeOfDevice=='emulated':
            self.__emulatorSerialNumber = "emulator-{0}".format(self.__telnetPort)
        else:
            self.__emulatorSerialNumber = emulator.name

        
    def start(self):
        """
        Uses telnetlib to connect to the emulator. We grep for keyword "OK" and 
        launch the different commands to simulate operations. Between each of them, 
        we sleep for a random time.
        Remark: from the Android Documentation, we do not have meaning to simulate 
        neither WIFI nor bluetooth
        """
        self._logger.debug("Starting stimulation with emulator: {0}.".format(self.__emulatorSerialNumber))

        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Opening telnet session with emulator: {0}".format(self.__emulatorSerialNumber))
        self.session = telnetlib.Telnet(self.__host, self.__telnetPort)
        self._checkAnswer(1)
   
        #Todo: build something different each time
        try:
            list_functions = [self._sendSms, self._setGpsLocation, self._simulatePhoneConversation, self._simulateChangingData, self._sendSensorAcceleration, self._simulateChangingData]
            random.seed()
            for function in list_functions:
                function()
                n = random.randint(20, 30)
                self._logger.debug("Sleeping for {0} seconds".format(n))
                time.sleep(n)

        except NameError as ne:
            raise Exception (ne)

        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Closing telnet for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Closing telnet")
        self.session.write("exit\r\n")
        self.session.close()


    def _checkAnswer(self, verbose):
        """
        Validate answer from emulator. Return True if response is OK, False otherwise.
        """
        ret = self.session.read_some()
        
        if ("Android Console:" in ret):
            if verbose: 
                self._logger.debug("Android console recognized")
            self._checkAnswer(1)
        elif ("OK" in ret):
            if verbose:
                self._logger.debug("OK")
            return True
        elif (ret=="\r\n"):
            if verbose:
                self._logger.debug("\\r\\n")
            return True
        elif ("KO" in ret):
            if verbose:
                self._logger.debug("KO")
            return False
        else:
            self._logger.debug(" unrecognized response: {0}".format(ret))
            return False


    def _sendSms(self):
        """ Send an SMS to emulator """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Sending SMS to emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Sending SMS to emulator"),
        self.session.write("sms send 062445581 It was nice to see you again, thx for this evening.\r\n")
        self._checkAnswer(1)

        
    def _setGpsLocation(self):
        """ Set the GPS location of emulator somewhere in Paris """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Setting GPS location to somewhere in Paris for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Setting GPS location to somewhere in Paris"),
        self.session.write("geo fix 2.33 48.89\r\n")
        self._checkAnswer(1)
   

    def _simulatePhoneConversation(self):
        """
        Simulate a phone conversation on the emulator.
        First, start the call, wait for several seconds, and hang up.
        """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Calling emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Calling emulator"),
        self.session.write("gsm call 0633416719\r\n")
        if self._checkAnswer(1):
            time.sleep(5)
            Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Answering call for emulator: {0}".format(self.__emulatorSerialNumber))
            self._logger.debug("Answer call"),
            self.session.write("gsm accept 0633416719\r\n")
            if self._checkAnswer(1):
                time.sleep(10)
                Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Hanging up call for emulator: {0}".format(self.__emulatorSerialNumber))
                self._logger.debug("Hang up call"),
                self.session.write("gsm cancel 0633416719\r\n")
                self._checkAnswer(1)
            else:
                Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Cannot accept call for emulator: {0}".format(self.__emulatorSerialNumber))
                self._logger.error("Cannot accept call")
        else:
            Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Cannot make call for emulator: {0}".format(self.__emulatorSerialNumber))
            self._logger.error("Cannot make call")
   

    def _simulateChangingData(self):
        """ Simulate a change of data connection """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Simulating data connection change for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Simulating data connection change"),
        self.session.write("gsm status\r\n")
        # This is a little different since we need the return string to chose which way to go: 2G -> 3G or 3G -> 2G
        res = self.session.read_until("OK")
        
        if ("unregistered" in res):
            self._simulate2Gto3G()
        else:
            self._simulate3Gto2G()
        

    def _simulate3Gto2G(self):
        """ Simulate a 3G to 2G connection """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Simulating 3G to 2G for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Simulating 3G to 2G"),
        self.session.write("gsm voice on\r\n")
        if self._checkAnswer(0):
            self.session.write("gsm data off\r\n")
            self._checkAnswer(1)
        else:
            self._logger.error("Error: Cannot make GSM voice on")
            

    def _simulate2Gto3G(self):
        """ Simulate a 2G to 3G connection """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Simulating 2G to 3G for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Simulating 2G to 3G"),
        self.session.write("gsm voice on\r\n")
        if self._checkAnswer(0):
            self.session.write("gsm data on\r\n")
            self._checkAnswer(1)
   

    def _sendSensorAcceleration(self):
        """ Simulate a sensor acceleration """
        Analysis.reportEvent(self.reporter, self.idXp, "Emulator", "Sending sensor acceleration for emulator: {0}".format(self.__emulatorSerialNumber))
        self._logger.debug("Sending a sensor acceleration"),
        self.session.write("sensor set acceleration 10\r\n")
        self._checkAnswer(1)
        self.session.write("sensor set orientation 10\r\n") #--> this is disabled for emulator?
        if not self._checkAnswer(0):
            self._logger.warning("Emulator doesn't seem to implement sensor orientation")

    @property
    def emulator(self):
        return self.__emulator

    @emulator.setter
    def emulator(self, emulator):
        if emulator is None:
            raise Exception("Emulator is null.")
        self.__emulator = emulator
    
    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session):
        if session is None:
            raise Exception("Telnet session is null.")
        self.__session = session

    @property
    def emulatorNumber(self):
        return self.__emulatorNumber

    @emulatorNumber.setter
    def emulatorNumber(self, emuNumber):
        if emuNumber is None:
            raise Exception("Emulator number is null.")
        self.__emulatorNumber = emuNumber

    @property
    def reporter(self):
        return self.__reporter

    @reporter.setter
    def reporter(self, reporter):
        if reporter is None:
            raise Exception("Reporter is null.")
        self.__reporter = reporter

    @property
    def idXp(self):
        return self.__idXp

    @idXp.setter
    def idXp(self, idxp):
        if idxp is None:
            raise Exception("idXp is null")
        self.__idXp = idxp
