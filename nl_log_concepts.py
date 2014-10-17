#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

logger = Logger.setupLogging(__name__)
   
if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    conceptFile = "topicsDict.p"
    #conceptFile = "documentsSimilarity.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #
    #conceptFile = "pptx.p"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/Research_20141709_104529"
    #dir = os.getcwd()#

    #filePath = dir + os.sep + conceptFile
    filePath = conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    #concepts.logConcepts()

    n = 0
    for x in concepts.getConcepts().values():
        n += 1
        logger.info("x %s[%s]" % (x.name, x.typeName))
        for y in x.getConcepts().values():
            logger.info("  y %s[%s]" % (y.name, y.typeName))
            for z in y.getConcepts().values():
                if not (z.name in ("h", "l", "t", "w")):
                    logger.info("    z  %s[%s]" % (z.name, z.typeName))

    #concepts.printConcepts()
    
        




