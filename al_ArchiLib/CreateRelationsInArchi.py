#!/usr/bin/python
#
# Archimate Relations
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from lxml import etree

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

from ArchiLib import ArchiLib
from Constants import *

import pytest

class CreateRelationsInArchi(object):

    dictReq = dict()

    def __init__(self, fileArchimate):

        lemmatizer = WordNetLemmatizer()

        self.fileArchimate = fileArchimate

        self.al = ArchiLib(self.fileArchimate)

        self.al.logTypeCounts()

        etree.QName(ARCHIMATE_NS, 'model')

        self.tree = etree.parse(self.fileArchimate)

    def createRelations(self):

        self.dictReq = self.al.dictName

        xp = "//folder[@name='" + "Data" + "']"
        txp = self.tree.xpath(xp)

        logger.debug("len : %d" % len(txp))

        for x in txp[0].getchildren():

            nameEntity = x.get("name")

            if nameEntity == None:
                continue

            logger.info("----Checking Entity : %s----" % nameEntity)

            for z in self.dictReq.keys():

                if z == None:
                    continue

                logger.info("%s -- %s" % (x.get("name"), z))

                nxp = "//element[@id='" + self.dictReq[z] + "']"
                logger.info("nxp : %s" % nxp)
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
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.al.insertRel("element", "Relations", attrib)

        self.al.outputXMLtoFile()

def test_CreateRelationsInArchi():

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimateTest)

    rcia = CreateRelationsInArchi(fileArchimateTest)

    rcia.createRelations()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    test_CreateRelationsInArchi()