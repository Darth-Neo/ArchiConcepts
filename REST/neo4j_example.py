from neo4jrestclient.client import GraphDatabase

__author__ = 'morrj140'
url = "http://localhost:7474/db/data/"

gdb = GraphDatabase(url)
#gdb = GraphDatabase(url, username="username", password="password")

#gdb = GraphDatabase(url, username="username", password="password",
#                        cert_file='path/to/file.cert',
#                        key_file='path/to/file.key')

if False:
    alice = gdb.nodes.create(name="Alice", age=30)

    bob = gdb.nodes.create(name="Bob", age=30)

    alice.relationships.create("Knows", bob, since=1980)
else:
    query = "MATCH (n)--() RETURN n LIMIT 5"
    results = gdb.query(query, data_contents=True)
    print results.stats
