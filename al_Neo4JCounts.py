#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.Neo4JLib import Neo4JLib


def neo4jCounts():

    logger.info(u"Neo4J instance : %s" % gdb)
    nj = Neo4JLib(gdb, fileCSVExport)

    sl = nj.neo4jCounts()

    for x in sl:
        if len(x) == 2:
            logger.info(u"%4d : %s" % (x[1], x[0]))
        else:
            logger.error(u"List of wrong length : %d" % len(x))

    return sl

if __name__ == u"__main__":
    sl = neo4jCounts()