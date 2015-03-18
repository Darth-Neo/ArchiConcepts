#! python

import solr

# create a connection to a solr server
s = solr.SolrConnection('http://localhost:8983/solr/gettingstarted')

sQuery = raw_input('Query : ')

#sQuery = "bonds"
#sQuery = "payment"

response = s.query(sQuery)

for hit in response.results:
    #print("hit: %s" % hit)

    for k, v in hit.items():
        #print("    %s%s" % (k, v))

        if k == u"Name":
            s = 'n file://%s' % str(hit[k]).encode('utf-8',errors='ignore')
            #s = 'file://%s' % s
            print("a %s" % s)

        elif k == u"Type":
            s = 'n file://%s' % str(hit[k]).encode('utf-8',errors='ignore')
            #s = 'file://%s' % s
            print("a %s" % s)

        elif k == u"author":
            s = 'file://%s' % str(hit[k]).encode('utf-8',errors='ignore')
            #s = 'file://%s' % s
            print("a %s" % s)

        elif k == u"id":
            s = 'file://%s' % str(hit[k]).encode('utf-8',errors='ignore')
            #s = 'file://%s' % s
            print("i %s" % s)

        elif k == u"resourcename":
            s = 'file://%s' % str(hit[k]).encode('utf-8',errors='ignore')
            #s = 'file://%s' % s
            print("r %s" % s)