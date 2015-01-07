#!/usr/bin/env python

import json

from py2neo.neo4j import GraphDatabaseService, CypherQuery

graph = GraphDatabaseService()

def get_graph():
    query = CypherQuery(graph, "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
                               "RETURN m.title as movie, collect(a.name) as cast "
                               "LIMIT {limit}")
    results = query.execute(limit=5)
    nodes = []
    rels = []
    i = 0
    for movie, cast in results.data:
        nodes.append({"title": movie, "label": "movie"})
        target = i
        i += 1
        for name in cast:
            actor = {"title": name, "label": "actor"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "target": target})
    return {"nodes": nodes, "links": rels}


def get_search(q):

    query = CypherQuery(graph, "MATCH (movie:Movie) "
                               "WHERE movie.title =~ {title} "
                               "RETURN movie")
    results = query.execute(title="(?i).*" + q + ".*")

    return json.dumps([{"movie": row["movie"].get_cached_properties()} for row in results.data])

if __name__ == "__main__":
    pass
