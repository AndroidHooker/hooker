#!/usr/bin/env python

from Market import Market

class PandaapMarket(Market):

    NAME = "Pandaap"
    URL = "http://android.pandaapp.com/"
    DESC = "No description yet."
    
    def __init__(self):
        super(PandaapMarket, self).__init__(PandaapMarket.NAME, PandaapMarket.URL, PandaapMarket.DESC)


        

    

    


