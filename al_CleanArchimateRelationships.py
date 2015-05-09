#!/usr/bin/python
#
#  Clean Archimate Relationships
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib


def cleanArchimateRelationships(fileArchimate):

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    n = 0
    countInvalid = 0

    for x in al.tree.getroot().iter():
        n += 1

        try:

            if ARCHI_TYPE in x.attrib and x.attrib[ARCHI_TYPE] in relations.values():
                sid = x.get(u"source")
                srcElm = al.findElementByID(sid)[0]

                tid = x.get(u"target")
                tgtElm = al.findElementByID(tid)[0]

                if srcElm is None or tgtElm is None:
                    logger.warn(u"Invalid Relationship : %s[%s]" % (x.get(u"id"), x.get(ARCHI_TYPE)))
                else:
                    logger.debug(u"Valid Relationship   : %s[%s]" % (x.get(u"id"), x.get(ARCHI_TYPE)))

            # <child xsi:type="archimate:DiagramObject" id="2be1001e" textAlignment="2" archimateElement="eedbdc28">
                # <bounds x="692" y="624" width="120" height="55"/>
                # <sourceConnection xsi:type="archimate:Connection" id="c90d2077" source="2be1001e" target="aff3d6b3" relationship="56057f65"/>
                # <sourceConnection xsi:type="archimate:Connection" id="d5cac998" source="2be1001e" target="dfa5c47b" relationship="99bc54ab"/>
                # <sourceConnection xsi:type="archimate:Connection" id="3174a55b" source="2be1001e" target="0308d4c3" relationship="67e21821"/>
            # </child>
            elif ARCHI_TYPE in x.attrib and x.get(ARCHI_TYPE) == DIAGRAM_OBJECT:
                ae = x.get(u"archimateElement")
                aeDO = al.findDiagramObject(ae)[0].attrib
                aeid = aeDO[u"archimateElement"]
                aeElm = al.findElementByID(aeid)[0]

                logger.debug(u"%s[%s] " % (aeElm.get(u"name"), aeElm.get(ARCHI_TYPE)))

            elif ARCHI_TYPE in x.attrib and x.tag == u"sourceConnection":

                src = x.get(u"source")
                srcDO = al.findDiagramObject(src)[0].attrib
                sid = srcDO[u"archimateElement"]
                srcElm = al.findElementByID(sid)[0]

                trc = x.get(u"target")
                tgtDO = al.findDiagramObject(trc)[0].attrib
                tid = tgtDO[u"archimateElement"]
                tgtElm = al.findElementByID(tid)[0]

                rrc = x.get(u"relationship")
                relElm = al.findElementByID(rrc)[0]
                rid = relElm.get(ARCHI_TYPE)[10:]

                logger.debug(u"  S - %s -> [%s] -> %s" % ((srcElm.get(u"name"), rid, tgtElm.get(u"name"))))

            else:
                if u"name" in x.attrib and x.attrib.has_key(ARCHI_TYPE):
                    logger.info(u"Skipping - %s[%s] - %s" % (x.get(ARCHI_TYPE)[10:], x.get(u"id"), x.get(u"name")[:20]))
                else:
                    logger.debug(u"Skipping - %s[%s]" % (x.tag, x.get(u"id")))
        except:
            countInvalid += 1
            logger.error(u"Error - %s[%s]" % (x.tag, x.get(u"id")))

    logger.info(u"Validated %d Elements" % n)

    al.logTypeCounts()

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v40.archimate"

    cleanArchimateRelationships(fileArchimate)
