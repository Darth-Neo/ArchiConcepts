#!/usr/bin/python
#
# Natural Language Processing of Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.4'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib


def createTagCloud(conceptFile, topic):

    start_time = ArchiLib.startTimer()

    concepts = Concepts.loadConcepts(conceptFile)

    tc = TopicCloud(concepts, font_path=u"/Users/morrj140/Fonts/DroidSans.ttf", imageFile=u"Requirements.png")

    tc.createTagCloud(topic)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    logger.debug(u"CWD : %s" % os.getcwd())

    #conceptFile = "TopicChunks.p"
    #topic = "Chunk"

    #conceptFile = u"topicsDict.p"
    #topic = u"Topic"

    #conceptFile = "archi.p"
    #topic="name"

    #conceptFile = "ngramsubject.p"
    #topic="NGRAM"

    conceptFile = u"reqs.p"
    topic = u"Word"

    conceptFile = u"chunks.p"
    topic = u"Lemma"
    #topic = "SBJ"
    #topic = "OBJ"
    #topic = "VP"
    #topic = "NN"
    #topic = "NNP"

    #conceptFile = "ngrams.p"
    #topic = "NGRAM"

    createTagCloud(conceptFile, topic)