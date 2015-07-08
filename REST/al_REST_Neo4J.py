#! /usr/bin/python
#
# Query Neo4J Via REST Calls
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

import urllib2
import time
import datetime
import json
import httplib
import urllib

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

# Example : http://localhost:7474/db/data/node/1

# Connection Info
server = u"localhost:7474"

NEO4J_REST = {
  u"extensions": {},
  u"node": server + u"/db/data/node",
  u"node_index": server + u"/db/data/index/node",
  u"relationship_index": server + u"/db/data/index/relationship",
  u"extensions_info": server + u"/db/data/ext",
  u"relationship_types": server + u"/db/data/relationship/types",
  u"batch": server + u"/db/data/batch",
  u"cypher": server + u"/db/data/cypher",
  u"indexes": server + u"/db/data/schema/index",
  u"constraints": server + u"/db/data/schema/constraint",
  u"transaction": server + u"/db/data/transaction",
  u"node_labels": server + u"/db/data/labels",
  u"neo4j_version": u"2.1.2"
}

if __name__ == u"__main__":
    # node
    nodeID = 1

    actionGet = u"GET"
    actionPost = u"POST"
    actionPut = u"PUT"
    action = actionGet

    headers = {u"Content-type": u"application/json;", u"Accept": u"application/json; charset=UTF-8"}

    # Queries
    serviceRoot = u"/db/data"
    nodeQuery = u"%s/node/%d" % (serviceRoot, nodeID)
    nodeInstance = u"%s/node" % (serviceRoot)
    nodeProperties = u"%s%s" % (nodeQuery,  u"/properties/typeName")
    nodePropKeys = u"%s/propertykeys" % serviceRoot
    nodeDegree = u"%s/node/%d/degree/all" % (serviceRoot, nodeID)

    params = urllib.urlencode({ u'query': u'MATCH (n) return n.typeName limit 50', u'params': {}})
    cypherQuery = u"%s/cypher" % serviceRoot

    params = urllib.urlencode({u"typeName": u"Library"})

    uri = nodeDegree

    logger.info(u"Using : http://%s" % server)
    logger.info(u"      params : %s" % params)
    connection = httplib.HTTPConnection(server)
    connection.request(action, uri, params, headers)
    response = connection.getresponse()

    logger.info(U"Result Status %s : %s" % (response.status, response.reason))

    result = response.read()

    logger.info(u"response: %s" % result)

    connection.close()
