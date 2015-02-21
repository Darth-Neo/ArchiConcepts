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

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Neo4JLib import Neo4JLib
from al_Constants import *

if __name__ == "__main__":
    logger.info("Neo4J instance : %s" % gdb)
    nj = Neo4JLib(gdb)

    qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
    lq, qd = nj.cypherQuery(qs)

    logger.info("Neo4J Counts")
    for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
        logger.info("%4d : %s" % (x[2], x[0]))