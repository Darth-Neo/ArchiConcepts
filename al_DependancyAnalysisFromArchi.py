#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.DependencyAnalysis import *

if __name__ == "__main__":
    concepts = dependancyAnalysis()
    concepts.logConcepts()