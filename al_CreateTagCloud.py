#!/usr/bin/python
#
# Natural Language Processing of Information
#

__author__ = 'morrj140'

import os
from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

logger = Logger.setupLogging(__name__)

def createTopicsCloud(concepts, topic, numWords=25, scale=0.5):
    logger.info("Starting Tag Cloud...")

    tc = TopicCloud(concepts, os.getcwd() + os.sep)

    logger.info("Create Tag Cloud")

    # Note: the first parameter must match for a topic cloud image to be created!
    tc.createCloudImage(topic, size_x=1500, size_y=1200, numWords=numWords, scale=scale)

    logger.info("Complete createTopicsCloud")


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

    #directory = "/Users/morrj140/Development/GitRepository/DirCrawler/DVC_20141211_100141"
    directory = os.getcwd()

    os.chdir(directory)

    c = Concepts("GraphConcepts", "GRAPH")

    filePath = directory + os.sep + conceptFile
    logger.info("Loading Topics from : " + filePath)

    concepts = Concepts.loadConcepts(filePath)

    createTopicsCloud(concepts, topic)

