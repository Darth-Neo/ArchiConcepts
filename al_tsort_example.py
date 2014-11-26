
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

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
            #raise RuntimeError(e, (s,t))
            pass
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
                    #raise GraphError('contains cycle: ', seen)
                    pass
                seen.append(s) # xx use ordered set..
                traverse(st[s].keys(), seen)
        traverse(st.keys(), list())

    return L

class Test(unittest.TestCase):

    def test_tsort(self):

        #g= [("7","11"), ("7","8"), ("5","11"), ("3","8"), ("3","10"), ("8","10"), ("11","2"), ("11","9"), ("11,10"), ("8","9")]

        g= [(7,11), (7,8), (5,11), (3,8), (3,10), (8,10), (11,2), (11,9), (11,10), (8,9)]

        #edges=[ tuple(map(int,e.split(','))) for e in g.strip().split('\n') ]

        print("Edges: %s:%s", (type(g), g))

	print("Sort: ", topological_sort(g))

        assert topological_sort(g)==[3, 5, 7, 8, 11, 2, 9, 10]

        #self.assertRaises(GraphError, topological_sort, (edges+[(9,3)]))

if __name__ == '__main__':

    unittest.main()
