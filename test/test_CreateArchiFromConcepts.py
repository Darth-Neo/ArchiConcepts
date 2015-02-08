__author__ = 'morrj140'

import sys
import os
import StringIO
import csv
import random
import math
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from pptx import Presentation
from lxml import etree

from traceback import format_exc

from al_ArchiLib.Constants import *
from al_ArchiLib.Neo4JLib import Neo4JLib
import al_CreateArchiFromConcepts as cafc

import pytest

def test_PPTXCrawl():
    path_to_presentation = "/Users/morrj140/Development/GitRepository/ArchiConcepts/test/simple.pptx"

    c = Concepts("Application", "Relations")

    cafc.crawlPPTX(c, path_to_presentation)

    #graphConcepts(c)

    c.logConcepts()

    Concepts.saveConcepts(c, filePPTXConcepts)

    assert isinstance(c, Concepts)