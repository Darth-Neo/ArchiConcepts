#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time

import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, GraphVizGraph, Neo4JGraph
from nl_lib.Constants import *
import networkx as nx

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph
from al_ArchiLib.Neo4JLib import Neo4JLib

if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    ag = AnalyzeGraph()
    ag.analyzeNetworkX()

    ArchiLib.stopTimer(start_time)

    



