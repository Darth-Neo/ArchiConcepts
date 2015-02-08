#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import time
import logging

from py2neo.neo4j import GraphDatabaseService, CypherQuery, Node, Relationship

from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.Neo4JLib import Neo4JLib as NL

class Neo4JLib(object):

    def __init__(self):
        # gdb defined in al_ArchiLib
        logger.debug("Neo4J instance : %s" % gdb)

        self.graph = Neo4JGraph(gdb)
        self.csvFileExport = csvFileExport

    def Traversal(self, ql):

        qs = "MATCH"
        n=0
        for x in ql:
            qs = qs + " (n%d:%s)--(r%d:relation)--" % (n, x, n)
            n += 1

        qr = " Return"
        for m in range(0, n, 1):
            qr = qr + " n%s, r%d," % (m, m)

        query = qs[:-11] + qr[:-5]

        logger.info("%s" % query)

        return query

    def cypherQuery(self, qs):

        qd = self.graph.query(qs)

        listQuery = list()

        n = 0

        ColHdr = True

        for x in qd:

            n += 1

            logger.debug("%s[%d]" % (x, n))

            if n == 1:
                cl = list()
                m = 0
                for y in x.columns:
                    m += 1
                    logger.debug("  %s[%d]" % (y, m))
                    cl.append(y)
                    cl.append("Type%d" % m)

                listQuery.append(cl)

                continue

            xl = list()

            for v in x.values:

                if isinstance(v, Node):
                    name = v["name"][:40]
                    typeName =v["typeName"]

                    xl.append(name)
                    xl.append(typeName)

                elif isinstance(v, int) or isinstance(v, float):
                    count = v
                    typeName ="Number"

                    xl.append(count)
                    xl.append(typeName)

                elif isinstance(v, str) or isinstance(v, unicode):
                    st = v
                    typeName ="String"

                    xl.append(st)
                    xl.append(typeName)

            listQuery.append(xl)

        return listQuery, qd


    def logResults(self, lq, f=None, n=0):
        n += 1

        spaces = " " * n

        rs = ""
        for x in lq:
            if isinstance(x, tuple) or isinstance(x, list):
                self.logResults(x, f, n)

            elif isinstance(x, str) or isinstance(x, unicode):
                if x == "Nodes" or x is None or len(x) == 0:
                    continue
                logger.debug("%s %s" % (spaces, x))
                rs += ", %s" % (x)

            elif isinstance(x, float) or isinstance(x, int):
                logger.debug("%s %s" % (spaces, x))
                rs += ", %s" % (x)

        if len(rs) != 0:
            logger.info("%s" % (rs[1:]))
            f.write("%s\n" % (rs[1:]))

    def queryExport(self, lq):

        # csvExport defined in al_ArchiLib.Constants
        f = open(self.csvFileExport,'w')

        self.logResults(lq, f)

        f.close()

        logger.info("Exported %d rows" % len(lq))
        logger.info("Save Model : %s" % self.csvFileExport)

    def Neo4JCounts(self):
        qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = self.cypherQuery(self.graph, qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))

if __name__ == "__main__":
    nj = Neo4JLib()
    nj.Neo4JCounts()