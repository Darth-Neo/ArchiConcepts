#!/usr/bin/python
#
# Archimate to Neo4J
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

import al_ExportArchi  as EA
import al_ImportNeo4J  as IN
import al_AnalyzeGraph as AC

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v18.archimate"

    exportConcepts = EA.al_ExportArchi(fileArchimate)

    IN.importNeo4J(exportConcepts)

    AC.analyzeConcepts(exportConcepts)