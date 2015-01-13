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

from al_ArchiLib import *

import al_ExportArchi as EA
import al_AnalyzeGraph as AG

logger = Logger.setupLogging(__name__)

logger.setLevel(logging.INFO)

if __name__ == "__main__":

    concepts = EA.al_ExportArchi()

    AG.graphConcepts(concepts)


