#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
import logging
from nl_lib import Logger

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, GraphVizGraph, Neo4JGraph
from nl_lib.Constants import *

from al_ArchiLib import *

import al_DependancyAnalysisFromArchi as DA
import al_ExportArchi  as EA
import al_ImportConceptsIntoNeo4J  as IN
import al_AnalyzeGraph as AG

import al_Neo4JCounts as NC

if __name__ == "__main__":

    # measure process time, wall time
    t0 = time.clock()
    start_time = time.time()

    al = ArchiLib()
    al.logTypeCounts()

    logger.info("...Export Archi...")
    concepts, al = EA.al_ExportArchi(al)

    logger.info("...Import Neo4J...")

    if  CleanNeo4j == True:
        IN.importNeo4J(concepts, ClearNeo4J=True)
    else:
        IN.importNeo4J(concepts)

    logger.info("...Neo4J Counts...")
    NC.Neo4JCounts()

    #logger.info("...Analyze NetworkX...")
    #if  CleanNeo4j == True:
    #    AG.analyzeNetworkX(concepts)
    #else:
    #    AG.analyzeNetworkX()

    #measure wall time
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info("Start time : %s" % strStartTime)

    end_time = time.time()

    strEndTime = time.asctime(time.localtime(end_time))
    logger.info("End   time : %s" % strEndTime)

    # measure process time
    timeTaken = end_time - start_time

    minutes = timeTaken / 60
    hours = minutes / 60
    logger.info("Process Time = %4.2f seconds, %d Minutes, %d hours" % (timeTaken, minutes, hours))