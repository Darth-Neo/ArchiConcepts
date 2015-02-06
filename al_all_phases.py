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
from al_ArchiLib.ArchiLib import ArchiLib as AL
from al_ArchiLib.DependencyAnalysis import DependencyAnalysis as DA
from al_ArchiLib.ExportArchi import ExportArchi as EA
from al_ArchiLib.ImportNeo4J import ImportNeo4J as IN
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph as AG
from al_ArchiLib.Neo4JLib import Neo4JLib as NL

if __name__ == "__main__":

    start_time = AL.startTimer()

    al = AL.ArchiLib()
    al.logTypeCounts()

    logger.info("...Export Archi...")
    concepts, al = EA.al_ExportArchi(al)

    logger.info("...Import Neo4J...")

    if  AL.CleanNeo4j == True:
        IN.importNeo4J(concepts, ClearNeo4J=True)
    else:
        IN.importNeo4J(concepts)

    logger.info("...Neo4J Counts...")
    NL.Neo4JCounts()

    logger.info("...Analyze NetworkX...")
    ag = AG.AnalyzeGraph()
    if  CleanNeo4j == True:
        ag.analyzeNetworkX(concepts)
    else:
        ag.analyzeNetworkX()

    AL.stopTimer(start_time)