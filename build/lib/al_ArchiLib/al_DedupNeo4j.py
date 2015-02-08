#!/usr/bin/python
#
# Neo4J Dedup
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

from al_ArchiLib import *
import al_QueryGraph as QG
import al_Neo4JCounts as NC

def Neo4JDedups():
    # gdb defined in al_ArchiLib
    logger.info("Neo4J instance : %s" % gdb)
    graph = Neo4JGraph(gdb)

    logger.info("Before Dedup")
    NC.Neo4JCounts()

    DropDuplicates = "match p=(n)--(r0:Relation), q=(m)--(r1:Relation) where n.name = m.name and n.typeName = m.typeName delete m, r1"
    QG.cypherQuery(graph, DropDuplicates)

    logger.info("After Dedup")
    NC.Neo4JCounts()

if __name__ == "__main__":
    Neo4JDedups()
