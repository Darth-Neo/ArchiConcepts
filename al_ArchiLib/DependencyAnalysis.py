#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.1'


from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

from ArchiLib import ArchiLib
from Constants import *

import pytest

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

class DependancyAnalysis(object):

    def __init__(self, fileArchimate):

        self.fileArchimate = fileArchimate

        logger.info(u"Using : %s" % self.fileArchimate)

        self.al = ArchiLib(fileArchimate)

        self.concepts = Concepts(u"BusinessProcess", u"archimate:BusinessProcess")

    # "Batches" are sets of tasks that can be run together
    def get_task_batches(self, nodes):

        # Build a map of node names to node instances
        name_to_instance = dict((n.name, n) for n in nodes )

        for x in name_to_instance.keys():
            logger.debug(u"name_to_instance[%s]=%s : %s" % (x, name_to_instance[x].name, name_to_instance[x].depends))

        # Build a map of node names to dependency names
        name_to_deps = dict( (n.name, set(n.depends)) for n in nodes )

        for x in name_to_deps.keys():
            logger.debug(u"name_to_deps[%s]=%s" % (x, name_to_deps[x]))

        # This is where we'll store the batches
        batches = []

        n = 0
        # While there are dependencies to solve...
        while name_to_deps:
            logger.info(u"length %d" % len(name_to_deps))

            # Get all nodes with no dependencies
            ready = {name for name, deps in name_to_deps.iteritems() if not deps}

            n += 1
            logger.info(u"iteration : %d" % n)
            for x in ready:
                logger.info(u"No Dep  %s" % (x))

            # If there aren't any, we have a loop in the graph
            if not ready:
                msg  = u"Circular dependencies found!\n"
                msg += self.format_dependencies(name_to_deps)
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
    def format_dependencies(self, name_to_deps):
        msg = []
        for name, deps in name_to_deps.iteritems():
            for parent in deps:
                msg.append(u"%s -> %s" % (name, parent))
        return "\n".join(msg)

    # Create and format a dependency graph for printing
    def format_nodes(self, nodes):
        return self.format_dependencies(dict( (n.name, n.depends) for n in nodes ))


    def findConcept(self, concepts, name, n=0):
        n += 1
        c = None

        if n == 3:
            return c

        for x in concepts.getConcepts().values():
            if x.name == name:
                return x
            else:
               c = self.findConcept(x, name, n)
        return c

    def getWords(self, s, concepts):
        lemmatizer = WordNetLemmatizer()

        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(s)):
            if len(word) > 1 and pos[0] == u"N":
                lemmaWord = lemmatizer.lemmatize(word.lower())
                e = concepts.addConceptKeyType(lemmaWord, u"Word")
                f = e.addConceptKeyType(pos, u"POS")

    def dependancyAnalysis(self):

        count = 0
        listTSort = list()
        for x in self.al.dictEdges.keys():
            logger.debug(u"[%s]=%s" % (self.al.dictEdges[x][u"id"], x))

            if u"source" in self.al.dictEdges[x]:
                source = self.al.dictEdges[x][u"source"]
                target = self.al.dictEdges[x][u"target"]

                logger.debug(u"  Rel    : %s" % (self.al.dictEdges[x][ARCHI_TYPE]))

                if self.al.dictEdges[x][ARCHI_TYPE] in (u"archimate:FlowRelationship"):

                    # al.countNodeType(al.dictNodes[source][ARCHI_TYPE])
                    # al.countNodeType(al.dictNodes[target][ARCHI_TYPE])
                    # al.countNodeType(al.dictEdges[x][ARCHI_TYPE])

                    if (self.al.dictNodes[source][ARCHI_TYPE] == u"archimate:BusinessProcess") and \
                            self.al.dictNodes[target][ARCHI_TYPE] == u"archimate:BusinessProcess":

                        sourceName = self.al.getNodeName(source)
                        targetName = self.al.getNodeName(target)

                        if sourceName[0].isdigit() or targetName[0].isdigit():
                            continue

                        logger.debug(u" %s:%s" % (sourceName, targetName))

                        l = list()

                        sc = self.findConcept(self.concepts, sourceName)
                        if sc is None:
                            logger.debug(u"New Target - %s" % sourceName)
                            sc = self.concepts.addConceptKeyType(self.al.getNodeName(source), u"Source")
                            self.getWords(sourceName, sc)
                        else:
                            logger.debug(u"Prior Target %s" % sourceName)

                        tc = self.findConcept(self.concepts, targetName)
                        if tc is None:
                            logger.debug(u"New Target %s" % targetName)
                            tc = sc.addConceptKeyType(self.al.getNodeName(target), u"Target")
                            self.getWords(sourceName, tc)
                        else:
                            logger.debug(u"Prior Target %s" % targetName)
                            sc.addConcept(tc)

                        l.append(target)
                        l.append(source)
                        listTSort.append(l)

        logger.debug(u"Edges = %s" % listTSort)

        Concepts.saveConcepts(self.concepts, fileConceptsTraversal)

        index = 0
        for x in listTSort:
            logger.debug(u"%d %s[%s] -%s-> %s[%s]" % (index, self.al.dictNodes[x[0]][u"name"], self.al.dictNodes[x[0]][ARCHI_TYPE], u"UsedBy",
                                                    self.al.dictNodes[x[1]][u"name"], self.al.dictNodes[x[1]][ARCHI_TYPE]))
            index += 1

            self.al.addToNodeDict(self.al.dictNodes[x[0]][u"name"], self.al.dictBP)
            self.al.addToNodeDict(self.al.dictNodes[x[1]][u"name"], self.al.dictBP)

        logger.info(u"Topic Sort Candidates : %d" % (len(listTSort)))

        nodes = list()
        index = 0
        dictTasks = dict()
        for x in listTSort:
            sname = self.al.dictNodes[x[0]][u"name"]
            tname = self.al.dictNodes[x[1]][u"name"]
            index += 1
            logger.debug(u"%d %s -%s-> %s" % (index, sname, u"UsedBy", tname))

            if sname in dictTasks:
                ln = dictTasks[sname]
                ln.append(tname)
            else:
                ln = list()
                ln.append(tname)
                dictTasks[sname] = ln

        for x in dictTasks.keys():
            logger.debug(u"dictTasks[%s]=%s" % (x, dictTasks[x]))
            a = Task(x, dictTasks[x])
            nodes.append(a)

        for x in self.al.dictBP.keys():
            # for x in listBP:
            if x not in dictTasks:
                logger.debug(u"Add %s" % (x))
                a = Task(x, list())
                nodes.append(a)

        self.format_nodes(nodes)

        conceptBatches = Concepts(u"Batch", u"archimate:WorkPackage")

        n = 0
        logger.info(u"Batches:")
        batches = self.get_task_batches(nodes)
        for bundle in batches:
            n += 1
            name = u"Batch %d" % n
            c = conceptBatches.addConceptKeyType(name, u"archimate:WorkPackage")
            for node in bundle:
                c.addConceptKeyType(node.name, u"archimate:BusinessProcess")

            logger.info(u"%d : %s" % (n, ", ".join(node.name.lstrip() for node in bundle)))

        Concepts.saveConcepts(conceptBatches, fileConceptsBatches)

        return conceptBatches

def test_DependencyAnalysis():

    start_time = ArchiLib.startTimer()

    da = DependancyAnalysis(fileArchimateTest)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    test_DependencyAnalysis()