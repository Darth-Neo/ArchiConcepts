#! python
import sys, getopt
import solr
import time
import datetime
import json

# http://localhost:8983/solr/gettingstarted/select?q=bond%0A&wt=json&indent=true


def createPostQuery(s, search=u"bond"):

    protocol = u"http://"
    server = u"localhost:8983"
    collection = u"dkb"

    query = u"solr/%s/select?q=%s" % (collection, search)
    url = u'{0:s}{1:s}/{2:s}\%0A&wt=json&indent=true'.format(protocol, server, query)

    return url

def jsonSave(data):

    with open(u'data.json', u'wb') as fp:
        json.dump(data, fp)

def jsonLoad(data):

    with open(u'data.json', u'rb') as fp:
        data = json.load(fp)

    return data

if __name__ == u"__main__":

    if len(sys.argv) != 2:
        print(u"Usage: %s search_term" % (sys.argv[0]))
        sQuery = raw_input(u'Query : ')

    else:
        print(u"Using: %s" % str(sys.argv[1]))
        sQuery = unicode(sys.argv[1])

    n = 0

    collection = u"dkb"

    # create a connection to a solr server
    s = solr.SolrConnection(u'http://localhost:8983/solr/%s' % collection)

    response = s.query(sQuery)

    for hit in response.results:
        # print("hit: %s" % hit)

        n += 1
        print u""

        for k, v in hit.items():
            print(u"    %s=%s" % (k, v))

            if k in (u"creator", u"dc_creator", u"Name", u"Type", u"author", u"meta_author"):
                s = u'n %s' % str(hit[k]).encode(u'utf-8', errors=u'replace')
                print(u"%d:a %s" % (n, s))

            elif k == u"creation_date":

                format = u'%m-%d-%Y %I:%M%p %Z'

                s = v[0].strftime(format)

                # s= v[0].isoformat(" ")[:-9]

                # print("%d:a %s" % (n ,s))

            elif k == u"id":
                # s = 'file://%s' % str(hit[k]).encode(encoding='utf-8',errors='ignore')
                s = u'file://%s' % hit[k]
                print(u"%d:a %s" % (n, s))

            elif k == u"resourcename":
                s = u'file://%s' % hit[k]
                print(u"%d:a %s" % (n, s))

