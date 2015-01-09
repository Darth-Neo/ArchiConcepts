#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = 'morrj140'

import os
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

import al_ExportArchi as ExportArchi
import al_AnalyzeGraph as GraphConcepts

logger = Logger.setupLogging(__name__)

logger.setLevel(logging.INFO)

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"

    concepts = ExportArchi.al_ExportArchi(fileArchimate)

    GraphConcepts.graphConcepts(concepts)


