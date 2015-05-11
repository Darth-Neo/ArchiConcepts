#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.Neo4JLib import Neo4JLib


def exportNeo4j(gdb):

    # measure process time, wall time
    start_time = ArchiLib.startTimer()

    concepts = Concepts(u"Neo4J", u"Neo4J Graph DB")

    nj = Neo4JLib(gdb)

    nj.exportNeo4JToConcepts(concepts)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    exportNeo4j(gdb)

