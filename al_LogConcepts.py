#!/usr/bin/python
#
# Concept Logging
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

def distribution(concepts, tc=None):
    distribution = dict()
    strCommon = ""

    if tc != None:
        topicList = [[x.name, x.count] for x in tc.getConcepts().values()]
        topicSortedList = sorted(topicList, key=lambda c: c[1], reverse=False)
        topics = [ a[0] for a in topicSortedList]

    # Document
    for x in concepts.getConcepts().values():
        logger.debug("%s[%d]" % (x.name, x.count))

        # Topic
        for y in x.getConcepts().values():
            logger.debug("%s" % y.name)

            lls = [z.name.lower() for z in y.getConcepts().values()]

            lss = sorted(lls, key=lambda c: c, reverse=False)

            strCommon = " ".join([x for x in lss]).replace(".", "")

        if distribution.has_key(strCommon):
            distribution[strCommon] += 1
        else:
            distribution[strCommon] = 1

    listCommon = sorted([ x for x in distribution.items() ], key=lambda c: c[1], reverse=False)

    lcd = [ [y, x.count(" ") + 1, x] for x, y in listCommon if y > 2]

    for x, y, z in lcd:
        logger.info("%d[%d] : %s" % (x, y, z))
        
        words = [a for a in z.split(" ")]
        if len(words) > 0:
            for w in words:
                if ((tc != None) and (w in topics)) :
                    topicCount = [q[1] for q in topicList if q[0] == w]
                    logger.info("  Topic : %s[%d]" % (w, topicCount[0]))

if __name__ == "__main__":

    #conceptFile = "topicsDict.p"
    #conceptFile = "GapsSimilarity.p"
    conceptFile  = "chunks.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #conceptFile = "traversal.p"
    #conceptFile = "batches.p"
    #conceptFile = "export.p"
    #conceptFile = "req.p"

    directory = os.getcwd()

    filePath = directory + os.sep + conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()
    #concepts.printConcepts(list)
    #Concepts.outputConceptsToCSV(concepts, fileExport)

    logger.info("Distribution Analysis")
    tc = Concepts.loadConcepts("topicsDict.p")
    #distribution(concepts, tc)
    distribution(concepts)

        




