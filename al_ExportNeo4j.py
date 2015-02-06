#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import logging
from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

if __name__ == "__main__":

    # measure process time, wall time
    start_time = ArchiLib.startTimer()

    concepts = Concepts("Neo4J", "Neo4J Graph DB")

    nj = Neo4JLib()
    nj.exportNeo4JToConcepts(concepts)

    ArchiLib.stopTimer(start_time)

