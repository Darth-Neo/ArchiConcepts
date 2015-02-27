
#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportModel import ExportArchiModel

from al_Constants import *

import pytest

#
# <child xsi:type="archimate:DiagramObject" id="013b04c7" textAlignment="2" targetConnections="ffa4ea15" archimateElement="88dbc529">
#              <bounds x="300" y="96" width="120" height="76"/>
#              <sourceConnection xsi:type="archimate:Connection" id="0a13c5e4" source="013b04c7" target="f959fa51" relationship="57b216b1"/>
#              <sourceConnection xsi:type="archimate:Connection" id="2365c387" source="013b04c7" target="9770f99b" relationship="390c04ff"/>
#            </child>

def exportArchiIntoNeo4J(fileArchimate, model, fileCSVExport):

    start_time = ArchiLib.startTimer()

    al = ArchiLib(fileArchimate)

    element = al.findElement(model)

    for x in list(element):
        logger.info("DM - %s" % x.get("name"))

        for y in list(x):

            yid = y.get("archimateElement")

            eid = al.findElementByID(yid)[0]

            logger.info("  DO - %s : %s[%s]" % (eid.get("name"), y.tag, y.get(ARCHI_TYPE)))

            for z in list(y):

                if z.tag == "bounds":
                    attrib = z.attrib

                    zX = attrib["x"]
                    zY  = attrib["y"]
                    zH  = attrib["height"]
                    zW  = attrib["width"]

                    logger.info("    B - %s : %s : %s : %s" % (zX, zY, zH, zW))

                elif z.tag == "sourceConnection":
                    src = z.get("source")
                    trc = z.get("target")
                    rrc = z.get("relationship")

                    srcNode = al.findDiagramObject(src)[0].attrib
                    trNode = al.findDiagramObject(trc)[0].attrib

                    sid = srcNode["archimateElement"]
                    tid = trNode["archimateElement"]

                    srcName = al.findElementByID(sid)[0]
                    trName  = al.findElementByID(tid)[0]


                    rlNode = al.findElementByID(rrc)[0]
                    rid = rlNode.get(ARCHI_TYPE)[10:]

                    logger.info("    S - %s -> [%s] -> %s" % ((srcName.get("name"), rid, trName.get("name"))))

                else:
                    attrib = z.attrib

                    id = attrib["archimateElement"]

                    eid = al.findElementByID(id)[0]

                    logger.info("    EL - %s : %s[%s]" % (eid.get("name"), z.tag, z.get(ARCHI_TYPE)))

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v28.archimate"
    model = "System Interaction- ToBe"

    exportArchiIntoNeo4J(fileArchimate, model, fileCSVExport)
