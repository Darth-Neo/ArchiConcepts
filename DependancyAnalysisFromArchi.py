#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
import time
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

import nl_phase_f_graph_concepts as GC
dictCount = dict()

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
        logger.debug("prune source : %s" % dictNodes[s]["name"])
        logger.debug("prune target : %s" % dictNodes[t]["name"])
        del st[s][t]
        del ts[t][s]

    def add(s,t):
        logger.debug("add source : %s" % dictNodes[s]["name"])
        logger.debug("  add target : %s" % dictNodes[t]["name"])

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
        logger.debug("source : %s" % dictNodes[s]["name"])
        L.append(s)
        for t in st.get(s,{}).keys():
            prune(s,t)
            if not ts[t]:       # new frontier
                logger.debug("  t : %s" % dictNodes[t]["name"])
                S.add(t)

    if filter(None, st.values()): # we have a cycle. report the cycle.
        def traverse(vs, seen):
            for s in vs:
                if s in seen:
                    logger.warn("%s:%s" % (dictNodes[s]["name"], GraphError('contains cycle: ', [dictNodes[x]["name"] for x in seen])))
                    break

                seen.append(s) # xx use ordered set..
                try:
                    traverse(st[s].keys(), seen)
                except:
                    return


        traverse(st.keys(), list())
        logger.debug("Should not reach")

    return L

def getEdgesForNode(nodeName, searchType, dictNodes, dictEdges, n=0):
    listNodes = list()

    if n == 4:
        return listNodes
    else:
        n += 1

    for x in dictNodes.keys():
        try:
            if dictNodes[x]["name"] == nodeName:
                source = x
                break
        except:
            source = None

    for x in dictEdges.keys():
        if dictEdges[x].has_key("source"):
            if dictEdges[x]["source"] == source:
                sourceNE = dictEdges[x]["source"]
                targetNE = dictEdges[x]["target"]

                if dictNodes[targetNE][ARCHI_TYPE] in searchType:
                    spaces = " " * n
                    nodeName = getNodeName(targetNE)
                    if nodeName != "NA":
                        nn = "%s%s" % (spaces, nodeName)
                        listNodes.append(nn)

                        ln = getEdgesForNode(nodeName, searchType, dictNodes, dictEdges, n)
                        for y in ln:
                            listNodes.append(y)

    return listNodes

def countNodeType(type):
    if dictCount.has_key(type):
        dictCount[type] += 1
    else:
        dictCount[type] = 1

def getNodeName(node):
    name = " "

    try:
        logger.debug("  Node : %s" % (dictNodes[node]["name"]))
        name = dictNodes[node]["name"]
    except:
        logger.debug("Node not Found")

    return name

def getNode(el, dictAttrib):
    logger.debug("%s" % (el.tag))

    attributes = el.attrib

    # Not every node will have a type
    try:
        countNodeType(attributes["type"])
    except:
        pass

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

def logTypeCounts():
    logger.info("Type Counts")
    listCounts = dictCount.items()
    for x in sorted(listCounts, key=lambda c: abs(c[1]), reverse=False):
        if x[1] > 1:
            logger.info("  %d - %s" % (x[1], x[0]))

    logger.info(" ")

if __name__ == "__main__":
    #fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v28.archimate"
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v29.archimate"
    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    dictNodes = dict()
    dictEdges = dict()

    listFolders = getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("Checking Folder : %s" % (x))
            getEdges(tree, x, dictNodes)

    # Get all Edges
    getEdges(tree, "Relations", dictEdges)

    concepts = Concepts("Node", "Nodes")

    logger.info("Found %d Nodes" % len(dictNodes))
    logger.info("Found %d Edges" % len(dictEdges))

    count = 0
    listTSort = list()
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            logger.debug("  Rel    : %s" % (dictEdges[x][ARCHI_TYPE]))

            if dictEdges[x][ARCHI_TYPE] in ("archimate:UsedByRelationship"):

                countNodeType(dictNodes[source][ARCHI_TYPE])
                countNodeType(dictNodes[target][ARCHI_TYPE])
                countNodeType(dictEdges[x][ARCHI_TYPE])

                if (dictNodes[source][ARCHI_TYPE] == "archimate:BusinessProcess") and \
                        dictNodes[target][ARCHI_TYPE] == "archimate:BusinessProcess":

                    logger.debug(" %s:%s" % (getNodeName(source), getNodeName(target)))

                    l = list()

                    c = concepts.addConceptKeyType(getNodeName(source), "Source")
                    c.addConceptKeyType(getNodeName(target), "Target")

                    l.append(target)
                    l.append(source)
                    listTSort.append(l)
                    count = count + 1

    logger.info("Topic Sort Candidates : %d" % (count))
    logger.debug("Edges = %s" % listTSort)


    GC.graphConcepts(concepts, filename="UsedByAnalysis.png")

    logTypeCounts()

    if False:
        index = 0
        for x in listTSort:
            logger.debug("%d %s[%s] -%s-> %s[%s]" % (index, dictNodes[x[0]]["name"], dictNodes[x[0]][ARCHI_TYPE], "UsedBy", dictNodes[x[1]]["name"], dictNodes[x[1]][ARCHI_TYPE]))
            index = index + 1

    if False:
        sort = topological_sort(listTSort)
        listBP = [dictNodes[x]["name"] for x in sort if dictNodes[x][ARCHI_TYPE] == "archimate:BusinessProcess"]
        listBP.reverse()

        n = 0
        logger.info("Sort")
        for x in listBP:
            logger.info("  %d : %s" % (n, x))
            n += 1

            if False:
                searchType = ("archimate:ApplicationService", "archimate:ApplicationComponent", "archimate:ApplicationInterface", "archimate:Requirement")
                listNodes = getEdgesForNode(x, searchType, dictNodes, dictEdges)
                for x in listNodes:
                    logger.info("    %s" % x)


    if False:
        logger.info("Skipped")
        s1 = set([x for x in listBP])
        s2 = set([dictNodes[x[0]]["name"] for x in listTSort])
        missing = s1 - s2
        searchType = ("archimate:Requirement")
        for x in missing:
            logger.info("  %s" % x)
            listNodes = getEdgesForNode(x, searchType, dictNodes, dictEdges)
            for y in listNodes:
                logger.info("    %s" % y)
