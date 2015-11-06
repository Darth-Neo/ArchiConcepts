#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.DedupArchimateXML import *
from al_lib.ArchiLib import ArchiLib
from al_lib.Constants import *


if __name__ == u"__main__":

    # fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v3.17.archimate"
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/Solution_Engineering_Template_V8.archimate"
    fileArchimateOutput = os.getcwd() + os.sep + u"dedup.archimate"

    da = DedupArchimateXML(fileArchimate)
    da.Dedup(fileArchimateOutput)

    n = 0
    while True:
        try:
            logger.info (u"%s - %s" % (da._typeCountStart[n], da._typeCountEnd[n]))
            n += 1

        except Exception, msg:
            logger.warn(u"Goodbye.")
            break




