#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

from ArchiLib import ArchiLib
from Neo4JLib import Neo4JLib
from Constants import *

import pytest

class ConceptsImportNeo4J(object):

    def __init__(self, fileArchimate, gdb, ClearNeo4J=False):

        self.ClearNeo4J = ClearNeo4J

        self.al = ArchiLib(fileArchimate)
        self.nj = Neo4JLib(gdb)

        if ClearNeo4J == True:
            self.clearNeo4J()

        logger.info("Neo4J instance : %s" % gdb)
        self.graph = Neo4JGraph(gdb)

        if ClearNeo4J == True:
            self.graph.clearGraphDB()


    def addGraphNodes(self, concepts, n=0, threshold=1):
        n += 1
        for c in concepts.getConcepts().values():
            logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

            c.name = c.name.replace("\"", "'")

            self.graph.addConcept(c)

            if len(c.getConcepts()) > threshold:
                self.addGraphNodes(c, n)

    def addGraphEdges(self, concepts, n=0):
        n += 1

        self.graph.addConcept(concepts)

        for c in concepts.getConcepts().values():

            logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

            c.name = c.name.replace("\"", "'")

            self.graph.addConcept(c)

            self.graph.addEdge(concepts, c, c.typeName)

            self.addGraphEdges(c, n)

    def logGraph(self, gl, title, scale=1):
        pr = 0
        len_pr = len(gl)
        sum_pr = 0.0
        try:
            logger.info("---%s---[%d]" % (title, len(gl)))

            n = 0
            for x in gl:
                n += 1
                if isinstance(gl, dict) and x != None:
                    sum_pr = gl[x]
                    if gl[x] > pr:
                        pr = gl[x]

                    logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

                else:
                    logger.info("%s [%d]" % (x, n))
        except:
            logger.warn("Ops...")

        logger.info("Len gl[x]=%3.4f" % len_pr)
        logger.info("Max gl[x]=%3.4f" % pr)
        logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

    def clearNeo4J(self):
        if not gdbTest == None:
            logger.info("Reset Neo4J Graph DB")

            call([resetNeo4J])

    def importNeo4J(self, concepts):

        logger.info("Adding Neo4J nodes to the graph ...")
        self.addGraphNodes(concepts)

        logger.info("Adding Neo4J edges to the graph ...")
        self.addGraphEdges(concepts)

        self.graph.setNodeLabels()

        if self.ClearNeo4J:
            DropNode = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
            self.nj.cypherQuery(DropNode)

        CountRequirements = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName:'Requirement' }) with n, count(o) as rc  set n.RequirementCount=rc RETURN n.name, rc order by rc desc"
        self.nj.cypherQuery(CountRequirements)

def conceptsImportNeo4J():

    logger.info("Using : %s" % fileConceptsExport)

    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    in4j = ConceptsImportNeo4J(fileArchimateTest, gdbTest, ClearNeo4J=True)

    in4j.importNeo4J(importConcepts)


if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    conceptsImportNeo4J()

    ArchiLib.stopTimer(start_time)






