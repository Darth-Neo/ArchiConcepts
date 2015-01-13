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

def Traversal(ql):

    qs = "MATCH"
    n=0
    for x in ql:
        qs = qs + " (n%d {typeName:'%s'}) --" % (n, x)
        n += 1

    qr = " Return"
    for m in range(0, n, 1):
        qr = qr + " n%s," % m

    query = qs[:-3] + qr[:-1]

    logger.info("%s" % query)

    #qs = "MATCH (n {typeName:'BusinessObject'})-- m -- (o {typeName:'Requirement'}) RETURN n, o"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName: 'DataObject'}) RETURN n, m, count(o)"
    #qs = "MATCH (n {typeName:'BusinessObject'})--m--(o {typeName:'Requirement'}) RETURN n, count(o)"

    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m {typeName:'AssociationRelationship'})-- (o {typeName:'ApplicationFunction'}) RETURN n, o"
    qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName:'Requirement' })  RETURN n, count(m) ORDER BY count(m) DESC"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName:'WorkPackage' }) RETURN n,m,o"
    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) RETURN n, m, o,p, q"
    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) -- r -- (s {typeName:'Requirement'}) RETURN n, m, o,p, q, r, count(s)"
    #qs = "MATCH (n {typeName:'WorkPackage'})-- (m {typeName:'AssociationRelationship'})-- (o {typeName:'Stakeholder'}) RETURN n, o"

    return query

def cypherQuery(graph, qs):

    qd = graph.query(qs)

    listQuery = list()

    for x in qd:
        n = 0
        logger.debug("%s[%d]" % (x, n))

        xl = list()

        for v in x.values:

            n += 1
            spaces = " " * n

            if isinstance(v, Node):
                name = v["name"][:40]
                typeName =v["typeName"]

                if n == 2:
                    name = name[:-57]

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

            #if name != None and typeName != None:
            #    logger.debug("%s%s[%s]" % (spaces, name, typeName))

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
    f = open(csvExport,'w')

    logResults(lq, f)

    f.close()

    logger.info("Save Model : %s" % csvExport)


if __name__ == "__main__":
    # gdb defined in al_ArchiLib
    logger.info("Neo4J instance : %s" % gdb)
    graph = Neo4JGraph(gdb)

    #demoQuery = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) RETURN n, m, o,p, q"
    #UpdateQuery = "match (n {typeName:'BusinessObject', name:'Contract'}) set n.PageRank = 1 return n"
    #demoQuery = "MATCH (l {typeName:'BusinessProcess'}) -- w --  (n {typeName:'ApplicationService'}) -- m -- (o {typeName: 'ApplicationComponent'}) -- r -- (q {typeName: 'DataObject'}) RETURN l, w, n, m, o, r, q"

    ql = list()
    ql.append("BusinessEvent")
    ql.append("TriggeringRelationship")
    ql.append("BusinessProcess")
    ql.append("FlowRelationship")
    ql.append("BusinessProcess")
    ql.append("AccessRelationship")
    ql.append("BusinessObject")
    ql.append("UsedByRelationship")
    ql.append("ApplicationService")
    #ql.append("UsedByRelationship")
    #ql.append("ApplicationComponent")
    #ql.append("RealisationRelationship")
    #ql.append("DataObject")

    qs = Traversal(ql)

    lq, qd = cypherQuery(graph, qs)

    queryExport(lq)
