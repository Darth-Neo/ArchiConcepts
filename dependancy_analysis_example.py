#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

class GraphError(Exception):
    pass

def topological_sort(edges):
    """topologically sort vertices in edges.

    edges: list of pairs of vertices. Edges must form a DAG.
           If the graph has a cycle, then GraphError is raised.

    returns: topologically sorted list of vertices.

    see http://en.wikipedia.org/wiki/Topological_sorting
    """
    # resulting list
    L=[]

    # maintain forward and backward edge maps in parallel.
    st,ts={},{}

    def prune(s,t):
        del st[s][t]
        del ts[t][s]

    def add(s,t):
        try:
            st.setdefault(s,{})[t]=1
        except Exception, e:
            raise RuntimeError(e, (s,t))
        ts.setdefault(t,{})[s]=1

    for s,t in edges:
        add(s,t)

    # frontier
    S=set(st.keys()).difference(ts.keys())

    while S:
        s=S.pop()
        L.append(s)
        for t in st.get(s,{}).keys():
            prune(s,t)
            if not ts[t]:       # new frontier
                S.add(t)

    if filter(None, st.values()): # we have a cycle. report the cycle.
        def traverse(vs, seen):
            for s in vs:
                if s in seen:
                    raise GraphError('contains cycle: ', seen)

                seen.append(s) # xx use ordered set..

                traverse(st[s].keys(), seen)

        traverse(st.keys(), list())
        assert False, 'should not reach..'

    return L

def getNode(el, dictAttrib):
    logger.debug("%s" % (el.tag))

    attributes = el.attrib

    nl = dict()
    for atr in attributes:
        nl[atr] = attributes[atr]
        logger.debug("%s = %s" % (atr, attributes[atr]))

    if nl.has_key("id"):
        dictAttrib[nl["id"]] = nl

    for elm in el:
        getNode(elm, dictAttrib)

def getEdges(tree, folder, dictAttrib):
    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        getNode(x, dictAttrib)

def getFolders(tree):
    r = tree.xpath('folder')

    l = list()

    for x in r:
        l.append(x.get("name"))
        logger.debug("%s" % (x.get("name")))

    return l

if __name__ == "__main__":
    fileArchiModel = 'archi.archimate'
    #fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Presentations/Solution Engineering.xml"
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/DNX Phase 2/DNX Phase 2 0.8.archimate"


    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    dictNodes = dict()
    dictEdges = dict()

    listFolders = getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        logger.debug("%s" % (x))
        if x != "Views" and x != "Relations":
            logger.debug("Checking : %s" % (x))
            getEdges(tree, x, dictNodes)

    # Get all Edges
    getEdges(tree, "Relations", dictEdges)

    listTSort = list()

    count = 0
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            logger.debug("  Rel    : %s" % (dictEdges[x][ARCHI_TYPE]))
            logger.debug("  Source : %s" % (dictNodes[source]["name"]))
            logger.debug("  Target : %s" % (dictNodes[target]["name"]))

            if dictEdges[x][ARCHI_TYPE] in ("archimate:FlowRelationship"): #,
                #"archimate:AssociationRelationship", "archimate:UsedByRelationship"):
                l = list()

                if dictNodes[source]["id"] == "Junction":
                    break

                if dictNodes[target]["id"] == "Junction":
                    break

                l.append(target)
                l.append(source)
                listTSort.append(l)
                count = count + 1

    logger.info("TSort : %d" % (count))
    logger.debug("Edges = %s" % listTSort)

    index = 0
    for x in listTSort:
        logger.info("%d %s[%s] --> %s[%s]" % (index, dictNodes[x[0]]["name"], dictNodes[x[0]]["id"], dictNodes[x[1]]["name"], dictNodes[x[1]]["id"]))
        index = index + 1

    logger.info("topological_sort")
    sort = topological_sort(listTSort)

    logger.info("Sort")
    for x in sort:
        if dictNodes[x][ARCHI_TYPE] == "archimate:BusinessProcess":
            logger.info("%s:%s" % (x, dictNodes[x]["name"]))