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


class ReportingConfiguration(object):
    """A container that stores all the parameters required for reporting
    """

    def __init__(self, elasticsearchMode, elasticsearchIp, elasticsearchPort, elasticsearchIndex, elasticsearchDoctype, fileMode):        
        self.elasticsearchMode = elasticsearchMode
        self.elasticsearchIp = elasticsearchIp
        self.elasticsearchPort = elasticsearchPort
        self.elasticsearchIndex = elasticsearchIndex
        self.elasticsearchDoctype = elasticsearchDoctype
        self.fileMode = fileMode
    
    @staticmethod
    def build(commandLineParser):
        """Builds and returns a ReportingConfiguration based on values
        contained in the specified CommandLineParser"""
        if commandLineParser is None:
            raise Exception("Cannot build the reporting configuration if no commandLineParser is provided")

        reportingOptions = commandLineParser.reportingOptions

        esMode = False
        esIp = None
        esPort = 0
        esIndex = None
        esDoctype = None
        fileMode = False

        # parses elasticsearch mode
        if 'elasticsearch_mode' in reportingOptions.keys():
            if reportingOptions['elasticsearch_mode'].lower() == 'true':
                esMode=True
                
        if esMode:
            # elasticsearch ip
            if not 'elasticsearch_ip' in reportingOptions.keys():
                raise Exception("ElasticSearch mode is activated, but no 'elasticsearch_ip' specified.")
            esIp = reportingOptions['elasticsearch_ip']

            # elasticsearch port
            if not 'elasticsearch_port' in reportingOptions.keys():
                raise Exception("ElasticSearch mode is activated, but no 'elasticsearch_port' specified.")
            esPort = reportingOptions['elasticsearch_port']

            # elasticsearch index
            if not 'elasticsearch_index' in reportingOptions.keys():
                raise Exception("ElasticSearch mode is activated, but no 'elasticsearch_index' specified.")
            esIndex = reportingOptions['elasticsearch_index']

            # elasticsearch doctype
            if not 'elasticsearch_doctype' in reportingOptions.keys():
                raise Exception("ElasticSearch mode is activated, but no 'elasticsearch_doctype' specified.")
            esDoctype = reportingOptions['elasticsearch_doctype']

        # parses file mode
        if 'file_mode' in reportingOptions.keys():
            if reportingOptions['file_mode'].lower() == 'true':
                fileMode = True
                
        return ReportingConfiguration(esMode, esIp, esPort, esIndex, esDoctype, fileMode)

    def __str__(self):
        """toString method"""
        lines = [
            "Reporting Conf:",
            "\t+ Elasticsearch",
            "\t\t- Active\t{0}".format(self.elasticsearchMode),
            "\t\t- IP\t\t{0}".format(self.elasticsearchIp),
            "\t\t- TCP Port\t{0}".format(self.elasticsearchPort),
            "\t\t- ES Index\t{0}".format(self.elasticsearchIndex),
            "\t\t- ES Doctype\t{0}".format(self.elasticsearchDoctype),                        
            "\t+ File mode",
            "\t\t- Active\t{0}".format(self.fileMode)
            ]
        return '\n'.join(lines)
        
    @property
    def elasticsearchMode(self):
        """Activate or not the elasticsearch mode
        """
        return self.__elasticsearchMode

    @elasticsearchMode.setter
    def elasticsearchMode(self, elasticsearchMode):
        if elasticsearchMode is None:
            elasticsearchMode = False
            
        self.__elasticsearchMode = elasticsearchMode
        
    @property
    def elasticsearchIp(self):
        """IP of the elasticsearch database
        """
        return self.__elasticsearchIp

    @elasticsearchIp.setter
    def elasticsearchIp(self, elasticsearchIp):
        if elasticsearchIp is None:
            elasticsearchIp = "0.0.0.0"
        self.__elasticsearchIp = elasticsearchIp
                
    @property
    def elasticsearchPort(self):
        """Port of the elasticsearch database
        """
        return self.__elasticsearchPort

    @elasticsearchPort.setter
    def elasticsearchPort(self, elasticsearchPort):
        if elasticsearchPort is None:
            elasticsearchPort = 0
        self.__elasticsearchPort = elasticsearchPort

    @property
    def elasticsearchIndex(self):
        """Index of the elasticsearch database
        """
        return self.__elasticsearchIndex

    @elasticsearchIndex.setter
    def elasticsearchIndex(self, elasticsearchIndex):
        if elasticsearchIndex is None:
            if self.__elasticsearchMode == 'True':
                raise Exception("An elasticsearch index must be set")
        self.__elasticsearchIndex = elasticsearchIndex

    @property
    def elasticsearchDoctype(self):
        """Doctype of the elasticsearch database
        """
        return self.__elasticsearchDoctype

    @elasticsearchDoctype.setter
    def elasticsearchDoctype(self, elasticsearchDoctype):
        if elasticsearchDoctype is None:
            if self.__elasticsearchMode == 'True':
                raise Exception("An elasticsearch doctype must be set")
        self.__elasticsearchDoctype = elasticsearchDoctype
        
    @property
    def fileMode(self):
        """Activate or not the file mode
        """
        return self.__fileMode

    @fileMode.setter
    def fileMode(self, fileMode):
        if fileMode is None:
            fileMode = False
        self.__fileMode = bool(fileMode)
        
