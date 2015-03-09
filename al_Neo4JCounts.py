#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.Neo4JLib import Neo4JLib
from al_Constants import *

import pytest

def neo4jCounts():

    logger.info("Neo4J instance : %s" % gdb)
    nj = Neo4JLib(gdb, fileCSVExport)

    qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
    lq, qd = nj.cypherQuery(qs)

    logger.info("Neo4J Counts")
    for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
        logger.info("%4d : %s" % (x[2], x[0]))

if __name__ == "__main__":
    neo4jCounts()