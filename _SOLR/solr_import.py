import solr
import datetime
from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def import_doc(c, sd):
    return c.add(sd, commit=True)


def search_doc(c, sd):
    return c.query(sd)

if __name__ == u"__main__":

    s = solr.SolrConnection(u'http://localhost:8983/solr/dkb')

    assert s is not None

    dtn = datetime.datetime.now()
    doc1 = dict(id=1, title=u'Lucene in action', author=[u'james', u'kevin'], datetime=dtn,
              d=u"book1", title_t=u"The Way of Kings", author_s=u"Brandon Sanderson")

    doc2 = dict()
    doc2[u'id'] = u"1"
    doc2[u'title'] = u"Lucene in action"
    doc2[u'author'] = [u"james", u"kevin"]
    doc2[u'id'] = u"book1"
    doc2[u'title_t'] = u"The Way of Kings"
    doc2[u'author_s'] = u"Brandon Sanderson"

    r = import_doc(s, doc2)

    logger.info(u"r : %s" % r)

    logger.info(u"____________________________________________________________________________")

    # do a search
    qd = u'title:*'
    # qd = u"'id'='book1'"
    # qd = u"'people'='james'"

    response = search_doc(s, qd)

    for hit in response.results:
        logger.info(u"---")
        for y in hit:
            logger.info(u"    %s = %s" % (y, hit[y]))