#!/usr/bin/python
#
# Natural Language Processing of Concepts from Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.TopicsModel import TopicsModel
from nl_lib.Constants import *

from lxml import etree

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

from al_ArchiLib.ArchiLib import ArchiLib

from al_Constants import *

import pytest

class Collocations(object):
    concepts         = None

    conceptsNGram        = None
    conceptNGramScore    = None
    conceptsNGramSubject = None

    ngramFile        = fileConceptsNGramFile
    ngramScoreFile   = fileConceptsNGramScoreFile
    ngramSubjectFile = fileConceptsNGramsSubject

    def __init__(self):
        self.conceptsNGram = Concepts("n-gram", "NGRAM")
        self.conceptsNGramScore = Concepts("NGram_Score", "Score")
        self.conceptsNGramSubject = Concepts("Subject", "Subjects")

    def getCollocationConcepts(self):
        return self.conceptsNGram, self.conceptsNGramScore, self.conceptsNGramSubject

    def find_collocations(self, concepts):
        self.concepts = concepts

        lemmatizer = WordNetLemmatizer()

        stopset = set(stop)
        filter_stops = lambda w: len(w) < 3 or w in stopset

        words = list()
        dictWords = dict()

        n = 0
        for document in self.concepts.getConcepts().values():
            n += 1
            logger.info("%d - Document %s" % (n, document.name[:25]))
            for concept in document.getConcepts().values():
               logger.debug("Word %s" % concept.name)

               for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                    logger.debug("Word: " + word + " POS: " + pos)
                    lemmaWord = lemmatizer.lemmatize(word.lower())
                    logger.debug("Word: " + word + " Lemma: " + lemmaWord)
                    words.append(lemmaWord)

                    if pos[0] == "N":
                        dictWords[lemmaWord] = word

        if False:
            for x in dictWords:
                logger.info("noun : %s" % x)

        bcf = BigramCollocationFinder.from_words(words)
        tcf = TrigramCollocationFinder.from_words(words)

        bcf.apply_word_filter(filter_stops)
        tcf.apply_word_filter(filter_stops)
        tcf.apply_freq_filter(3)

        listBCF = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 100)

        for bigram in listBCF:
            concept = ' '.join([bg for bg in bigram])
            e = self.conceptsNGram.addConceptKeyType(concept, "BiGram")
            logger.info("Bigram  : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)

        listTCF = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 100)

        for trigram in listTCF:
            concept = ' '.join([bg for bg in trigram])
            e = self.conceptsNGram.addConceptKeyType(concept, "TriGram")
            logger.info("Trigram : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)

        bcfscored = bcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)
        lt = sorted(bcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, "BiGram")
            for x in score[0]:
                e.addConceptKeyType(x, "BWord")
            e.count = count
            logger.debug("bcfscored: %s=%s" % (name, count))

        tcfscored = tcf.score_ngrams(TrigramAssocMeasures.likelihood_ratio)
        lt = sorted(tcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, "TriGram")
            for x in score[0]:
                e.addConceptKeyType(x, "TWord")
            e.count = count
            logger.debug("tcfscored: %s = %s" % (name, count))

        Concepts.saveConcepts(self.conceptsNGramScore, self.ngramScoreFile)
        Concepts.saveConcepts(self.conceptsNGram, self.ngramFile)

        for concept in self.conceptsNGram.getConcepts().values():
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                if pos[0] == "N":
                    e = self.conceptsNGramSubject.addConceptKeyType(word, pos)
                    e.addConceptKeyType(concept.name, "NGRAM")

        Concepts.saveConcepts(self.conceptsNGramSubject, self.ngramSubjectFile)

