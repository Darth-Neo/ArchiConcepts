#! /usr/bin/python
#
# Estimate Scope_Items Export
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

import pytest

def createEstimate(gdb):
    nj = Neo4JLib(gdb)

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

if __name__ == "__main__":
    createEstimate(gdbTest)