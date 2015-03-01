
#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from subprocess import call

from nl_lib.Concepts import Concepts
from al_ArchiLib.Logger import *

logger = setupLogging(__name__)
logger.setLevel(INFO)

from py2neo import neo4j, node, rel
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

import pytest

#
# Script to reset Neo4J
#
resetNeo4J = "/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"

class ExportArchimateIntoNeo4J (object):

    listRelations = None
    fileArchimate = None
    gdb = None

    def __init__(self, fileArchimate, gdb):

        logger.info("Using : %s" % fileArchimate)
        self.fileArchimate = fileArchimate
        logger.info("Using : %s" % gdb)
        self.gdb = gdb

        logger.debug("Neo4J instance : %s" % gdb)
        self.graph = neo4j.GraphDatabaseService(gdb)

        self.al = ArchiLib(fileArchimate)

        self.clearNeo4J()

        self.listRelations = list()

    def addElement(self, x):

        tag = x.get(ARCHI_TYPE)[10:]
        text = x.text


        if x.attrib == None:
            prop = dict()
        else:
            prop = x.attrib

        for y in list(x):
            #
            #  Find ArchimateElement for DiagramObject
            #
            logger.debug("y.tag : %s" % y.tag)
            if y.tag == "documentation":
                logger.info("documentation : %s" % y.tag)
                prop["documentation"] = y.text

            if y.tag == "content":
                logger.info("content : %s" % y.tag)
                prop["content"] = y.text.rstrip()

            elif y.tag == "property":
                logger.info("property : %s" % y.tag)
                # <property key="Comments " value="Align to complete after the Contact and Lead Management project
                # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
                key = y.get("key")
                value = y.get("value")
                prop[key] = value

        name = x.get(ARCHI_TYPE)[10:]

        if text != None:
            prop["text"] = text.rstrip()

        if tag != None:
            prop["tag"] = tag.rstrip()

        ps = ""
        for k, v in prop.items():
            if k == "id":
                logger.debug("k=%s\t V=%s" % (k, v))
                ps = ps + " a%s:\"%s\", " % (k, v)
                continue

            if k <> ARCHI_TYPE:
                logger.debug("k=%s\t V=%s" % (k, v))
                ps = ps + " %s:\"%s\", " % (k, v)

        ps = ps[:-2]
        logger.debug("properties : .%s." % ps)

        qs = "MERGE (n:%s {%s, typeName:\"%s\"}) return n" % (name.strip(" "), ps, tag)

        logger.info("    Node Query : '%s'" % qs)

        query = neo4j.CypherQuery(self.graph, qs)

        return query.execute().data

    def createRelations(self):

        for x in self.listRelations:
            logger.info("    REL Query %s" % x)
            query = neo4j.CypherQuery(self.graph, x)
            query.execute().data

    def addRelation (self, parentElement, childElement, relation):

        pid = parentElement.get("id")
        cid = childElement.get("id")

        qs = "MATCH (n { aid:'%s'}), (m { aid:'%s'}) MERGE (n)-[r:%s]->(m) RETURN r" % (pid, cid, relation.replace(" ", "_"))

        self.listRelations.append(qs)

    def cypherQuery(self, qs):
        query = neo4j.CypherQuery(self.graph, qs)
        return query.execute().data

    #
    # export to Neo4J
    #
    # <child xsi:type="archimate:DiagramObject" id="013b04c7" textAlignment="2" targetConnections="ffa4ea15" archimateElement="88dbc529">
    #              <bounds x="300" y="96" width="120" height="76"/>
    #              <sourceConnection xsi:type="archimate:Connection" id="0a13c5e4" source="013b04c7" target="f959fa51" relationship="57b216b1"/>
    #              <sourceConnection xsi:type="archimate:Connection" id="2365c387" source="013b04c7" target="9770f99b" relationship="390c04ff"/>
    #            </child>

    def exportArchiDO(self, x):
        #
        # Iterate through Children of DiagramObject
        #
        for y in list(x):
            #
            #  Find ArchimateElement for DiagramObject
            #
            self.addRelation(x, y, "Diagram")

            for z in list(y):
                logger.info("z.tag : %s" % z.tag )

                #<documentation>Reporting tool that sits alone. BURT pulls in information form the Tours System
                # (Gates) and Contract System to create a near-real-time report used by Sales organization leadership
                # to identify the percentages of Tours vs. Sales at any given time.</documentation>

                if z.tag == "documentation":
                    x.attrib["documentation"] = z.text

                if z.tag == "content":
                    x.attrib["content"] = z.text.rtrim()

                elif z.tag == "property":
                    # <property key="Comments " value="Align to complete after the Contact and Lead Management project
                    # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
                    key = z.get("key")
                    value = z.get("value")
                    x.attrib[key] = value

                elif z.tag == "bounds":
                    attrib = z.attrib

                    zX = attrib["x"]
                    zY  = attrib["y"]
                    zH  = attrib["height"]
                    zW  = attrib["width"]

                    #logger.debug("    B - %s : %s : %s : %s" % (zX, zY, zH, zW))

                    x.attrib["x"] = zX
                    x.attrib["y"] = zY
                    x.attrib["height"] = zH
                    x.attrib["width"] = zW

                elif z.tag == "sourceConnection":
                    src = z.get("source")
                    srcDO = self.al.findDiagramObject(src)[0].attrib
                    sid = srcDO["archimateElement"]
                    srcElm = self.al.findElementByID(sid)[0]

                    trc = z.get("target")
                    tgtDO = self.al.findDiagramObject(trc)[0].attrib
                    tid = tgtDO["archimateElement"]
                    tgtElm  = self.al.findElementByID(tid)[0]

                    rrc = z.get("relationship")
                    relElm = self.al.findElementByID(rrc)[0]

                    rid = relElm.get(ARCHI_TYPE)[10:]
                    logger.info("    S - %s -> [%s] -> %s" % ((srcElm.get("name"), relElm.get("name"), tgtElm.get("name"))))

                    self.addElement(srcElm)
                    self.addElement(tgtElm)
                    self.addElement(relElm)

                    self.addRelation(srcElm, tgtElm, rid)

    def exportArchiDM(self, model):

        #
        # Find DiagramModel and add to Neo4j
        #
        element = self.al.findDiagramModelByName(model)
        logger.info("Model : %s[%s]" % (model, element.get("id")))
        self.addElement(element)

        #
        # Iterate through DiagramObject's
        #
        for x in list(element):
            logger.info("  DO - %s" % x.get("id"))
            self.addElement(x)

            nmodel = "DM_%s" % model
            nmodel = nmodel.replace(" ", "_")
            nmodel = nmodel.replace(".", "_")

            self.addRelation(element, x, nmodel)

            xid = x.get("archimateElement")
            if xid != None:
                aeid = self.al.findElementByID(xid)[0]
                logger.info("    AE - %s : %s[%s]" % (aeid.get("name"), aeid.tag, aeid.get(ARCHI_TYPE)))
                self.addElement(aeid)
                self.addRelation(x, aeid, "archimateElement")

            self.exportArchiDO(x)

        self.createRelations()

    def clearNeo4J(self):

        logger.info("Reset Neo4J Graph DB")
        call([resetNeo4J])

    def neo4jCounts(self):

        logger.info("Neo4J instance : %s" % self.gdb)
        nj = Neo4JLib(self.gdb)

        qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = nj.cypherQuery(qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v28.archimate"
    #model = "System Interaction- ToBe"

    model = "01.1 Market to Leads"

    eain = ExportArchimateIntoNeo4J(fileArchimate, gdb)

    eain.exportArchiDM(model)

    ArchiLib.stopTimer(start_time)