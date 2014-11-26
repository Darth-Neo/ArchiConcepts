#!/usr/bin/python
#
# Natural Language Processing of Information
#
__author__ = 'morrj140'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

logger = Logger.setupLogging(__name__)

def recurseConcepts(concepts, depth, n=0):

    if n == depth:
        return

    try:
        n += 1
        spaces = ' ' * n
        for x in concepts.getConcepts().values():
            if n != 1:
                logger.info("%s%s:%s" % (spaces, x.name, x.typeName))
            recurseConcepts(x, depth, n)
    except:
        logger.info("depth, %d n" % (depth, n))
        return
if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    #conceptFile = "topicsDict.p"
    conceptFile = "documentsSimilarity.p"
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

    #
    #conceptFile = "pptx.p"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/Research_20141709_104529"
    #dir = os.getcwd()#

    #filePath = dir + os.sep + conceptFile
    filePath = conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    #concepts.logConcepts()
    concepts.printConcepts()
    #recurseConcepts(concepts, 3)

        




