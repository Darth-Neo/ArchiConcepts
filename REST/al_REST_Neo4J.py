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

if __name__ == "__main__":

    # Example : http://localhost:7474/db/data/node/1

    # Connection Info
    server = "localhost"
    port = 7474
    nodeID = 1
    action = "GET"

    #params = urllib.urlencode({'node': 1, 'eggs': 2, 'bacon': 0})
    params = urllib.urlencode({'node': 1,})
    headers = {"Content-type": "application/json;", }

    # Queries
    serviceRoot = "/db/data"
    nodeQuery = "%s/node/%d" % (serviceRoot, nodeID)
    nodeProperties = nodeQuery + "/properties/aname"
    nodePropKeys = "%s/propertykeys" % serviceRoot

    uri = nodeQuery

    logger.info("Using : %s" % server)

    connection = httplib.HTTPConnection(server, port)

    connection.request(action, uri, None, headers)

    response = connection.getresponse()

    logger.info("Result %s : %s" % (response.status, response.reason))

    result = response.read()

    logger.info("response: %s" % result)

    connection.close()
