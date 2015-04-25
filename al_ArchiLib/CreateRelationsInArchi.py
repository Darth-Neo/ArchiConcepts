#!/usr/bin/python
#
# Archimate Relations
#
__author__ = u'morrj140'
__VERSION__ = u'0.1'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from lxml import etree

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic(u'ic-brown.dat')

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

        etree.QName(ARCHIMATE_NS, u'model')

        self.tree = etree.parse(self.fileArchimate)

    def createRelations(self, fileArchimateImport):

        self.dictReq = self.al.dictName

        xp = u"//folder[@name='" + u"Data" + u"']"
        txp = self.tree.xpath(xp)

        logger.debug(u"len : %d" % len(txp))

        for x in txp[0].getchildren():

            nameEntity = x.get(u"name")

            if nameEntity == None:
                continue

            logger.info(u"----Checking Entity : %s----" % nameEntity)

            for z in self.dictReq.keys():

                if z == None:
                    continue

                logger.info(u"%s -- %s" % (x.get(u"name"), z))

                nxp = u"//element[@id='" + self.dictReq[z] + "']"
                logger.info(u"nxp : %s" % nxp)
                ntxp = self.al.tree.xpath(nxp)

                if (len(ntxp) != 0) and (nameEntity in z):
                    wv = ntxp[0].get(u"name")
                    wy = self.al._cleanCapital(wv)

                    if wy == None:
                        continue
                    logger.info(u"%s ==> %s" % (x.get(u"name"), wy))

                    attrib = dict()
                    attrib[u"source"] = x.get(u"id")
                    attrib[u"target"] = ntxp[0].get(u"id")
                    attrib[ARCHI_TYPE] = u"archimate:AssociationRelationship"
                    self.al.insertRel(u"element", u"Relations", attrib)

        self.al.outputXMLtoFile(fileArchimateImport)

def test_CreateRelationsInArchi():

    start_time = ArchiLib.startTimer()

    logger.info(u"Using : %s" % fileArchimateTest)

    rcia = CreateRelationsInArchi(fileArchimateTest)

    rcia.createRelations()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    test_CreateRelationsInArchi()