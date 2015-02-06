#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import logging

from py2neo.neo4j import Node

from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet as worksheet

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

class Neo4JLib(object):

    def __init__(self):
        # gdb defined in al_ArchiLib
        logger.debug("Neo4J instance : %s" % gdb)

        self.graph = Neo4JGraph(gdb)
        self.csvFileExport = csvFileExport

        self.fileExcelIn  = fileExcelIn
        self.fileExcelOut = fileExcelOut
        self.fileNodes    = "nodes.p"

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
        lq, qd = self.cypherQuery(qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))


    def queryExportExcel(self, lq, fileIn=None, fileOut=None, wst=None):

        if fileIn == None:
            fileIn = self.fileExcelIn

        if fileOut == None:
            fileOut = self.fileExcelIn

        wb = load_workbook(filename = fileIn)

        if wst == None:
            wsTitle = "Import Items" + time.strftime("%Y%d%m_%H%M%S")
        else:
            wsTitle = wst

        ws = wb.create_sheet()
        ws.title = wsTitle

        logger.info("Created Worksheet %s" % wsTitle)

        n = 0
        for x in lq:
            n += 1

            logger.debug("x in lq : %s" % x)

            m = 0
            for y in x:
                m += 1

                col = get_column_letter(m)
                logger.debug("col : %s" % col)

                logger.debug("y : %s" % y)

                rs = "%s%s" % (col, n)
                logger.debug("%s : %s" % (rs, y))

                ws.cell(rs).value = ("%s" % (y))

        wb.save(filename = fileOut)

        logger.info("Saved file : %s" % fileOut)


    def exportNeo4JToConcepts(self, concepts):
        # #et all nodes
        # Match n return n limit 25

        qs = "Match n return n"

        lq, qd = self.cypherQuery(qs)

        for x in lq:
            if len(x) == 2:
                logger.info("%s[%s]" % (x[0], x[1]))
                concepts.addConceptKeyType(x[0], x[1])
            else:
                logger.warn("Not a standard node : %s" % x)

        # Match r relations
        qs = "match n-[r]-m return n, r, m"
        lq, qd = self.cypherQuery(qs)

        for x in lq:
            if len(x) == 6:
                logger.info("%s[%s]" % (x[0], x[1]))
                concepts.addConceptKeyType(x[0], x[1])
            else:
                logger.warn("Not a standard node : %s" % x)

        Concepts.saveConcepts(concepts, self.fileNodes)

if __name__ == "__main__":
    nj = Neo4JLib()
    nj.Neo4JCounts()