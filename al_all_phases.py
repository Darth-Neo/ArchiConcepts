#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'

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
import al_ImportNeo4J  as IN
import al_AnalyzeGraph as AG

import al_Neo4JCounts as NC

if __name__ == "__main__":

    # measure process time, wall time
    t0 = time.clock()
    t1 = time.time()

    al = ArchiLib()
    al.logTypeCounts()

    logger.info("...Export Archi...")
    concepts, al = EA.al_ExportArchi()

    logger.info("...Import Neo4J...")
    concepts = IN.importNeo4J(concepts, ClearNeo4J=True)

    logger.info("...Neo4J Counts...")
    NC.Neo4JCounts()

    logger.info("...Analyze NetworkX...")
    AG.analyzeNetworkX()

    logger.info("...Neo4J Counts...")
    NC.Neo4JCounts()

    logger.info("...Analyze Dependencies...")
    conceptBatches = DA.dependancyAnalysis()
    IN.importNeo4J(conceptBatches, ClearNeo4J=False)

    logger.info("***Neo4J Counts...")
    NC.Neo4JCounts()

    #measure wall time
    localtime = time.asctime( time.localtime(t1))
    logger.info("Start      time : %s" % localtime)

    localtime = time.asctime( time.localtime(time.time()) )
    logger.info("Completion time : %s" % localtime)

    # measure process time
    timeTaken = (time.clock() - t0)
    minutes = timeTaken / 60
    hours = minutes / 60
    logger.info("Process Time = %4.2f seconds, %d Minutes, %d hours" % (timeTaken, minutes, hours))