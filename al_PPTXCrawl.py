#!/usr/bin/python
#
# PPTX Crawl
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(Logger.DEBUG)

import math

from pptx import Presentation
from lxml import etree

from traceback import format_exc

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.PPTXCreateArchi import PPTXCreateArchil

if __name__ == "__main__":
    logger.info("Using : %s" % filePPTXCrawl)

    cpptx = PPTXCreateArchil(filePPTXCrawl)

    c = cpptx.crawlPPTX()

    c.logConcepts()

    Concepts.saveConcepts(c, filePPTXConcepts )


