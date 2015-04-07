#! python
import sys, getopt
import solr
import time
import datetime
import json

# http://localhost:8983/solr/gettingstarted/select?q=bond%0A&wt=json&indent=true

def postQuery(s, search="bond"):

    protocol = "http://"
    server = "localhost:8983"

    query = "solr/gettingstarted/select?q=%s" % search
    url = "%s%s/%s%0A&wt=json&indent=true" % (protocol, server, query)

    return url

def jsonSave(data):

    with open('data.json', 'wb') as fp:
        json.dump(data, fp)

def jsonLoad(data):

    with open('data.json', 'rb') as fp:
        data = json.load(fp)

    return data

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: %s search_term" % (sys.arv[0]))
        sQuery = raw_input('Query : ')
    else:
        print("Using: %s" % str(sys.argv[1]))
        sQuery = unicode(sys.argv[1])

    n = 0

    # create a connection to a solr server
    s = solr.SolrConnection('http://localhost:8983/solr/gettingstarted')

    response = s.query(sQuery)

    for hit in response.results:
        #print("hit: %s" % hit)

        n += 1
        print ""

        for k, v in hit.items():
            #print("    %s%s" % (k, v))

            if k in (u"creator", u"dc_creator", u"Name", u"Type", u"author", u"meta_author"):
                s = 'n %s' % str(hit[k]).encode('utf-8',errors='ignore')
                print("%d:a %s" % (n ,s))

            elif k == u"creation_date":

                format = '%m-%d-%Y %I:%M%p %Z'

                s = v[0].strftime(format)

                #s= v[0].isoformat(" ")[:-9]

                #print("%d:a %s" % (n ,s))

            elif k == u"id":
                # s = 'file://%s' % str(hit[k]).encode(encoding='utf-8',errors='ignore')
                s = 'file://%s' % hit[k]
                print("%d:a %s" % (n ,s))

            elif k == u"resourcename":
                s = 'file://%s' % hit[k]
                print("%d:a %s" % (n ,s))

