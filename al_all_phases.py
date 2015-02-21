#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.2'

import sys
import os
import StringIO
import time
import logging
from nl_lib import Logger

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportArchi import ExportArchi
from al_ArchiLib.ConceptsImportNeo4J import ConceptsImportNeo4J
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph
from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v27.archimate"

    al = ArchiLib(fileArchimate)

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    logger.info("...Export Archi...")
    concepts = ea.exportArchi()

    logger.info("...Import Neo4J...")
    in4j = ConceptsImportNeo4J(ClearNeo4J=True)
    in4j.importNeo4J(concepts)

    logger.info("...Analyze NetworkX...")
    ag = AnalyzeGraph(gdb)
    ag.analyzeNetworkX(concepts)

    ArchiLib.stopTimer(start_time)