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

logger.setLevel(logging.INFO)

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

def logResults(lq, fileOut=None, n=0):
    n += 1

    spaces = " " * n

    rs = ""
    for x in lq:
        if isinstance(x, tuple) or isinstance(x, list):
            logResults(x,  n)

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

        if fileOut != None:
            f.write("%s\n" % (rs[1:]))




if __name__ == "__main__":
    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    graph = Neo4JGraph(gdb)
    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    demoQuery = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) RETURN n, m, o,p, q"

    #UpdateQuery = "match (n {typeName:'BusinessObject', name:'Contract'}) set n.PageRank = 1 return n"

    #qs = "MATCH n RETURN n LIMIT 5"
    #qs = "MATCH (n:`ApplicationService`)-[r1]-m-[r2]-o RETURN n, r1, m, r2, o "
    #qs = "MATCH (n {typeName:'BusinessObject'})--m-->(o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'BusinessEvent'}) -- (m {typeName : 'TriggeringRelationship'}) -- (o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'AccessRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationService'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'ApplicationService'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationComponent'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'Requirement'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'RealisationRelationship'}) -- (o {typeName: 'DataObject'}) RETURN n, m, o"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName: 'DataObject'}) RETURN n, m, count(o)"
    #qs = "MATCH (n {typeName:'BusinessObject'})--m--(o {typeName:'Requirement'}) RETURN n, count(o)"
    #qs = "MATCH (n {typeName:'BusinessObject'})-- m -- (o {typeName:'Requirement'}) RETURN n, o"
    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m {typeName:'CompositionRelationship'})-- (o {typeName:'Stakeholder'}) RETURN n, o"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName:'Requirement' })  RETURN n, count(m) ORDER BY count(m) DESC"
    #qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName:'WorkPackage' }) RETURN n,m,o"
    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) RETURN n, m, o,p, q"
    #qs = "MATCH (n {typeName:'Stakeholder'})-- (m )-- (o {typeName:'WorkPackage'}) -- (p) -- (q {typeName:'BusinessObject'}) -- r -- (s {typeName:'Requirement'}) RETURN n, m, o,p, q, r, count(s)"
    #qs = "MATCH (n {typeName:'WorkPackage'})-- (m {typeName:'AssociationRelationship'})-- (o {typeName:'Stakeholder'}) RETURN n, o"

    lq, qd = cypherQuery(graph, qs)

    fileExport = "ExportQuery.csv"

    f = open(fileExport,'w')

    logResults(lq, f)

    f.close()
    logger.info("Save Model : %s" % fileExport)