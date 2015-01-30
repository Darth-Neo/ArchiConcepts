#!/usr/bin/python
#
# Natural Language Processing of Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

logger = Logger.setupLogging(__name__)

def createTopicsCloud(concepts, topic, numWords=50, scale=0.25):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1500, size_y=1200, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")

def getLemma(concept, lemmatizer):

    cl = list()

    for x in concept.name.split(" "):
        lemmaWord = lemmatizer.lemmatize(x.lower())
        cl.append(lemmaWord)

    return cl

def updateConceptLemma(concepts, lemmatizer):

    cl = getLemma(concepts, lemmatizer)

    for concept in concepts.getConcepts().values():
       logger.info("Word %s" % concept.name)

       for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
            logger.debug("Word: " + word + " POS: " + pos)
            lemmaWord = lemmatizer.lemmatize(word.lower())


if __name__ == "__main__":

    #conceptFile = "TopicChunks.p"
    #topic = "Chunk"

    conceptFile = "topicsDict.p"
    topic="Topic"

    #conceptFile = "archi.p"
    #topic="name"

    #conceptFile = "ngramsubject.p"
    #topic="NGRAM"

    #conceptFile = "req.p"
    #topic = "Word"

    #conceptFile = "chunks.p"
    #topic = "Lemma"
    #topic = "SBJ"
    #topic = "OBJ"
    #topic = "VP"
    #topic = "NN"
    #topic = "NNP"

    #conceptFile = "ngrams.p"
    #topic = "NGRAM"

    lemmatizer = WordNetLemmatizer()

    #directory = "/Users/morrj140/Development/GitRepository/DirCrawler/DVC_20141211_100141"
    directory = os.getcwd()

    os.chdir(directory)

    c = Concepts("GraphConcepts", "GRAPH")

    updateConceptLemma(c, lemmatizer)

    filePath = directory + os.sep + conceptFile
    logger.info("Loading Topics from : " + filePath)

    concepts = Concepts.loadConcepts(filePath)

    createTopicsCloud(concepts, topic)

