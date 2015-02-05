#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import time
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

import al_ArchiLib as AL
import al_QueryGraph as QG

def Neo4JCounts():
    # gdb defined in al_ArchiLib
    logger.info("Neo4J instance : %s" % AL.gdb)
    graph = Neo4JGraph(AL.gdb)

    qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
    lq, qd = QG.cypherQuery(graph, qs)

    logger.info("Neo4J Counts")
    for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
        logger.info("%4d : %s" % (x[2], x[0]))

if __name__ == "__main__":
    Neo4JCounts()