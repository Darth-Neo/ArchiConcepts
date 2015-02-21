#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

import pytest

def exportNeo4j(gdb):

    # measure process time, wall time
    start_time = ArchiLib.startTimer()

    concepts = Concepts("Neo4J", "Neo4J Graph DB")

    nj = Neo4JLib(gdb)

    nj.exportNeo4JToConcepts(concepts)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    exportNeo4j(gdbTest)

