#!/usr/bin/env python

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

    # Build a map of node names to dependency names
    name_to_deps = dict( (n.name, set(n.depends)) for n in nodes )

    # This is where we'll store the batches
    batches = []

    # While there are dependencies to solve...
    while name_to_deps:

        # Get all nodes with no dependencies
        ready = {name for name, deps in name_to_deps.iteritems() if not deps}

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

    # An example, working dependency graph
    a = Task("a")
    b = Task("b")
    c = Task("c", "a")
    d = Task("d", "b")
    e = Task("e", "c", "d")
    f = Task("f", "a", "b")
    g = Task("g", "e", "f")
    h = Task("h", "g")
    i = Task("i", "a")
    j = Task("j", "b")
    k = Task("k")
    nodes = (a, b, c, d, e, f, g, h, i, j)

    # Show it on screen
    print "A working dependency graph example:"
    print format_nodes(nodes)
    print

    # Show the batches on screen
    print "Batches:"
    for bundle in get_task_batches(nodes):
        print ", ".join(node.name for node in bundle)
    print

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