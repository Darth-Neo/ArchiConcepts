#! /usr/bin/python
#
# Estimate Scope_Items Export
#
__author__ = 'morrj140'
import datetime
import logging
from nl_lib import Logger
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet as worksheet

from al_ArchiLib import *
import al_QueryGraph as QG

def queryExportExcel(lq, fileIn, fileOut):

    wb = load_workbook(filename = fileIn)

    ws = wb.create_sheet()

    ws.title = "Scope Items"
    m = 0
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
            logger.info("Row %d \t rs : %s : %s" % (n, rs, y))

            ws.cell(rs).value = ("%s" % (y))

    wb.save(filename = fileOut)

    logger.info("Saved file : %s" % fileOut)

if __name__ == "__main__":
    fileIn = 'Template_Estimate.xlsx'
    fileOut = 'Template_Estimate_new.xlsx'

    graph = Neo4JGraph(gdb)

    ql = list()
    ql.append("ApplicationFunction")
    ql.append("ApplicationComponent")
    ql.append("ApplicationService")
    qs = QG.Traversal(ql)

    lq, qd = QG.cypherQuery(graph, qs)

    queryExportExcel(lq, fileIn, fileOut)