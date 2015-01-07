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

cypheQuery = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"

if __name__ == "__main__":
    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    graph = Neo4JGraph(gdb)
    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    #qs = "MATCH n RETURN n LIMIT 5"
    qs = "MATCH (n:`ApplicationService`)-[r1]-m-[r2]-o RETURN n, r1, m, r2, o "

    qd = graph.query(qs)

    for x in qd:
        n = 0
        logger.debug("%s[%d]" % (x, n))

        for v in x.values:

            n += 1
            spaces = " " * n

            name = v["name"]
            typeName =v["typeName"]

            if typeName != None and typeName == "Edge":
                name = name[:-56]

            if name != None and typeName != None:
                logger.info("%s%s[%s]" % (spaces, name, typeName))





