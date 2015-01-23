#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'

import os
import time
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib import *

import al_QueryGraph as QG

def Neo4JCounts():
    # gdb defined in al_ArchiLib
    logger.info("Neo4J instance : %s" % gdb)
    graph = Neo4JGraph(gdb)

    qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
    lq, qd = QG.cypherQuery(graph, qs)

    for x in lq:
        logger.info("%26s\t%d" % (x[0], x[2]))

    #CG.logResults(lq)

if __name__ == "__main__":
    Neo4JCounts()