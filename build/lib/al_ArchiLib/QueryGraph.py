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

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib as AL
from al_ArchiLib.Neo4JLib import Neo4JLib as NL

if __name__ == "__main__":
        start_time = AL.startTimer()

        nj = NL.Neo4JLib()

        qg = nj.QueryGraph()

        nj.Neo4JCounts()

        ql = list()
        qs="match (i:DataObject)--(r0:Relation) -- (j:ApplicationComponent)--(r1:Relation)--(l:ApplicationService)--(r2:Relation)-- (n:BusinessProcess)--(r3:Relation)--(m:WorkPackage) return m,n,l,j,i order by m.name"

        lq, qd = nj.cypherQuery(qs)
        nj.queryExport(lq)

        AL.stopTimer(start_time)