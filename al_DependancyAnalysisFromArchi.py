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

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

import al_ArchiLib as al
import al_GraphConcepts as GC

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

    for x in name_to_instance.keys():
        logger.debug("name_to_instance[%s]=%s : %s" % (x, name_to_instance[x].name, name_to_instance[x].depends))

    # Build a map of node names to dependency names
    name_to_deps = dict( (n.name, set(n.depends)) for n in nodes )

    for x in name_to_deps.keys():
        logger.debug("name_to_deps[%s]=%s" % (x, name_to_deps[x]))

    # This is where we'll store the batches
    batches = []

    n = 0
    # While there are dependencies to solve...
    while name_to_deps:
        logger.debug("length %d" % len(name_to_deps))

        # Get all nodes with no dependencies
        ready = {name for name, deps in name_to_deps.iteritems() if not deps}

        n += 1
        logger.info("iteration : %d" % n)
        for x in ready:
            logger.info("  %s" % (x))

        # If there aren't any, we have a loop in the graph
        if not ready:
            msg  = "Circular dependencies found!\n"
            msg += format_dependencies(name_to_deps)
            raise ValueError(msg)

        # Remove them from the dependency graph
        for name in ready:
            del name_to_deps[name]
        for deps in name_to_deps.itervalues():
            deps.difference_update(ready)

        # Add the batch to the list
        batches.append( {name_to_instance[name] for name in ready} )

    # Return the list of batches
    return batches

# Format a dependency graph for printing
def format_dependencies(name_to_deps):
    msg = []
    for name, deps in name_to_deps.iteritems():
        for parent in deps:
            msg.append("%s -> %s" % (name, parent))
    return "\n".join(msg)

# Create and format a dependency graph for printing
def format_nodes(nodes):
    return format_dependencies(dict( (n.name, n.depends) for n in nodes ))


def findConcept(concept, name, n=0):
    n += 1
    c = None

    if n == 3:
        return c

    for x in concepts.getConcepts().values():
        if x.name == name:
            return x
        else:
           c = findConcept(x, name, n)
    return c

def getWords(s, concepts):
    lemmatizer = WordNetLemmatizer()

    for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(s)):
        if len(word) > 1 and pos[0] == "N":
            lemmaWord = lemmatizer.lemmatize(word.lower())
            e = concepts.addConceptKeyType(lemmaWord, "Word")
            f = e.addConceptKeyType(pos, "POS")

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v31.archimate"
    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    concepts = Concepts("Node", "Nodes")

    dictNodes = dict()
    dictEdges = dict()
    dictBP = dict()

    listFolders = al.getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("Checking Folder : %s" % (x))
            al.getEdges(tree, x, dictNodes)

    # Get all Edges
    al.getEdges(tree, "Relations", dictEdges)

    logger.info("Found %d Nodes" % len(dictNodes))
    logger.info("Found %d Edges" % len(dictEdges))

    count = 0
    listTSort = list()
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            logger.debug("  Rel    : %s" % (dictEdges[x][al.ARCHI_TYPE]))

            if dictEdges[x][al.ARCHI_TYPE] in ("archimate:UsedByRelationship"):

                al.countNodeType(dictNodes[source][al.ARCHI_TYPE])
                al.countNodeType(dictNodes[target][al.ARCHI_TYPE])
                al.countNodeType(dictEdges[x][al.ARCHI_TYPE])

                if (dictNodes[source][al.ARCHI_TYPE] == "archimate:BusinessProcess") and \
                        dictNodes[target][al.ARCHI_TYPE] == "archimate:BusinessProcess":

                    sourceName = al.getNodeName(source)
                    targetName = al.getNodeName(target)

                    logger.debug(" %s:%s" % (sourceName, targetName))

                    l = list()

                    sc = findConcept(concepts, sourceName)
                    if sc == None:
                        logger.debug("New Target - %s" % sourceName)
                        sc = concepts.addConceptKeyType(al.getNodeName(source), "Source")
                        getWords(sourceName, sc)
                    else:
                        logger.debug("Prior Target %s" % sourceName)

                    tc = findConcept(concepts, targetName)
                    if tc == None:
                        logger.debug("New Target %s" % targetName)
                        tc = sc.addConceptKeyType(al.getNodeName(target), "Target")
                        getWords(sourceName, tc)
                    else:
                        logger.debug("Prior Target %s" % targetName)
                        sc.addConcept(tc)

                    l.append(target)
                    l.append(source)
                    listTSort.append(l)
                    count = count + 1

    logger.debug("Edges = %s" % listTSort)

    Concepts.saveConcepts(concepts, "traversal.p")

    if False:
        GC.graphConcepts(concepts, filename="UsedByAnalysis.png")

    al.logTypeCounts()

    index = 0
    for x in listTSort:
        logger.info("%d %s[%s] -%s-> %s[%s]" % (index, dictNodes[x[0]]["name"], dictNodes[x[0]][al.ARCHI_TYPE], "UsedBy", dictNodes[x[1]]["name"], dictNodes[x[1]][al.ARCHI_TYPE]))
        index = index + 1

        al.addToNodeDict(dictNodes[x[0]]["name"], dictBP)
        al.addToNodeDict(dictNodes[x[1]]["name"], dictBP)

    logger.info("Topic Sort Candidates : %d" % (len(listTSort)))

    nodes = list()
    index = 0
    dictTasks = dict()
    for x in listTSort:
        sname = dictNodes[x[0]]["name"]
        tname = dictNodes[x[1]]["name"]
        index += 1
        logger.debug("%d %s -%s-> %s" % (index, sname, "UsedBy", tname))

        if dictTasks.has_key(sname):
            ln = dictTasks[sname]
            ln.append(tname)
        else:
            ln = list()
            ln.append(tname)
            dictTasks[sname] = ln

    for x in dictTasks.keys():
        logger.debug("dictTasks[%s]=%s" % (x, dictTasks[x]))
        a = Task(x, dictTasks[x])
        nodes.append(a)

    for x in dictBP.keys():
        #for x in listBP:
        if not dictTasks.has_key(x):
            logger.info("Add %s" % (x))
            a = Task(x, list())
            nodes.append(a)

    format_nodes(nodes)

    conceptBatches = Concepts("Batch", "Batches")

    n = 0
    logger.info("Batches:")
    batches = get_task_batches(nodes)
    for bundle in batches:
        n += 1
        name = "Batch %d" % n
        c = conceptBatches.addConceptKeyType(name, "Batch")
        for node in bundle:
            c.addConceptKeyType(node.name, "Node")

        logger.info("%d : %s" % (n, ", ".join(node.name.lstrip() for node in bundle)))

    Concepts.saveConcepts(conceptBatches, "batches.p")