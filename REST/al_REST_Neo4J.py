#! /usr/bin/python
#
# Query Neo4J Via REST Calls
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

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

NEO4J_REST = {
  "extensions": {},
  "node": "http://localhost:7474/db/data/node",
  "node_index": "http://localhost:7474/db/data/index/node",
  "relationship_index": "http://localhost:7474/db/data/index/relationship",
  "extensions_info": "http://localhost:7474/db/data/ext",
  "relationship_types": "http://localhost:7474/db/data/relationship/types",
  "batch": "http://localhost:7474/db/data/batch",
  "cypher": "http://localhost:7474/db/data/cypher",
  "indexes": "http://localhost:7474/db/data/schema/index",
  "constraints": "http://localhost:7474/db/data/schema/constraint",
  "transaction": "http://localhost:7474/db/data/transaction",
  "node_labels": "http://localhost:7474/db/data/labels",
  "neo4j_version": "2.1.2"
}

if __name__ == "__main__":

    # Connection Info
    server = "localhost:7474"

    # node
    nodeID = 1

    actionGet = "GET"
    actionPost = "POST"
    actionPut = "PUT"
    action = actionGet

    headers = {"Content-type": "application/json;", "Accept" : "application/json; charset=UTF-8"}

    # Queries
    serviceRoot = "/db/data"
    nodeQuery = "%s/node/%d" % (serviceRoot, nodeID)
    nodeInstance = "%s/node" % (serviceRoot)
    nodeProperties = nodeQuery + "/properties/aname"
    nodePropKeys = "%s/propertykeys" % serviceRoot
    nodeDegree = "%s/node/%d/degree/all" % (serviceRoot, nodeID)

    if False:
        params = urllib.urlencode({ 'query' : 'MATCH n:BusinessProcess return n.aname', 'params' : {}})
        cypherQuery = "%s/cypher" % serviceRoot

    params = urllib.urlencode({ "typeName" : "BusinessProcess"})

    uri = nodeDegree

    logger.info("Using : http://%s" % server)
    logger.info("      params : %s" % params)

    connection = httplib.HTTPConnection(server)

    connection.request(action, uri, params, headers)

    response = connection.getresponse()

    logger.info("Result %s : %s" % (response.status, response.reason))

    result = response.read()

    logger.info("response: %s" % result)

    connection.close()
