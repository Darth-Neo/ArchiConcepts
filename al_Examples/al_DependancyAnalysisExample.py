#!/usr/bin/env python

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

logger = Logger.setupLogging(__name__)

# Dependency resolution example in Python
# By Mario Vilas (mvilas at gmail dot com)

# The graph nodes
class Task(object):
    def __init__(self, name, *depends):
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
            logger.info("ready=%s" % (x))

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

# The test code
if __name__ == "__main__":

    nodes = list()

    # An example, working dependency graph
    a = Task("a")
    nodes.append(a)
    b = Task("b")
    nodes.append(b)
    c = Task("c", "a")
    nodes.append(c)
    d = Task("d", "b")
    nodes.append(d)
    e = Task("e", "c", "d")
    nodes.append(e)
    f = Task("f", "a", "b")
    nodes.append(f)
    g = Task("g", "e", "f")
    nodes.append(g)
    h = Task("h", "g")
    nodes.append(h)
    i = Task("i", "a")
    nodes.append(i)
    j = Task("j", "b")
    nodes.append(j)
    k = Task("k")
    nodes.append(k)

    # nodes is the superset of Task
    # nodes = (b, c, d, e, f, g, h, i, j, a)

    # Show it on screen
    logger.info( "A working dependency graph example:")
    logger.info( format_nodes(nodes))

    # Show the batches on screen
    logger.info("Batches:")
    batches = get_task_batches(nodes)
    for bundle in batches:
        logger.info( ", ".join(node.name for node in bundle))


    # An example, *broken* dependency graph
    #a = Task("a", "i")
    #nodes = (a, b, c, d, e, f, g, h, i, j)

    # Show it on screen
    #print "A broken dependency graph example:"
    #print format_nodes(nodes)
    #print

    # This should raise an exception and show the current state of the graph
    #print "Trying to resolve the dependencies will raise an exception:"
    #print
    #get_task_batches(nodes)