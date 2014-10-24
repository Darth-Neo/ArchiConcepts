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

import import_artifacts as ia
import CreateArchiFromConcepts as cafc

import pytest

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]

ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

def test_PPTXCrawl():
    #graph = NetworkXGraph()

    #path_to_presentation = "/Users/morrj140/PycharmProjects/ArchiConcepts/example2.pptx"
    #path_to_presentation = "/Users/morrj140/PycharmProjects/ArchiConcepts/ARP-TBX - High Level Solution_Draft_v9.pptx"
    #path_to_presentation = "/Users/morrj140/Development/GitRepository/ArchiConcepts/ARP-TBX - High Level Solution_Draft_v10a.pptx"
    #path_to_presentation = "/Users/morrj140/Development/GitRepository/ArchiConcepts/Accovia_Replacement_Messages.pptx"
    #path_to_presentation = "/Users/morrj140/Development/GitRepository/ArchiConcepts/ARP-TBX - Next Level Solution -v1.pptx"

    path_to_presentation = "/Users/morrj140/Development/GitRepository/ArchiConcepts/simple2.pptx"

    c = Concepts("Application", "Relations")

    cafc.crawlPPTX(c, path_to_presentation)

    #graphConcepts(c)

    c.logConcepts()

    Concepts.saveConcepts(c, "pptx.p")

    assert isinstance(c, Concepts)