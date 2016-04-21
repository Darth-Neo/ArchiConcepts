#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.DedupArchimateXML import *
from al_lib.ArchiLib import ArchiLib
from al_lib.Constants import *


if __name__ == u"__main__":

    pathModel = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models"

    fileArchimateXML = u"DVC v3.19.archimate"
    # fileArchimateXML = u"Solution_Engineering_Template_V8.archimate"
    # fileArchimateXML = u"RTPv9.archimate"

    fileArchimate = pathModel + os.sep + fileArchimateXML

    fileArchimateOutput = os.getcwd() + os.sep + fileArchimateXML[:-10] + u"_dedup.archimate"

    da = DedupArchimateXML(fileArchimate)
    da.Dedup(fileArchimateOutput)

    n = 0
    while True:
        try:
            logger.info (u"%s - %s" % (da._typeCountStart[n], da._typeCountEnd[n]))
            n += 1

        except Exception, msg:
            logger.warn(u"Goodbye. - %s")
            break




