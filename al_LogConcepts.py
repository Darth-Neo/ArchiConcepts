#!/usr/bin/python
#
# Concept Logging
#
__author__ = 'morrj140'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

from al_ArchiLib import *

if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "documentsSimilarity.p"
    conceptFile = "GapsSimilarity.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #conceptFile = "traversal.p"
    #conceptFile = "batches.p"
    #conceptFile = "export.p"
    #conceptFile = "req.p"
    #conceptFile = "Systems.p"
    #conceptFile = "Contract Management.p"
    #conceptFile = "Estimation20142212_180938.p"
    #conceptFile = "pptx.p"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/Research_20141709_104529"
    directory = os.getcwd()

    #filePath = dir + os.sep + conceptFile
    filePath = directory + os.sep + conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    #concepts.logConcepts()

    distribution = dict()

    for x in concepts.getConcepts().values():
        logger.info("%s" % x.name)
        for y in x.getConcepts().values():
            logger.info("%s" % y.name)

            strCommon = ""
            for z in y.getConcepts().values():
                logger.info("%s" % z.name)
                strCommon = strCommon + " " + z.name

        if distribution.has_key(strCommon):
            distribution[strCommon] += 1
        else:
            distribution[strCommon] = 1

    listCommon = list()
    for x in distribution:
        logger.info("%s : %d" % (x, distribution[x]))
        dl = list()
        dl.append(x)
        dl.append(distribution[x])
        listCommon.append(dl)

    for x in sorted(listCommon, key=lambda c: abs(c[1]), reverse=False):
            logger.info("  %d - %s" % (x[1], x[0]))


    #concepts.printConcepts(list)
    #Concepts.outputConceptsToCSV(concepts, fileExport)



        




