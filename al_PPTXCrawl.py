#!/usr/bin/python
#
# PPTX Crawl
#
import os

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_lib.Constants import *
from al_lib.PPTXCreateArchi import PPTXCreateArchil


def PPTXCrawl(filePPTX):

    logger.info(u"Using : %s" % filePPTX)

    cpptx = PPTXCreateArchil(filePPTX)

    c = cpptx.crawlPPTX()

    c.logConcepts()

    Concepts.saveConcepts(c, fileConceptsPPTX)

if __name__ == u"__main__":

    path = os.getcwd()

    filePPTX = u"FY17DP.pptx"

    PPTXCrawl(filePPTX)

