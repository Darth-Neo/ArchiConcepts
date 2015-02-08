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

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportArchi import ExportArchi
from al_ArchiLib.ConceptsImportNeo4J import ConceptsImportNeo4J
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph
from al_ArchiLib.Neo4JLib import Neo4JLib

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    al = ArchiLib()
    al.logTypeCounts()

    nj = Neo4JLib()
    nj.Neo4JCounts()

    ea = ExportArchi(al)

    logger.info("...Export Archi...")
    concepts, al = ea.exportArchi()

    logger.info("...Import Neo4J...")

    in4j = ConceptsImportNeo4J(ClearNeo4J=True)
    in4j.importNeo4J(concepts)


    logger.info("...Neo4J Counts...")
    nj.Neo4JCounts()

    logger.info("...Analyze NetworkX...")
    ag = AnalyzeGraph()

    if  CleanNeo4j == True:
        ag.analyzeNetworkX(concepts)
    else:
        ag.analyzeNetworkX()

    ArchiLib.stopTimer(start_time)