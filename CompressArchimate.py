__author__ = 'morrj140'

#!/usr/bin/python
#
#  Clean Archimate Relationships
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

def compressArchimate(fileArchimate):

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    dp = al.findProperties()

    n = 0

    for bad in dp:
        n += 1
        parent = bad.getparent().remove(bad)
        logger.info("%d - %s" % (n, bad))

    al.outputXMLtoFile(filename=u"clean.archimate")


if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v44.archimate"

    compressArchimate(fileArchimate)
