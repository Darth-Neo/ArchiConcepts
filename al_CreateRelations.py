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

from al_ArchiLib import *

from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

def relateEntities(tree, folder, subfolder, eType, v1, v2):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    xp = "//folder[@name='" + folder + "']"
    tag = "element"

    # <folder name="Process" id="e23b1e50">

    attrib = dict()
    attrib["id"] = getID()
    attrib["name"] = subfolder
    insertNode("folder", folder, tree, attrib)

    folder = subfolder

    CM1 = v1.decode(encoding='UTF-8',errors='ignore').lstrip()
    CM2 = v2.decode(encoding='UTF-8',errors='ignore').lstrip()

    C1 = CM1
    attrib = dict()
    attrib["name"] = CM1
    attrib[ARCHI_TYPE] = eType
    insertNode(tag, folder, tree, attrib)
    CM1_ID = attrib["id"]

    C2 = CM2
    attrib = dict()
    attrib["name"] = CM2
    attrib[ARCHI_TYPE] = eType
    insertNode(tag, folder, tree, attrib)
    CM2_ID = attrib["id"]

    attrib = dict()
    attrib["source"] = CM1_ID
    attrib["target"] = CM2_ID
    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
    insertRel(tag, "Relations", tree, attrib)


def checkEntity(d, e):

    fl  = list()

    for x in d.keys():
        y = cleanCapital(x)

        if e in y:
            logger.debug("dictName[%s] : %s" % (d[x], y))
            fl.append(d[x])

    return fl

def maxSimilarity(a, b):

    maxSim = 0
    mA = None
    mB = None
    y = 0

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

        y = cleanCapital(x)

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
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v9.archimate"
    etree.QName(ARCHIMATE_NS, 'model')

    treeArchi = etree.parse(fileArchimate)

    listType = ("archimate:ApplicationService")
    logAll(treeArchi, type=listType)
    dictReq = dictName

    xp = "//folder[@name='" + "Data" + "']"
    txp = treeArchi.xpath(xp)

    logger.debug("len : %d" % len(txp))

    for x in txp[0].getchildren():

        nameEntity = x.get("name")

        logger.info("----Checking Entity : %s----" % nameEntity)

        for z in dictReq.keys():
            logger.debug("%s -- %s" % (x.get("name"), z))

            nxp = "//element[@id='" + dictReq[z] + "']"
            ntxp = treeArchi.xpath(nxp)

            if (len(ntxp) != 0) and (nameEntity in z):
                wv = ntxp[0].get("name")
                wy = cleanCapital(wv)

                if wy == None:
                    continue
                logger.info("%s ==> %s" % (x.get("name"), wy))

                attrib = dict()
                attrib["source"] = x.get("id")
                attrib["target"] = ntxp[0].get("id")
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel("element", "Relations", treeArchi, attrib)

    outputXML(treeArchi)