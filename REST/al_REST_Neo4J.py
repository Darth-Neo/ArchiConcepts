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

    # Example : http://localhost:7474/db/data/node/1

    # Connection Info
    server = "localhost:7474"

    # node
    nodeID = 1

    action = "GET"
    params = urllib.urlencode({'node': 1,})
    headers = {"Content-type": "application/json;", }

    # Queries
    serviceRoot = "/db/data"
    nodeQuery = "%s/node/%d" % (serviceRoot, nodeID)
    nodeProperties = nodeQuery + "/properties/aname"
    nodePropKeys = "%s/propertykeys" % serviceRoot

    uri = nodeQuery

    logger.info("Using : http://%s" % server)

    connection = httplib.HTTPConnection(server)

    connection.request(action, uri, params, headers)

    response = connection.getresponse()

    logger.info("Result %s : %s" % (response.status, response.reason))

    result = response.read()

    logger.info("response: %s" % result)

    connection.close()
