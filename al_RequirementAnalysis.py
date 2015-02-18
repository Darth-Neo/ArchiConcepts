#!/usr/bin/python
#
# Requirement Analysis via NLP Chunks noun.verb(predicate)
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import logging
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

from lxml import etree

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from itertools import islice
from pattern.vector import count, words, PORTER, LEMMA
from pattern.vector import Document, Model, TFIDF, HIERARCHICAL
from pattern.vector import Vector, distance, NB
from pattern.db import csv
from pattern.en import parse, Sentence, parsetree

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

class Chunks(object):

    conceptFile = fileConceptsDocuments
    chunkFile = fileConceptsChunks
    concepts = None
    chunkConcepts = None

    def __init__(self, concepts=None):
        if concepts == None:
            logger.info("Loading : %s" % self.conceptFile)
            self.concepts = Concepts.loadConcepts(self.conceptFile)
        else:
            logger.info("Using   : %s" % concepts.name)
            self.concepts = concepts

        self.chunkConcepts = Concepts("Chunk", "Chunks")

    def getChunkConcepts(self):
        return self.chunkConcepts

    def createChunks(self):
        stop = stopwords.words('english')
        stop.append("This")
        stop.append("The")
        stop.append(",")
        stop.append(".")
        stop.append("..")
        stop.append("...")
        stop.append(".")
        stop.append(";")
        stop.append("and")

        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        tokenizer = RegexpTokenizer("[\w]+")

        for document in self.concepts.getConcepts().values():
            logger.info("%s" % document.name)
            d = self.chunkConcepts.addConceptKeyType(document.name, "Document")

            for sentence in document.getConcepts().values():
                logger.debug("%s(%s)" % (sentence.name, sentence.typeName))
                cleanSentence = ' '.join([word for word in sentence.name.split() if word not in stop])

                listSentence = list()

                for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                    logger.debug("Word: " + word + " POS: " + pos)

                    if pos[:1] == "N":
                    #if True:
                        lemmaWord = lemmatizer.lemmatize(word)
                        logger.debug("Word: " + word + " Lemma: " + lemmaWord)

                        morphWord = wn.morphy(word, wn.NOUN)
                        if morphWord != None:
                            logger.debug("Word: " + word + " Morph: " + morphWord)

                        synset = wn.synsets(word, pos='n')
                        logger.debug("synset : %s" %  synset)

                        if len(synset) != 0:
                            syn = synset[0]

                            root = syn.root_hypernyms()
                            logger.debug("root : %s" %  root)

                            mh = syn.member_holonyms()
                            logger.debug("member_holonyms : %s" %  mh)

                            hypernyms = syn.hypernyms()
                            logger.debug("hypernyms : %s" %  hypernyms)

                            if len(hypernyms) > 0:
                                hyponyms = syn.hypernyms()[0].hyponyms()
                                logger.debug("hyponyms : %s" %  hyponyms)
                            else:
                                hyponyms = None

                            listSentence.append((word, lemmaWord, pos, root, hypernyms, hyponyms))

                nounSentence = ""
                for word in listSentence:
                    nounSentence += word[1] + " "

                if len(nounSentence) > 2:
                    e = d.addConceptKeyType(nounSentence, "NounSentence")

                    for word in listSentence:
                        f = e.addConceptKeyType(word[0], word[2])
                        f.addConceptKeyType(word[1], "Lemma")

                logger.debug("%s = %s" % (cleanSentence, type(cleanSentence)))
                cleanSentence = cleanSentence.decode("utf-8", errors="ignore")
                pt = parsetree(cleanSentence, relations=True, lemmata=True)

                for sentence in pt:
                    logger.debug("relations: %s" % [x for x in sentence.relations])
                    logger.debug("subject  : %s" % [x for x in sentence.subjects])
                    logger.debug("verb     : %s" % [x for x in sentence.verbs])
                    logger.debug("object   : %s" % [x for x in sentence.objects])

                    if sentence.subjects is not None:
                        logger.debug("Sentence : %s" % sentence.chunks)

                        for chunk in sentence.chunks:
                            logger.debug("Chunk  : %s" % chunk)

                            relation = str(chunk.relation).encode("ascii", errors="ignore").strip()
                            role = str(chunk.role).encode("ascii", errors="ignore").strip()

                            logger.debug("Relation : %s" % relation)
                            logger.debug("Role     : %s" % role)

                            for subject in sentence.subjects:
                                logger.debug(" Subject.realtion : %s " % subject.relation)
                                logger.debug(" Subject : %s " % subject.string)
                                f = e.addConceptKeyType(subject.string, "SBJ")

                                for verb in sentence.verbs:
                                    if verb.relation == subject.relation:
                                        logger.debug("  Verb.realtion : %s " % verb.relation)
                                        logger.debug("  Verb   : %s " % verb.string)
                                        g = f.addConceptKeyType(verb.string, "VP")

                                        for obj in sentence.objects:
                                            if obj.relation == verb.relation:
                                                logger.debug("    Obj.realtion : %s " % obj.relation)
                                                logger.debug("    Object : %s " % obj.string)
                                                g.addConceptKeyType(obj.string, "OBJ")

        Concepts.saveConcepts(self.chunkConcepts, self.chunkFile)
        logger.info("Saved : %s" % self.chunkFile)

if __name__ == "__main__":

    al = ArchiLib(fa="/Users/morrj140/Documents/SolutionEngineering/Archimate Models/FOS V4.archimate")

    conceptsFile = fileRequirementsConcepts

    searchTypes = list()
    searchTypes.append("archimate:Requirement")
    nl = al.getTypeNodes(searchTypes)

    logger.info("Find Words in Requirements...")
    concepts = Concepts("Requirement", "Requirements")
    n = 0
    for sentence in nl:
        n += 1
        logger.debug("%s" % sentence)

        c = concepts.addConceptKeyType("Document" + str(n), "Document")
        d = c.addConceptKeyType(sentence, "Sentence" + str(n))

        if True and sentence != None:
            cleanSentence = ' '.join([word for word in sentence.split(" ") if word not in stop])
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                if len(word) > 1 and pos[0] == "N":
                    e = d.addConceptKeyType(word, "Word")
                    f = e.addConceptKeyType(pos, "POS")

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Saved : %s" % conceptsFile)

    chunks = Chunks(concepts)
    chunks.createChunks()

