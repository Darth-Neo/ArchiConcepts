#!/usr/bin/python
#
# PPTX Crawl
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_lib.Constants import *
from al_lib.PPTXCreateArchi import PPTXCreateArchil


def PPTXCrawl():

    logger.info(u"Using : %s" % filePPTXIn)

    cpptx = PPTXCreateArchil(filePPTXIn)

    c = cpptx.crawlPPTX()

    c.logConcepts()

    Concepts.saveConcepts(c, fileConceptsPPTX)

if __name__ == u"__main__":
    PPTXCrawl()

