#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = 'morrj140'

import os
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)

import time
import json

from py2neo.neo4j import GraphDatabaseService, CypherQuery, Node, Relationship

logger.setLevel(logging.INFO)

cypher_ExampleQuery = "MATCH n RETURN n LIMIT 5"
cypherDeleteNodesQuery = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
cypherBusinessObjectQuery = "MATCH (n:`BusinessObject` {name :'Inventory'}) RETURN n"
cypherApplicationServiceQuery = "MATCH (n:`ApplicationService`)-[r1]-m-[r2]-o RETURN n, r1, m, r2, o "


# MATCH (n {name :'Inventory', typeName:'BusinessObject'})-->m RETURN count(m)

if __name__ == "__main__":
    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    graph = Neo4JGraph(gdb)
    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    #qs = cypheApplicationServiceQuery
    #qs = cypherBusinessObjectQuery

    qs = "MATCH (n {typeName:'BusinessObject'})--m-->(o {typeName: 'BusinessProcess'}) RETURN n, m, o"

    qd = graph.query(qs)

    listQuery = list()

    for x in qd:
        n = 0
        logger.debug("%s[%d]" % (x, n))

        xl = list()

        for v in x.values:

            n += 1
            spaces = " " * n

            name = v["name"]
            typeName =v["typeName"]

            if n == 2:
                name = name[:-57]

            if name != None and typeName != None:
                logger.debug("%s%s[%s]" % (spaces, name, typeName))

            l = list()
            l.append(name)
            l.append(typeName)

            xl.append(l)
        listQuery.append(xl)

    #qd = graph.query(cypherDeleteNodesQuery)

    nl = sorted(listQuery, key=lambda c: c[0], reverse=False)

    for x in nl:
        logger.info("%s->%s->%s" % (x[0][0], x[1][0], x[2][0]))



