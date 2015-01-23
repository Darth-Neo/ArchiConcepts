#! /usr/bin/python
#
# Natural Language Processing of Neo4J Information
#
__author__ = 'morrj140'

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

from al_ArchiLib import *
from al_Neo4JCounts import *

def Traversal(ql):

    qs = "MATCH"
    n=0
    for x in ql:
        qs = qs + " (n%d:%s) -- (r%d) --" % (n, x, n)
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

    for x in qd:

        logger.debug("%s[%d]" % (x, n))

        n += 1

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

        if f != None:
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

    Neo4JCounts()

    #
    # Useful Cypher Queries
    #
    #UpdateQuery = "match (n0 {typeName:'BusinessObject', name:'Contract'}) set n0.PageRank = 1 return n"
    #demoQuery1 = "MATCH (n0:Stakeholder)-- (r0)-- (n1:WorkPackage)--(r1)--(n2:BusinessObject) RETURN n0, r0, n1, r1, n2"
    #demoQuery2 = "MATCH (n0:WorkPackage)--(r0)--(n1:ApplicationComponent)--(r1)--(n2:ApplicationService)--(r2)--(n3:BusinessProcess) where n1.name = 'Contract Management' RETURN n0, r0, n1, r1, n2, r2, n3"

    ql = list()

    if False:
        ql.append("ApplicationFunction")
        ql.append("ApplicationComponent")
        ql.append("ApplicationService")
        ql.append("BusinessProcess")
        qs = Traversal(ql)

    elif True:
        ql.append("BusinessObject")
        ql.append("BusinessProcess")
        ql.append("ApplicationService")
        qs = Traversal(ql)

    elif False:
        qs1 = "MATCH (n0:BusinessEvent)-- (r0)-- (n1:BusinessProcess) -- (r1) -- (n2:BusinessObject)  RETURN n0, r0, n1, r1, n2"
        qs2 = "MATCH (n0:BusinessProcess)--(r0)--(n1:ApplicationService)--(r1)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n0, r0, n1, r1, n2, r2, n3"
        qs3 = "MATCH (n0:WorkPackage)--(r0)--(n1:BusinessProcess) RETURN n0, r0, n1"
        qs4 = "MATCH (n0:ApplicationService)--(r0)--(n2:ApplicationComponent)--(r2)--(n3:DataObject) RETURN n1,r1,n2, r2, n3"
        qs5 = "MATCH (n0:BusinessObject)--(r0)--(n1:DataObject) RETURN n0, r0, n1"
        qs6 = "MATCH (n0:BusinessProcess)--(r0)--(n1: BusinessObject)--(r1)--(n2:DataObject)--(r2)--(n3: ApplicationComponent) RETURN n0, r0, n1, r1, n2, r2, n3"

    elif False:
        #qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, r0, n1"
        #qs = "MATCH (n0:BusinessObject)--(r0)--(n1:Requirement) RETURN n0, count(n1)"
        qs = "MATCH (n0:BusinessObject)--(r0:AssociationRelationship)--(n1:Requirement)  RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count, count(n1) ORDER BY count(n1) DESC"
        #qs = "MATCH (n0:BusinessObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"
        #qs = "MATCH (n0:DataObject) RETURN n0, n0.PageRank, n0.RequirementCount, n0.Degree, n0.count"

    else:
        qs = "match (n0:WorkPackage) --(r0)--(n1:BusinessProcess)--(r1)--(n2:ApplicationService) where n0.name='Batch %d'  return n0, r0, n1,r1, n2" % (1)

    lq, qd = cypherQuery(graph, qs)

    queryExport(lq)
