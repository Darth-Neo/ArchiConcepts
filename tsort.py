#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree
import lxml

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

dictElement = dict()
dictName = dict()

try:
    from functools import reduce
except:
    pass

data = {
    'des_system_lib':   set('std synopsys std_cell_lib des_system_lib dw02 dw01 ramlib ieee'.split()),
    'dw01':             set('ieee dw01 dware gtech'.split()),
    'dw02':             set('ieee dw02 dware'.split()),
    'dw03':             set('std synopsys dware dw03 dw02 dw01 ieee gtech'.split()),
    'dw04':             set('dw04 ieee dw01 dware gtech'.split()),
    'dw05':             set('dw05 ieee dware'.split()),
    'dw06':             set('dw06 ieee dware'.split()),
    'dw07':             set('ieee dware'.split()),
    'dware':            set('ieee dware'.split()),
    'gtech':            set('ieee gtech'.split()),
    'ramlib':           set('std ieee'.split()),
    'std_cell_lib':     set('ieee std_cell_lib'.split()),
    'synopsys':         set(),
    }

def toposort2(data):
    for k, v in data.items():
        v.discard(k) # Ignore self dependencies

    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item,dep in data.items() if not dep)
        if not ordered:
            break
        yield ' '.join(sorted(ordered))
        data = {item: (dep - ordered) for item,dep in data.items()
                if item not in ordered}
    #assert not data, "A cyclic dependency exists amongst %r" % data

def logXML(el, i=3, n=0):
    if i==0:
        return

    spaces = " " * n
    n = n + 1

    logger.debug("%se.%d.%s - %s" % (spaces, i, el.tag, el.text))

    spaces = " " * n
    n = n + 1

    attributes = el.attrib
    for atr in attributes:
        logger.debug("%sa.%d.%s = %s" % (spaces, i, atr, attributes[atr]))

    #("archimate:CompositionRelationship", "archimate:AggregationRelationship",
    # # "archimate:AssignmentRelationship", "archimate:AssociationRelationship" )

    if attributes.has_key(ARCHI_TYPE):
        if attributes[ARCHI_TYPE] in \
                                ("archimate:FlowRelationship") : #,
                                #  "archimate:TriggeringRelationship",
                                #  "archimate:AccessRelationship",
                                #  "archimate:UsedByRelationship"):

            sourceID = int(attributes["source"], 16)
            targetID = int(attributes["target"], 16)

            if dictElement.has_key(sourceID):
                l = dictElement[sourceID]
                l.append(targetID)
                dictElement[sourceID] = l
            else:
                l = list()
                l.append(targetID)
                dictElement[sourceID] = l

            logger.debug(" source:%s" % (logID(sourceID)))
            logger.debug(" target:%s" % (logID(targetID)))

    i = i - 1
    for elm in el:
        logXML(elm, i, n)

def logFolder(tree, folder):
    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        logXML(x, i=6)

def logID(id):
    try:
        n = dictName[id]
        return ("%s:%s:%s:%s" % (n.tag, n.get("name"), n.get("id"), n.get(ARCHI_TYPE)))
    except:
        return ""

def logNode(n):

    attributes = n.attrib

    logger.debug("%s:%s:%s:%s" % (n.tag, n.get("name"), n.get("id"), n.get(ARCHI_TYPE)))
    try:

        if attributes.get("id") != None:
            id = int(attributes["id"], 16)
            dictName[id] = n
    except:
        pass

    for y in n:
        logNode(y)

def logAll(tree):
    for x in tree.getroot():
        logNode(x)

if __name__ == '__main__':
    #fileArchimate = "/Users/morrj140/Development/GitRepository/DirCrawler/DNX Phase 2 0.9.archimate"

    fileArchimate = "/Users/morrj140/PycharmProjects/ArchiConcepts/CodeGen_v10.archimate"

    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    logAll(tree)

    logFolder(tree, "Relations")

    dt = dict()

    for x in dictElement.keys():
        sourceID = x

        tt = set()

        targetID = dictElement[x]
        for y in targetID:

            if y != None:
                tt.add(str(y));

                #logger.info("sourceID:%s \t target:%s" % (logID(sourceID), logID(y)))
                logger.debug("%s \t %s" % (sourceID, y))
                logger.debug("%s" % tt)

        dt[str(x)] = tt
        logger.debug("dt = %s" % dt)

    r = toposort2(dt)

    output = list()
    for x in r:
        #logger.info("x : %s" % x)
        for y in x.split():
            logger.debug("y : %s" % y)

            n = dictName[int(y)]
            logger.debug("%s" % (n.get("name")))

            output.insert(0, n.get("name"))

    for x in output:
        if x != "Junction":
            logger.info("%s" % x)