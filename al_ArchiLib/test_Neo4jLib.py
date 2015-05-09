#!/usr/bin/python
#
# al_ArchiLib Testing
#
__author__ = u'morrj140'
__VERSION__ = u'0.2'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from Constants import *
from Neo4JLib import *

import pytest

@pytest.fixture(scope=u"module")
def gdb():
    return gdbTest

@pytest.fixture(scope=u"module")
def graph(gdb):
    return Neo4JLib(gdbTest)

@pytest.mark.Neo4J
def _executeQuery(qs, graph):

    lq = graph.cypherQuery(qs)

    return lq

@pytest.mark.Neo4J
def test_BusinessObjects(graph):
    qs = u"MATCH (n:`BusinessObject` {name :'Inventory'}) RETURN n"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessObject'})--m-->(o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessObject'}) -- (m {typeName : 'RealisationRelationship'}) -- (o {typeName: 'DataObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName: 'DataObject'}) RETURN n, m, count(o)"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessObject'})--m--(o {typeName:'Requirement'}) RETURN n, count(o)"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessObject'})-- m -- (o {typeName:'Requirement'}) RETURN n, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

@pytest.mark.Neo4J
def test_ApplicationService(graph):
    qs = u"MATCH (n:`ApplicationService`)-[r1]-m-[r2]-o RETURN n, r1, m, r2, o "
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'ApplicationService'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationComponent'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

@pytest.mark.Neo4J
def test_BusinessProcess(graph):

    qs = u"MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'AccessRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n {typeName:'BusinessProcess'}) -- (m {typeName : 'UsedByRelationship'}) -- (o {typeName: 'ApplicationService'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

@pytest.mark.Neo4J
def test_BusinessEvent(graph):
    qs = u"MATCH (n {typeName:'BusinessEvent'}) -- (m {typeName : 'TriggeringRelationship'}) -- (o {typeName: 'BusinessProcess'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

@pytest.mark.Neo4J
def test_Requirement(graph):
    qs = u"MATCH (n {typeName:'Requirement'}) -- (m {typeName : 'AssociationRelationship'}) -- (o {typeName: 'BusinessObject'}) RETURN n, m, o"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

@pytest.mark.Neo4J
def goQueryGraph(graph):

    qs = u"MATCH n RETURN n LIMIT 5"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

    qs = u"MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
    lq = _executeQuery(qs, graph)
    logger.info(u"%d : %s" % (len(lq), qs))

if __name__ == u"__main__":

    goQueryGraph(graph())
