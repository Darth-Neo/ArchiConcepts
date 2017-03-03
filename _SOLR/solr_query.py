#!/usr/bin/env python
from __future__ import print_function
import solr
import json

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

# http://localhost:8983/solr/gettingstarted/select?q=bond%0A&wt=json&indent=true

logInfo = print
# logInfo = logger.info
logDebug = print
# logDebug = logger.debug

def createPostQuery(search, collection):

    protocol = u"http://"
    server = u"localhost:8983"

    query = u"solr/%s/select?q=%s" % (collection, search)
    url = u'{0:s}{1:s}/{2:s}\%0A&wt=json&indent=true'.format(protocol, server, query)

    return url

def reviewResults(collection, Hit=False, Skip=True):
    # create a connection to a solr server
    s = solr.SolrConnection(u'http://localhost:8983/solr/%s' % collection)

    response = s.query(sQuery)

    n = 0

    logInfo(u"hit: %d" % len(response.results))

    for hit in response.results:

        n += 1
        logInfo(u"\n")

        for k, v in hit.items():
            logDebug(u"%d \t %s=%s" % (n, k, v))

            if k in (u"creator", u"dc_creator", u"Name", u"Type", u"author", u"meta_author") and Skip is False:
                s = u'n %s' % str(hit[k]).encode(u'utf-8', errors=u'replace')
                logDebug(u"%d:%s: %s" % (n, k, s))

            elif k == u"creation_date" and Skip is False:
                format = u'%m-%d-%Y %I:%M%p %Z'
                s = v[0].strftime(format)
                # s= v[0].isoformat(" ")[:-9]
                # logDebug("%d:a %s" % (n ,s))

            elif k == u"id":
                # s = 'file://%s' % str(hit[k]).encode(encoding='utf-8',errors='ignore')
                s = u'file://%s' % hit[k]
                logInfo(u"%d:id: %s" % (n, s))

            elif k == u"resourcename":  # and Skip is False:
                s = u'file://%s' % hit[k]
                logInfo(u"%d:resourcename: %s" % (n, s))

        logInfo(u"\n")


if __name__ == u"__main__":

    if len(sys.argv) != 2:
        logInfo(u"Usage: %s search_term" % (sys.argv[0]))
        sQuery = raw_input(u'Query : ')

    else:
        logInfo(u"Using: %s" % str(sys.argv[1]))
        sQuery = unicode(sys.argv[1])

    Skip = True
    Hit = False
    collection = u"Kronos"

    reviewResults(collection, Hit=False, Skip=True)

