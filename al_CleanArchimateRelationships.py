#!/usr/bin/python
#
#  Clean Archimate Relationships
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

from lxml import etree


def cleanArchimateRelationships():

    # fileArchimate is defined in al_Constants
    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    n = 0
    countInvalid = 0

    for x in al.tree.getroot().iter():
        n += 1

        try:

            if x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] in relations.values():
                sid = x.get("source")
                srcElm = al.findElementByID(sid)[0]

                tid = x.get("target")
                tgtElm  = al.findElementByID(tid)[0]

                if srcElm == None or tgtElm == None:
                    logger.warn("Invalid Relationship : %s[%s]" % (x.get("id"), x.get(ARCHI_TYPE)))
                else:
                    logger.debug("Valid Relationship   : %s[%s]" % (x.get("id"), x.get(ARCHI_TYPE)))

            #<child xsi:type="archimate:DiagramObject" id="2be1001e" textAlignment="2" archimateElement="eedbdc28">
                #<bounds x="692" y="624" width="120" height="55"/>
                #<sourceConnection xsi:type="archimate:Connection" id="c90d2077" source="2be1001e" target="aff3d6b3" relationship="56057f65"/>
                #<sourceConnection xsi:type="archimate:Connection" id="d5cac998" source="2be1001e" target="dfa5c47b" relationship="99bc54ab"/>
                #<sourceConnection xsi:type="archimate:Connection" id="3174a55b" source="2be1001e" target="0308d4c3" relationship="67e21821"/>
            #</child>
            elif x.attrib.has_key(ARCHI_TYPE) and x.get(ARCHI_TYPE) == DIAGRAM_OBJECT:
                ae = x.get("archimateElement")
                aeDO = al.findDiagramObject(ae)[0].attrib
                aeid = aeDO["archimateElement"]
                aeElm = al.findElementByID(aeid)[0]

                logger.debug("%s[%s] " % (aeElm.get("name"), aeElm.get(ARCHI_TYPE)))

            elif x.attrib.has_key(ARCHI_TYPE) and x.tag == "sourceConnection":

                src = x.get("source")
                srcDO = al.findDiagramObject(src)[0].attrib
                sid = srcDO["archimateElement"]
                srcElm = al.findElementByID(sid)[0]

                trc = x.get("target")
                tgtDO = al.findDiagramObject(trc)[0].attrib
                tid = tgtDO["archimateElement"]
                tgtElm  = al.findElementByID(tid)[0]

                rrc = x.get("relationship")
                relElm = al.findElementByID(rrc)[0]
                rid = relElm.get(ARCHI_TYPE)[10:]

                logger.debug("  S - %s -> [%s] -> %s" % ((srcElm.get("name"), rid, tgtElm.get("name"))))

            else:
                if x.attrib.has_key("name") and x.attrib.has_key(ARCHI_TYPE):
                    logger.info("Skipping - %s[%s] - %s" % (x.get(ARCHI_TYPE)[10:], x.get("id"), x.get("name")[:20]))
                else:
                    logger.debug("Skipping - %s[%s]" % (x.tag, x.get("id")))
        except:
            countInvalid += 1
            logger.error("Error - %s[%s]" % (x.tag, x.get("id")))

    logger.info("Validated %d Elements" % n)

    al.logTypeCounts()

if __name__ == "__main__":
    cleanArchimateRelationships()
