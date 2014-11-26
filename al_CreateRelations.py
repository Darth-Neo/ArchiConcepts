#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
import sys
import os
import StringIO
import csv
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

import al_ArchiLib as al

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]

ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

def relateEntities(tree, folder, subfolder, eType, v1, v2):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    xp = "//folder[@name='" + folder + "']"
    tag = "element"

    # <folder name="Process" id="e23b1e50">

    attrib = dict()
    attrib["id"] = al.getID()
    attrib["name"] = subfolder
    al.insertNode("folder", folder, tree, attrib)

    folder = subfolder

    CM1 = v1.decode(encoding='UTF-8',errors='ignore').lstrip()
    CM2 = v2.decode(encoding='UTF-8',errors='ignore').lstrip()

    C1 = CM1
    attrib = dict()
    attrib["name"] = CM1
    attrib[ARCHI_TYPE] = eType
    al.insertNode(tag, folder, tree, attrib)
    CM1_ID = attrib["id"]

    C2 = CM2
    attrib = dict()
    attrib["name"] = CM2
    attrib[ARCHI_TYPE] = eType
    al.insertNode(tag, folder, tree, attrib)
    CM2_ID = attrib["id"]

    attrib = dict()
    attrib["source"] = CM1_ID
    attrib["target"] = CM2_ID
    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
    al.insertRel(tag, "Relations", tree, attrib)


def checkEntity(d, e):

    fl  = list()

    for x in d.keys():
        y = al.cleanCapital(x)

        if e in y:
            logger.debug("dictName[%s] : %s" % (d[x], y))
            fl.append(d[x])

    return fl

def maxSimilarity(a, b):

    maxSim = 0
    mA = None
    mB = None

    #
    # Only Compare same part of speech
    #
    for x in a:
        #for y in b:
        if True:
            #wsim = x.path_similarity(y)
            #wsim = wn.lch_similarity(x, y)

            #wsim = x.wup_similarity(b)

            wsim = x.res_similarity(b, brown_ic)
            #wsim = x.jcn_similarity(b, brown_ic)
            #wsim = x.jcn_similarity(b, brown_ic)

            if wsim > maxSim:
                maxSim = wsim
                mA = x
                mB = y

    return maxSim, mA, mB

def checkSimilarity(d, e, THRESHOLD=0.79):

    fl  = list()

    for x in d.keys():

        y = al.cleanCapital(x)

        logger.debug("dict[x] : %s" % (y))

        for wx in y.split(" "):
            logger.debug("wx : %s" % (wx))

            if not (wx.lower() == e.lower()):

                try:
                    if False:
                        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(wy)):
                            lemmaWord = lemmatizer.lemmatize(word)
                            if pos[0] == "N":
                                logger.info("Word: %s Lemma: %s" % (word, lemmaWord))

                    wdx = wn.synsets(wx)
                    logger.debug("  %s.sysset : %s" % (wx, wdx))

                    wde = wn.synset("%s.n.01" % e)
                    #wde = wn.synsets(e)
                    logger.debug("  %s.sysset : %s" % (e, wde))

                    ms, ma, mb = maxSimilarity(wdx, wde)

                    if ms  > THRESHOLD:
                        logger.info("        SIW %s : %s[%s] is %3.2f" % (x, wx, mb, ms))
                        fl.append(d[x])
                except:
                    pass

    return fl


if __name__ == "__main__":
    lemmatizer = WordNetLemmatizer()

    # Archimate
    fileArchimate = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v18.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    treeArchi = etree.parse(fileArchimate)

    testClean = "getTravelAgencyResponse"
    logger.debug("clean : %s - %s" % (testClean, al.cleanCapital(testClean)))

    al.logAll(treeArchi)

    #relateEntities(treeArchi, "Entities", "archimate:ApplicationService", nFile, method)

    xp = "//folder[@name='" + "Entity" + "']"
    txp = treeArchi.xpath(xp)

    logger.debug("len : %d" % len(txp))

    for x in txp[0].getchildren():

        nameEntity = x.get("name")

        y = al.cleanCapital(nameEntity)

        if len(y.split(" ")) > 1:
            continue

        logger.info("----Checking Entity : %s----" % y)

        fl = checkSimilarity(al.dictName, y, THRESHOLD=0.85)

        #fl = checkEntity(dictName, y)

        # May need to change to dict for uniqueness
        for z in fl:
            logger.debug("%s -- %s" % (x.get("name"), z))

            nxp = "//element[@id='" + z + "']"
            ntxp = treeArchi.xpath(nxp)

            if len(ntxp) != 0:
                wv = ntxp[0].get("name")
                wy = al.cleanCapital(wv)
                if wy == None:
                    continue
                logger.info("%s ==> %s" % (x.get("name"), wy))

                attrib = dict()
                attrib["source"] = x.get("id")
                attrib["target"] = ntxp[0].get("id")
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                al.insertRel("element", "Relations", treeArchi, attrib)

    # outputXML(treeArchi)