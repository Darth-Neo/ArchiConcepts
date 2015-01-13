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

from al_ArchiLib import *

import al_ExportArchi  as EA
import al_ImportNeo4J  as IN
import al_AnalyzeGraph as AG

if __name__ == "__main__":

    exportConcepts = EA.al_ExportArchi()

    IN.importNeo4J(exportConcepts)

    AG.analyzeNetworkX(exportConcepts)