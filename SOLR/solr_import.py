import solr

# create a connection to a solr server
s = solr.SolrConnection('http://localhost:8983/solr/gettingstarted')

if s <> None:
    # add a document to the index
    doc = dict(id=1, title='Lucene in action', author=['james', 'kevin'],)

    s.add(doc, commit=True)

    # do a search
    response = s.query('title:lucene')
    for hit in response.results:
        print hit['title']
else:
    print "Not a valid connection"

