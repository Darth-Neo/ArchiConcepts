__author__ = 'morrj140'

#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

logger = Logger.setupLogging(__name__)

class Collocations(object):
    concepts         = None

    conceptsNGram        = None
    conceptNGramScore    = None
    conceptsNGramSubject = None

    conceptFile      = "documents.p"

    ngramFile        = "ngrams.p"
    ngramScoreFile   = "ngramscore.p"
    ngramSubjectFile = "ngramsubject.p"

    def __init__(self, conceptFile=None):
        if conceptFile == None:
            conceptFile      = "documents.p"

        logger.info("Load Concepts from %s " % (conceptFile))
        self.concepts = Concepts.loadConcepts(conceptFile)
        logger.info("Loaded Concepts")

        self.conceptsNGram = Concepts("n-gram", "NGRAM")
        self.conceptsNGramScore = Concepts("NGram_Score", "Score")
        self.conceptsNGramSubject = Concepts("Subject", "Subjects")

    def getCollocationConcepts(self):
        return self.conceptsNGram, self.conceptsNGramScore, self.conceptsNGramSubject

    def find_collocations(self):
        stop = stopwords.words('english')
        stop.append("This")
        stop.append("The")
        stop.append(",")
        stop.append(".")
        stop.append("..")
        stop.append("...")
        stop.append("...).")
        stop.append("\")..")
        stop.append(".")
        stop.append(";")
        stop.append("/")
        stop.append(")")
        stop.append("(")
        stop.append("must")
        stop.append("system")

        lemmatizer = WordNetLemmatizer()

        stopset = set(stop)
        filter_stops = lambda w: len(w) < 3 or w in stopset

        words = list()

        dictWords = dict()

        for document in self.concepts.getConcepts().values():
            logger.debug(document.name)
            for concept in document.getConcepts().values():
               logger.debug(concept.name)

               for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                    logger.debug("Word: " + word + " POS: " + pos)
                    lemmaWord = lemmatizer.lemmatize(word.lower())
                    logger.debug("Word: " + word + " Lemma: " + lemmaWord)
                    words.append(lemmaWord)

                    if pos[0] == "N":
                        dictWords[lemmaWord] = word


        for x in dictWords.keys():
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

if __name__ == "__main__":
    fileConcepts = "document.p"
    fc = Collocations(fileConcepts)
    fc.find_collocations()

