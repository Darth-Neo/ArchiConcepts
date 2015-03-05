#!/usr/bin/python
#
# Neo4J Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'


from Constants import *
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)
from nl_lib.Concepts import Concepts
from py2neo import neo4j, node, rel
from py2neo.neo4j import Node
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet as worksheet

import pytest

class Neo4JLib(object):

    def __init__(self, gdb):
        logger.debug("Neo4J instance : %s" % gdb)

        self.graph = neo4j.GraphDatabaseService(gdb)

        self.fileCSVExport = fileCSVExport

    def cypherQuery(self, qs):
        query = neo4j.CypherQuery(self.graph, qs)
        return query.execute().data

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

        query = neo4j.CypherQuery(self.graph, qs)

        qd = query.execute().data

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
        f = open(self.fileCSVExport,'w')

        self.logResults(lq, f)

        f.close()

        logger.info("Exported %d rows" % len(lq))
        logger.info("Save Model : %s" % self.fileCSVExport)

    def Neo4JCounts(self):
        qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = self.cypherQuery(qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))


    def queryExportExcel(self, lq, fileIn=fileExcelIn, fileOut=fileExcelOut):

        wb = load_workbook(filename = fileIn)

        wsTitle = "Import Items" + time.strftime("%Y%d%m_%H%M%S")

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


    def exportNeo4JToConcepts(self, concepts, fileNodes="nodes.p"):
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

        Concepts.saveConcepts(concepts, fileNodes)

        return concepts

def test_Neo4jLib():
    nj = Neo4JLib(gdbTest)
    nj.Neo4JCounts()

if __name__ == "__main__":
    test_Neo4jLib()