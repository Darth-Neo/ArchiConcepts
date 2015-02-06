#! /usr/bin/python
#
# Estimate Scope_Items Export
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import datetime
import time
import logging
from nl_lib import Logger
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet as worksheet

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib


if __name__ == "__main__":
    nj = Neo4JLib()

    qs = "MATCH "
    qs = qs +    "(n0:ApplicationFunction)-- (r0)"
    qs = qs + "-- (n1:ApplicationComponent)--(r1)"
    qs = qs + "-- (n2:ApplicationService)--  (r2)"
    qs = qs + "-- (n3:BusinessProcess)--     (r3)"
    qs = qs + "-- (n4:BusinessObject) "
    qs = qs + "Return n0, r0, n1, r1, n2, r2, n3, r3, n4, n4.PageRank, n4.RequirementCount, n4.Degree"

    lq, qd = nj.cypherQuery(qs)

    nj.queryExportExcel(lq)

    logger.info("%d rows returned" % len(lq))