class DocumentsSimilarity(object):
    conceptsDoc = None
    conceptsSimilarity = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None
    topics = None
    topicConcepts = None
    lemmatizer = None

    def __init__(self):
        self.num_topics = 100
        self.num_words  = 50
        self.similarity = 0.95

    def createTopics(self, concepts):

        self.conceptsDoc = concepts

        self.tm = TopicsModel()

        logger.debug("--Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadConceptsWords(self.conceptsDoc)

        logger.info("--Read " + str(len(self.documentsList)) + " Documents, with " + str(self.wordcount) + " words.")

        logger.info("--Compute Topics--")
        self.topics = self.tm.computeTopics(self.documentsList, nt=self.num_topics, nw=self.num_words)

        if True:
            logger.info("--Log Topics--")
            self.tm.logTopics(self.topics)

        #self.listTopics = [x[0].encode('ascii', errors="ignore").strip() for x in self.topics]
        self.listTopics = [x[0] for x in self.topics]

        logger.info("--Saving Topics--")

        self.topicConcepts = self.tm.saveTopics(self.topics)

    def findSimilarties(self):

        conceptsSimilarityFile = "GapsSimilarity.p"

        logger.info("Compute Similarity")

        self.conceptsSimilarity = Concepts("ConceptsSimilarity", "Similarities")

        # Compute similarity between documents / concepts
        similarityThreshold = self.similarity

        for document in self.documentsList:
            indexNum = self.documentsList.index(document)

            self.df = self.conceptsDoc.getConcepts().keys()

            logger.debug("++conceptsDoc %s" % (self.df[indexNum]))

            logger.debug("  documentsList[" + str(indexNum) + "]=" + "".join(x + " " for x in document))

            # Show common topics
            d = [x.encode('ascii', errors="ignore").strip().replace("'", "") for x in document]
            e = [y.encode('ascii', errors="ignore").strip().replace("\"", "") for y in self.listTopics]

            s1 = set(e)
            s2 = set(d)
            common = s1 & s2
            lc = [x for x in common]
            logger.debug("  Common Topics : %s" % (lc))

            self.doComputation(indexNum, similarityThreshold, tfAddWords=True)

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info("Saved Concepts : %s" % conceptsSimilarityFile)

        return self.conceptsSimilarity

    def doComputation(self, j, similarityThreshold, tfAddWords=True):
        logger.debug("--doComputation--")
        pl = self.tm.computeSimilar(j, self.documentsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug("   similarity above threshold - %2.3f" % (100.0 * float(pl[0][0])))
            logger.debug("   pl:" + str(pl))

            for l in pl:
                if l[1] != l[2]:
                    logger.debug("  l:" + str(l))
                    l1 = "".join(x + " " for x in l[1])
                    ps = self.conceptsSimilarity.addConceptKeyType(l1, "Similar")
                    ps.count = TopicsModel.convertMetric(l[0])

                    l2 = "".join(x + " " for x in l[2])
                    pt = ps.addConceptKeyType(l2, "Concept")

                    common = set(l[1]) & set(l[2])
                    lc = [x for x in common]

                    logger.debug("  l    : %s" % l)
                    logger.debug("  l[1] : %s" % (l1))
                    logger.debug("  l[2] : %s" % (l2))
                    logger.debug("  Common : %s" % (lc))

                    if tfAddWords == True:
                        for x in common:
                            if not x in stop:
                                logger.debug("word : %s" % x)
                                pc = pt.addConceptKeyType(x, "CommonTopic")
                                pc.count = len(lc)

        else:
            logger.debug("   similarity below threshold")

def gapSimilarity(fileArchimate):

    lemmatizer = WordNetLemmatizer()

    logger.info("Using : %s" % fileArchimate)

    al = ArchiLib(fileArchimate)

    searchTypes = list()
    searchTypes.append("archimate:Requirement")
    nl = al.getTypeNodes(searchTypes)

    logger.info("Find Words...")
    concepts = Concepts("Requirement", "Requirements")

    n = 0
    for sentence in nl:
        n += 1
        logger.debug("%s" % sentence)

        c = concepts.addConceptKeyType("Document" + str(n), "Document")
        d = c.addConceptKeyType(sentence, "Sentence" + str(n))

        if sentence != None:
            cleanSentence = ' '.join([word for word in sentence.split(" ") if word not in stop])
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                if len(word) > 1 and pos[0] == "N":
                    lemmaWord =lemmatizer.lemmatize(word.lower())
                    e = d.addConceptKeyType(lemmaWord, "LemmaWord")
                    f = e.addConceptKeyType(pos, "POS")

    if True:
        logger.info("Find Collocations...")
        fc = Collocations()
        fc.find_collocations(concepts)

    if True:
        npbt = DocumentsSimilarity()

        logger.info("Create Topics")
        npbt.createTopics(concepts)

        if True:
            logger.info("Find Similarities")

            nc = npbt.findSimilarties()

            if True:
                logger.debug("Topics")
                listTopics = list()
                ncg = npbt.topicConcepts.getConcepts().values()
                for x in ncg:
                    logger.info("%s[%d]" % (x.name, x.count))
                    lt = (x.name, x.count)
                    listTopics.append(lt)

                logger.info("Topics Sorted")
                for x in sorted(listTopics, key=lambda c: abs(c[1]), reverse=False):
                    logger.info("Topic : %s[%d]" % (x[0], x[1]))

if __name__ == "__main__":
    gapSimilarity(fileArchimateTest)