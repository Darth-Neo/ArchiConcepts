#!/usr/bin/python
#
# Natural Language Processing of Information
#
__author__ = 'morrj140'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

from al_ArchiLib import *

def recurseConcepts(concepts, depth, n=0):

    if n == depth:
        return

    try:
        n += 1
        spaces = ' ' * n
        for x in concepts.getConcepts().values():
            if n != 1:
                logger.debug("%s%s:%s" % (spaces, x.name, x.typeName))
            recurseConcepts(x, depth, n)
    except:
        logger.info("depth, %d n" % (depth, n))


        return

def lineCSV(concepts, cstr=None, n=0):
    n += 1

    spaces = " " * n

    if cstr == None:
        rs = "%s," % concepts.name
    else:
        rs = cstr

    logger.debug("%s%d[%s]" % (spaces, n, rs))

    if len(concepts.getConcepts().values()) == 0:
        return rs + "\n"

    for c in concepts.getConcepts().values():
        rs = rs + lineCSV(c, cstr)
        logger.debug("%s%s[%s]" % (spaces, n, rs))

    logger.debug("%s%d[%s]" % (spaces, n, rs))

    return rs

def outputConceptsToCSV(concepts, fileExport):
    n = 0

    #f = open(fileExport,'w')
    #f.write("Model, Source, Type, Relationship, type, Target, Type\n")

    for c in concepts.getConcepts():
        n += 1
        fl = lineCSV(concepts, None)
        logger.info("fl : %s[%s]" % (fl[:-1], n))

    #f.close()
    #logger.info("Save Model : %s" % fileExport)

if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "documentsSimilarity.p"
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
    conceptFile = "Estimation20142212_180938.p"

    fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +".csv"

    #
    #conceptFile = "pptx.p"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/Research_20141709_104529"
    #dir = os.getcwd()#

    #filePath = dir + os.sep + conceptFile
    filePath = conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()
    #concepts.printConcepts()
    #recurseConcepts(concepts, 3)

    #outputConceptsToCSV(concepts, fileExport)



        




