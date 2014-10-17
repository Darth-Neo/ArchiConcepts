__author__ = 'morrj140'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

from lxml import etree

import nltk

import import_artifacts as ia

num_topics = 100
num_words  = 100
similarity = 0.80

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

class DocumentsSimilarity(object):
    concepts = None
    conceptsSimilarity = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None
    topics = None
    topicConcepts = None

    def __init__(self):
        pass

    def createTopics(self, conceptsFile):

        logger.info("Load Concepts from " + conceptsFile)
        self.concepts = Concepts.loadConcepts(conceptsFile)
        logger.info("Loaded Concepts")

        self.tm = TopicsModel()

        logger.info("Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadConceptsWords(self.concepts)

        logger.info("Read " + str(len(self.documentsList)) + " Documents, with " + str(self.wordcount) + " words.")

        logger.info("Compute Topics")
        self.topics = self.tm.computeTopics(self.documentsList, nt=num_topics, nw=num_words)

        logger.info("Log Topics")
        self.tm.logTopics(self.topics)

        self.listTopics = [x[0].encode('ascii', errors="ignore").strip() for x in self.topics]

        logger.info("Saving Topics")
        self.topicConcepts = self.tm.saveTopics(self.topics)

    def findSimilarties(self, conceptsSimilarityFile):

        logger.info("Compute Similarity")

        self.conceptsSimilarity = Concepts("ConceptsSimilarity", "Similarities")

        # Compute similarity between documents / concepts
        similarityThreshold = similarity

        for document in self.documentsList:
            indexNum = self.documentsList.index(document)

            df = self.concepts.getConcepts().keys()

            logger.debug("Document %s" % (df[indexNum]))

            logger.debug("  documentsList[" + str(indexNum) + "]=" + str(document))

            # Show common topics
            d = [x.encode('ascii', errors="ignore").strip().replace("'", "") for x in document]
            e = [y.encode('ascii', errors="ignore").strip().replace("\"", "") for y in self.listTopics]

            s1 = set(e)
            s2 = set(d)
            common =  s1 & s2
            lc = [x for x in common]
            logger.debug("  Common Topics : %s" % (lc))

            self.doComputation(document, similarityThreshold)

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info("Complete createTopics")

        return self.conceptsSimilarity

    def doComputation(self, j, similarityThreshold):

        pl = self.tm.computeSimilar(self.documentsList.index(j), self.documentsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug("   similarity above threshold")
            logger.debug("   pl:" + str(pl))

            for l in pl:
                if l[1] != l[2]:
                    logger.debug("  l:" + str(l))
                    ps = self.conceptsSimilarity.addConceptKeyType(l[1], "Similar")
                    ps.count = TopicsModel.convertMetric(l[0])
                    #rt1 = ps.addConceptKeyType(str(l[3]), "SimilarTopics")
                    #rt1 = len(l[3])
                    pt = ps.addConceptKeyType(l[2], "Concept")
                    #rt2 = pt.addConceptKeyType(str(l[4]), "ProjectTopics")
                    #rt2.count = len(l[4])
                    common = set(l[1]) & set(l[2])
                    lc = [x for x in common]

                    logger.debug("  l[1] : %s" % (l[1]))
                    logger.debug("  l[2] : %s" % (l[2]))
                    logger.debug("  Common : %s" % (lc))
                    for x in common:
                        pc = pt.addConceptKeyType(x, "CommonTopic")
                        pc.count = len(lc)

        else:
            logger.debug("   similarity below threshold")


if __name__ == "__main__":
    filePPConcepts = "pptx.p"
    fileArchimateIn = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v23.archimate"
    fileArchimateOut = 'import_pp.archimate'
    fileConcepts = "req.p"

    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)

    #ia.logAll(tree, type="archimate:Requirement")
    ia.logAll(tree, type="archimate:BusinessFunction")

    concepts = Concepts("Requirement", "Requirement")
    for sentence in ia.dictName:
        logger.debug("%s" % sentence)

        d = concepts.addConceptKeyType(sentence, "Requirement")

        cleanSentence = ' '.join([word for word in sentence.split() if word not in stop])
        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
            if len(word) > 1 and pos[0] == "N":
                e = d.addConceptKeyType(word, "Word")
                f = e.addConceptKeyType(pos, "POS")

    Concepts.saveConcepts(concepts, fileConcepts)

    npbt = DocumentsSimilarity()
    npbt.createTopics(fileConcepts)
    nc = npbt.findSimilarties("documentsSimilarity.p")

    logger.info("Topics")
    listTopics = list()
    ncg = npbt.topicConcepts.getConcepts().values()
    for x in ncg:
        logger.debug("%s[%d]" % (x.name, x.count))
        lt = (x.name, x.count)
        listTopics.append(lt)

    for x in sorted(listTopics, key=lambda c: abs(c[1]), reverse=False):
        logger.info("Topic : %s[%d]" % (x[0], x[1]))