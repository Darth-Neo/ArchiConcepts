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

# The graph nodes
class Task(object):
    def __init__(self, name, depends):
        self.__name    = name
        self.__depends = set(depends)

    @property
    def name(self):
        return self.__name

    @property
    def depends(self):
        return self.__depends

# "Batches" are sets of tasks that can be run together
def get_task_batches(nodes):

    # Build a map of node names to node instances
    name_to_instance = dict( (n.name, n) for n in nodes )

    # Build a map of node names to dependency names
    name_to_deps = dict( (n.name, set(n.depends)) for n in nodes )

    # This is where we'll store the batches
    batches = []

    n = 0

    # While there are dependencies to solve...
    while name_to_deps:

        n += 1

        # Get all nodes with no dependencies
        ready = {name for name, deps in name_to_deps.iteritems() if not deps}

        logger.debug("ready : %s" % ready)

        # If there aren't any, we have a loop in the graph
        if not ready:
            msg  = "Circular dependencies found!\n"
            msg += format_dependencies(name_to_deps)

            logger.warn("  %s" % ValueError(msg))

        # Remove them from the dependency graph
        for name in ready:
            del name_to_deps[name]

        for deps in name_to_deps.itervalues():
            deps.difference_update(ready)

        # Add the batch to the list
        listBatch = {name_to_instance[name] for name in ready}

        if len(listBatch) == 0:
            return batches

        batches.append(listBatch )

        logger.debug("%d batches : %s" % (len(batches), listBatch))

    # Return the list of batches
    return batches

# Format a dependency graph for printing
def format_dependencies(name_to_deps):
    msg = []
    for name, deps in name_to_deps.iteritems():
        nn = dictName[int(name)].get("name")
        for parent in deps:

            pn = dictName[int(parent)].get("name")

            #msg.append("%s -> %s" % (name, parent))
            msg.append("%s -> %s" % (nn, pn))

    return "\n".join(msg)

# Create and format a dependency graph for printing
def format_nodes(nodes):
    return format_dependencies(dict( (n.name, n.depends) for n in nodes ))

def toposort(data):
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

def loadXML(el, i=3, n=0):
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
        if attributes[ARCHI_TYPE] in ("archimate:UsedByRelationship"):
        #if attributes[ARCHI_TYPE] in ("archimate:AccessRelationship"):
                                # , "archimate:FlowRelationship"):
                                # , "archimate:AccessRelationship"):
                                # , "archimate:UsedByRelationship") :
                                # , "archimate:TriggeringRelationship",
                                # , "archimate:AccessRelationship",
                                # , "archimate:UsedByRelationship"):

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

            logger.debug(" source:%s" % (loadID(sourceID)))
            logger.debug(" target:%s" % (loadID(targetID)))

    i = i - 1
    for elm in el:
        loadXML(elm, i, n)

def loadFolder(tree, folder):
    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        loadXML(x, i=6)

def loadID(id):
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

def loadAll(tree):
    for x in tree.getroot():
        logNode(x)

if __name__ == '__main__':
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v12.archimate"

    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    loadAll(tree)

    loadFolder(tree, "Relations")

    dt = dict()

    n = 0

    logger.info("Found %d len(dictElement)" % len(dictElement))

    #
    # Prepare for Sort
    #
    for x in dictElement.keys():
        sourceID = x

        tt = set()
        n += 1
        targetID = dictElement[x]
        for y in targetID:

            if y != None:
                tt.add(str(y));

                logger.debug("sourceID:%s \t target:%s" % (loadID(sourceID), loadID(y)))
                logger.debug("%s \t %s" % (sourceID, y))
                logger.debug("%s" % tt)

        dt[str(x)] = tt
        logger.debug("dt[%s]=%s" % (str(x), dt[str(x)]))

    logger.info("Found %d BPs" % n)

    #
    # Topological Sort
    #
    r = toposort(dt)

    #
    # Generate Output
    #
    output = list()
    for x in r:
        logger.debug("x : %s" % x)
        for y in x.split():
            logger.debug("y : %s" % y)

            n = dictName[int(y)]
            logger.debug("%s" % (n.get("name")))

            output.insert(0, n.get("name"))

    n = 0
    for x in output:
        n += 1
        if x != "Junction":
            logger.debug("%d.%s" % (n, x))

    #
    # Determine Batches
    #
    nodes = set()
    for x in dt:
        logger.debug("dt[%s]=%s" % (str(x), dt[str(x)]))

        setTasks = list()

        for y in dt[str(x)]:
            if y != x:
                setTasks.append(str(y))
                logger.debug("setTasks : %s - type : %s" % (setTasks, type(setTasks)))

        node = Task(str(x), setTasks)
        nodes.add(node)

    logger.info("Batches:")
    w = 0
    bundles = get_task_batches(nodes)
    for bundle in reversed(bundles):
        w += 1
        logger.info("Batch %d : %s" % (w, ", ".join(node.name for node in bundle)))

        for y in bundle:
            n = dictName[int(y.name)]
            logger.info("    %s" % (n.get("name")))

