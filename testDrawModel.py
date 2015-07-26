import os
import pytest
from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_Constants import *
from al_DrawModel import DrawModels

if __name__ == u"__main__":

    fileArchimate = os.getcwd() + os.sep + u"test" + os.sep + u"test.archimate"

    dm = DrawModels(fileArchimate)

    elements = list()

    #
    # Elements
    #
    tag = u"element"
    folder = u"Business"
    attrib = dict()
    attrib[NAME] = u"DO%d" % dm.n
    attrib[ARCHI_TYPE] = u"archimate:BusinessObject"
    AE_ID_1 = dm.createArchimateElement(tag, folder, attrib)

    dm.n += 1
    tag = u"element"
    folder = u"Business"
    attrib = dict()
    attrib[NAME] = u"DO%d" % dm.n
    attrib[ARCHI_TYPE] = u"archimate:BusinessObject"
    AE_ID_2 = dm.createArchimateElement(tag, folder, attrib)

    dm.n += 1
    tag = u"element"
    folder = u"Relations"
    attrib = dict()
    attrib[ID] = dm.al.getID()
    attrib[u"source"] = AE_ID_1
    attrib[u"target"] = AE_ID_2
    attrib[ARCHI_TYPE] = u"archimate:AssociationRelationship"
    R_ID = dm.createArchimateRelations(tag, folder, attrib)

    nl = list()
    nl.append(AE_ID_1)
    nl.append(AE_ID_2)
    nl.append(R_ID)
    elements.append(nl)

    dm.drawModel(elements)

    dm.outputXMLtoFile()

