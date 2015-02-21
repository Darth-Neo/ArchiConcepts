#!/usr/bin/python
#
# Archimate Relations
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import time
import random
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import ArchiLib as AL

from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Constants import *

class CreateRelationsInArchi(object):

    dictReq = dict()

    def __init__(self):

        lemmatizer = WordNetLemmatizer()

        # Archimate
        self.fileArchimate = fileArchimate
        self.fileExport="report" + time.strftime("%Y%d%m_%H%M%S") +".csv"

        al = ArchiLib(self.fileArchimate, self.fileExport)

        al.logTypeCounts()

        etree.QName(ARCHIMATE_NS, 'model')

        self.tree = etree.parse(self.fileArchimate)

    def createRelations(self):

        self.dictReq = self.al.dictName

        xp = "//folder[@name='" + "Data" + "']"
        txp = self.tree.xpath(xp)

        logger.debug("len : %d" % len(txp))

        for x in txp[0].getchildren():

            nameEntity = x.get("name")

            logger.info("----Checking Entity : %s----" % nameEntity)

            for z in self.dictReq.keys():
                logger.debug("%s -- %s" % (x.get("name"), z))

                nxp = "//element[@id='" + self.dictReq[z] + "']"
                ntxp = self.al.tree.xpath(nxp)

                if (len(ntxp) != 0) and (nameEntity in z):
                    wv = ntxp[0].get("name")
                    wy = self.al._cleanCapital(wv)

                    if wy == None:
                        continue
                    logger.info("%s ==> %s" % (x.get("name"), wy))

                    attrib = dict()
                    attrib["source"] = x.get("id")
                    attrib["target"] = ntxp[0].get("id")
                    attrib[AL.ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.al.insertRel("element", "Relations", self.tree, attrib)

        self.al.outputXMLtoFile()

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    rcia = CreateRelationsInArchi()

    rcia.createRelations()

    ArchiLib.stopTimer(start_time)