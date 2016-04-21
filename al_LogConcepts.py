#!/usr/bin/python
#
# Concept Logging
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib


def distribution(concepts, tc=None):
    distribution = dict()
    strCommon = ""

    if tc is not None:
        topicList = [[x.name, x.count] for x in tc.getConcepts().values()]
        topicSortedList = sorted(topicList, key=lambda c: c[1], reverse=False)
        topics = [a[0] for a in topicSortedList]

    # Document
    for x in concepts.getConcepts().values():
        logger.debug(u"%s[%d]" % (x.name, x.count))

        # Topic
        for y in x.getConcepts().values():
            logger.debug(u"%s" % y.name)

            lls = [z.name.lower() for z in y.getConcepts().values()]

            lss = sorted(lls, key=lambda c: c, reverse=False)

            strCommon = u" ".join([x for x in lss]).replace(u".", u"")

        if strCommon in distribution:
            distribution[strCommon] += 1
        else:
            distribution[strCommon] = 1

    listCommon = sorted([x for x in distribution.items()], key=lambda c: c[1], reverse=False)

    lcd = [[y, x.count(u" ") + 1, x] for x, y in listCommon if y > 2]

    for x, y, z in lcd:
        logger.info(u"%d[%d] : %s" % (x, y, z))
        
        words = [a for a in z.split(u" ")]
        if len(words) > 0:
            for w in words:
                if ((tc is not None) and (w in topics)):
                    topicCount = [q[1] for q in topicList if q[0] == w]
                    logger.info(u"  Topic : %s[%d]" % (w, topicCount[0]))

if __name__ == u"__main__":
    # conceptFile = u"documents.p"
    # conceptFile = u"topicsDict.p"
    conceptFile = u"GapsSimilarity.p"
    # conceptFile = u"chunks.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    # conceptFile = u"ngramsubject.p"
    # conceptFile = u"traversal.p"
    # conceptFile = u"batches.p"
    # conceptFile = u"export.p"
    # conceptFile = u"reqs.p"
    # conceptFile = u"Estimation.p"
    #conceptFile = u"archi.p"

    if True:
        filePath = conceptFile
    else:
        # fileConceptsExport = u"export.csv"
        directory = os.getcwd() + os.sep + u"run" + os.sep
        filePath = directory + conceptFile

    logger.info(u"Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()
    # concepts.printConcepts(list)
    # Concepts.outputConceptsToCSV(concepts, fileConceptsExport)

    if False:
        logger.info(u"Distribution Analysis")
        tc = Concepts.loadConcepts(filePath)
        distribution(concepts, tc)
        distribution(concepts)






