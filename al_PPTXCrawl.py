#!/usr/bin/python
#
# PPTX Crawl
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.PPTXCreateArchi import PPTXCreateArchil

from al_Constants import *

def PPTXCrawl():

    logger.info("Using : %s" % filePPTXIn)

    cpptx = PPTXCreateArchil(filePPTXIn)

    c = cpptx.crawlPPTX()

    c.logConcepts()

    Concepts.saveConcepts(c, fileConceptsPPTX)

if __name__ == "__main__":
    PPTXCrawl()

