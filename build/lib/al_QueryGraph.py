#! /usr/bin/python
#
# Query Neo4J Information in Cypher
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import logging
import time
import json

from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from py2neo.neo4j import GraphDatabaseService, CypherQuery, Node, Relationship

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet

from al_ArchiLib import *
from al_Neo4JCounts import *

def Traversal(ql):

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

def getColumnHeaders(qs):
    pass

def cypherQuery(graph, qs):

    qd = graph.query(qs)

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


def logResults(lq, f=None, n=0):
    n += 1

    spaces = " " * n

    rs = ""
    for x in lq:
        if isinstance(x, tuple) or isinstance(x, list):
            logResults(x, f, n)

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

def queryExport(lq):

    # csvExport defined in al_ArchiLib
    f = open(csvFileExport,'w')

    logResults(lq, f)

    f.close()

    logger.info("Exported %d rows" % len(lq))
    logger.info("Save Model : %s" % csvFileExport)

if __name__ == "__main__":
    # gdb defined in al_ArchiLib
    logger.debug("Neo4J instance : %s" % gdb)

    graph = Neo4JGraph(gdb)

    # measure process time, wall time
    t0 = time.clock()

    start_time = time.time()

    Neo4JCounts()

    #
    # Useful Cypher Queries
    #
    #UpdateQuery = "match (n0 {typeName:'BusinessObject', name:'Contract'}) set n0.PageRank = 1 return n"
    #demoQuery1 = "MATCH (n0:Stakeholder)-- (r0)-- (n1:WorkPackage)--(r1)--(n2:BusinessObject) RETURN n0, r0, n1, r1, n2"
    #demoQuery2 = "MATCH (n0:WorkPackage)--(r0)--(n1:ApplicationComponent)--(r1)--(n2:ApplicationService)--(r2)--(n3:BusinessProcess) where n1.name = 'Contract Management' RETURN n0, r0, n1, r1, n2, r2, n3"

    #delNodes = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"

    ql = list()

    if True:
        # Determine order of service development based on the dependancy analysis done on Business Processes
        #qs="match (l:ApplicationService)--(r0:Relation)-- (n:BusinessProcess)--(r1:Relation)--(m:WorkPackage) return m,l,n order by m.name"
        # Try with Application Component as well
        qs="match (i:DataObject)--(r0:Relation) -- (j:ApplicationComponent)--(r1:Relation)--(l:ApplicationService)--(r2:Relation)-- (n:BusinessProcess)--(r3:Relation)--(m:WorkPackage) return m,n,l,j,i order by m.name"

    elif True:
        # Determine the business process ordering by the magnitude of the reqiurements
        qs="match (i:Requirement)--(r1:Relation)--(j:BusinessObject)--(r2:Relation)--(k:BusinessProcess)--(r3:Relation)--(l:WorkPackage) return l,k,j,count(i) order by l.name"

    elif False:
        # Determine a Business Scenario's associciation to Business Processes
        #qs = "match (n0:BusinessEvent) --> (r0:TriggeringRelationship) --> (n1:BusinessProcess) --> (r1:TriggeringRelationship) --> (n2:BusinessEvent) return n0, r0, n1, r1,  n2"
        qs = "match (n0:BusinessEvent) --> (r0:Relation)--> (n1:BusinessProcess) -[*1..10]-> (r1:FlowRelationship) --> (n2:BusinessProcess) return n0, n1, n2 order by n0.name"

    elif False:
        qs = "MATCH (n0:BusinessObject) --> (r0:Relation) --> (n1:BusinessProcess) "
        qs = qs + "where (toint(substring(n1.name, 0, 1)) is null ) "
        qs = qs + "return n0.name, n1.name order by n0.name desc"

    elif True:
        qs = "match (n:BusinessProcess) <-- (r0:Relation) <-- (m:ApplicationService) "
        qs = qs + "with n, m, count(r) as cr "
        qs = qs + " where cr > 0 "
        qs = qs + " return n.name, m.name, cr"

    elif False:
        qs = "MATCH (n:Requirement) <-- (r0:Relation) <-- (n0:BusinessObject) --> (r1:Relation) -->  (n1:BusinessProcess) "
        qs = qs + "where (toint(substring(n1.name, 0, 1)) is null ) "
        qs = qs + "return count(n), n0.name, n0.Degree, n0.PageRank, n1.name, n1.Degree, n1.PageRank order by n0.name desc"

    elif False:
        ql.append("ApplicationFunction")
        ql.append("ApplicationComponent")
        ql.append("ApplicationService")
        qs = Traversal(ql)

    elif False:
        ql.append("BusinessObject")
        ql.append("BusinessProcess")
        ql.append("ApplicationService")
        ql.append("ApplicationComponent")
        ql.append("ApplicationFunction")
        qs = Traversal(ql)

    elif False:
        ql.append("WorkPackage")
        ql.append("BusinessProcess")
        ql.append("ApplicationService")
        ql.append("ApplicationComponent")
        ql.append("ApplicationFunction")
        qs = Traversal(ql)

    elif False:
        qs1 = "MATCH (n0:BusinessEvent)-- (r0)-- (n1:BusinessProcess) -- (r1) -- (n2:BusinessObject)  RETURN n0, r0, n1, r1, n2"
        qs2 = "MATCH (n0:BusinessProcess)--(r0)--(n1:ApplicationService)--(r1)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n0, r0, n1, r1, n2, r2, n3"
        qs3 = "MATCH (n0:WorkPackage)--(r0)--(n1:BusinessProcess) RETURN n0, r0, n1"
        qs4 = "MATCH (n0:ApplicationService)--(r0)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n1,r1,n2, r2, n3"
        qs5 = "MATCH (n0:BusinessObject)--(r0)--(n1:DataObject) RETURN n0, r0, n1"
        qs6 = "MATCH (n0:BusinessProcess)--(r0)--(n1: BusinessObject)--(r1)--(n2:DataObject)--(r2)--(n3: ApplicationComponent) RETURN n0, r0, n1, r1, n2, r2, n3"
        qs7 = "MATCH (n:Requirement)<--() <-- (n0:BusinessObject) --> () --> (n1:BusinessProcess) <-- () <-- (n2:ApplicationService)-->()-->(n3:ApplicationComponent)-->()-->(n4:ApplicationFunction) Return n0, count(n), n1, n2, n3, n4 order by count(n) desc, n0.name"
        qs = qs7

    elif False:
        qs = "MATCH    (n:Requirement)           <--() "
        qs = qs + "<-- (n0:BusinessObject)      --> ()"
        qs = qs + "--> (n1:BusinessProcess)     <-- ()"
        qs = qs + "<-- (n2:ApplicationService)   -->()"
        qs = qs + "--> (n3:ApplicationComponent) -->()"
        qs = qs + "--> (n4:ApplicationFunction) "
        qs = qs + "Return n0, count(n), n1, n2, n3, n4 "
        qs = qs + "order by count(n) desc, n0.name"

    elif False:
        qs = "MATCH    (n0:BusinessObject)      --> ()"
        qs = qs + "--> (n1:BusinessProcess)     <-- ()"
        qs = qs + "<-- (n2:ApplicationService)   -->()"
        qs = qs + "--> (n3:ApplicationComponent) -->()"
        qs = qs + "--> (n4:ApplicationFunction) "
        qs = qs + "Return n0, n1, n2, n3, n4 "
        qs = qs + "order by n0.name desc"

    elif False:
        #qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, r0, n1"
        qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, count(n1) ORDER BY count(n1) DESC"
        #qs = "MATCH (n0:BusinessObject)--(r0:AssociationRelationship)--(n1:Requirement)  RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count, count(n1) ORDER BY count(n1) DESC"
        #qs = "MATCH (n0:BusinessObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"
        #qs = "MATCH (n0:DataObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"

    else:
        qs = "match (n0:WorkPackage) --(r0)--(n1:BusinessProcess)--(r1)--(n2:ApplicationService) where n0.name='Batch %d'  return n0, r0, n1,r1, n2" % (1)

    lq, qd = cypherQuery(graph, qs)

    queryExport(lq)

    #measure wall time
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info("Start time : %s" % strStartTime)

    end_time = time.time()

    strEndTime = time.asctime(time.localtime(end_time))
    logger.info("End   time : %s" % strEndTime)

    # measure process time
    timeTaken = end_time - start_time

    minutes = timeTaken / 60
    hours = minutes / 60
    logger.info("Process Time = %4.2f seconds, %d Minutes, %d hours" % (timeTaken, minutes, hours))

