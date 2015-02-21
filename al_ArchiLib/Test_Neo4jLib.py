#!/usr/bin/python
#
# al_ArchiLib Testing
#
__author__ = 'morrj140'
__VERSION__ = '0.2'

from Logger import *

logger = setupLogging(__name__)
logger.setLevel(INFO)

from Neo4JLib import *
from Constants import *

import pytest

@pytest.fixture(scope="module")
def graph():
    return Neo4JLib(gdbTest)

def _executeQuery(qs, graph):

    lq = graph.cypherQuery(qs)

    return lq

def test_BusinessObjects(graph):
    qs = "MATCH (n:`BusinessObject` {name :'Inventory'}) RETURN n"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessObject'})--m-->(o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'RealisationRelationship'}) -- (o {typeName: 'DataObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName: 'DataObject'}) RETURN n, m, count(o)"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessObject'})--m--(o {typeName:'Requirement'}) RETURN n, count(o)"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessObject'})-- m -- (o {typeName:'Requirement'}) RETURN n, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

def test_ApplicationService(graph):
    qs = "MATCH (n:`ApplicationService`)-[r1]-m-[r2]-o RETURN n, r1, m, r2, o "
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'ApplicationService'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationComponent'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

def test_BusinessProcess(graph):

    qs = "MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'AccessRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationService'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

def test_BusinessEvent(graph):
    qs = "MATCH (n {typeName:'BusinessEvent'}) -- (m {typeName : 'TriggeringRelationship'}) -- (o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

def test_Requirement(graph):
    qs = "MATCH (n {typeName:'Requirement'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

def goQueryGraph(graph):

    qs = "MATCH n RETURN n LIMIT 5"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

    qs = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
    lq = _executeQuery(qs, graph)
    logger.info("%d : %s" % (len(lq), qs))

if __name__ == "__main__":
    goQueryGraph(graph())
