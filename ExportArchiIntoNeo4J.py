
#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.3'
import os
import sys
from traceback import format_exc
from subprocess import call

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib
from al_Constants import *

from py2neo import neo4j, node, rel

#
# Script to reset Neo4J
#
resetNeo4J = "/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"

class ExportArchimateIntoNeo4J (object):
    listModels    = None
    listRelations = None
    fileArchimate = None
    gdb = None

    def __init__(self, fileArchimate, gdb, Reset=True):

        logger.info("Using : %s" % fileArchimate)
        self.fileArchimate = fileArchimate

        self.gdb = gdb
        logger.info("Neo4J instance : %s" % self.gdb)
        self.graph = neo4j.GraphDatabaseService(self.gdb)

        self.al = ArchiLib(fileArchimate)

        if Reset == True:
            self.clearNeo4J()

        self.listRelations = list()
        self.listModels    = list()

        self.getDiagramModels()

    #
    # Add an Archimate Element to Neo4J
    #
    def addElement(self, x):

        try:
            ps = ""
            typeName = x.get(ARCHI_TYPE)[10:].strip(" ")

            if x.attrib == None:
                prop = dict()
            else:
                prop = x.attrib

            if x.text != None:
                prop["text"] = x.text.rstrip()

            if x.tag != None:
                prop["tag"] = x.tag.rstrip()

            #
            #  Iterate through DiagramObject Children
            #
            for y in list(x):

                logger.debug("y.tag : %s" % y.tag)
                if y.tag == "documentation":
                    logger.debug("  documentation : %s" % y.tag)
                    prop["documentation"] = y.text

                if y.tag == "content":
                    logger.debug("content : %s" % y.tag)
                    prop["content"] = y.text.rstrip()

                #
                #  <property key="Comments " value="Align to complete after the Contact and Lead Management project
                # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
                #
                elif y.tag == "property":

                        logger.debug("property : %s" % y.tag)
                        key = str(y.get("key").encode('utf-8',errors='ignore')).rstrip(" ").replace(" ", "_")
                        value = str(y.get("value").encode('utf-8',errors='ignore')).rstrip(" ").replace(" ", "_")
                        logger.info("k[v] : %s[%s]" % (key, value))
                        prop[key] = value

            #
            # Get the properties
            #
            for k, v in prop.items():
                if k == "id":
                    logger.debug("k=%s\t V=%s" % (k, v))
                    ps = ps + " a%s:\"%s\", " % (k, v)
                    continue

                if k <> ARCHI_TYPE:
                    logger.debug("k=%s\t V=%s" % (k, v))
                    ps = ps + " %s:\"%s\", " % (k, v)

            # remove the last comma
            ps = ps[:-2]

            logger.debug("properties : .%s." % ps)

            qs = "MERGE (n:%s {%s, typeName:\"%s\"}) return n" % (typeName, ps, typeName)

            logger.debug("    Node Query : '%s'" % qs)

            return self.cypherQuery(qs)

        except:
            em = format_exc()
            logger.warn("Warning: %s" % (em))

    #
    # Add an Archimate Relations to Neo4J
    #
    def createRelations(self):

        for x in self.listRelations:
            logger.debug("    REL Query %s" % x)
            query = self.cypherQuery(x)


    def addRelation (self, parentElement, childElement, relation):

        pid = parentElement.get("id")
        cid = childElement.get("id")

        qs = "MATCH (n { aid:'%s'}), (m { aid:'%s'}) MERGE (n)-[r:%s]->(m) RETURN r" % (pid, cid, relation.replace(" ", "_"))
        logger.debug("    Rel Query : '%s'" % qs)
        self.listRelations.append(qs)

    #
    # Get all DiagramModels from Archimate XML
    #
    def getDiagramModels(self, folder="Views"):

        dm = self.al.getElementsFromFolder(folder)

        for x in dm.iter():
            if x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] == DIAGRAM_MODEL:
                logger.debug("DM : %s" % (x.tag))
                self.listModels.append(x)

    #
    # Iterate through all DiagramModels
    #
    def exportArchiDMS(self):

        for x in self.listModels:
            model = x.get("name")

            logger.info("Model - %s" % model)

            self.exportArchiDM(model)

        self.createAllIndexes()

        self.createRelations()

    #
    # Iterate through all DiagramObjects
    #
    def exportArchiDM(self, model):

        #
        # Find DiagramModel and add to Neo4j
        #
        element = self.al.findDiagramModelByName(model)
        logger.debug("Model : %s[%s]" % (model, element.get("id")))
        self.addElement(element)

        #
        # Iterate through DiagramObject's
        #
        for x in list(element):

            if x.get(ARCHI_TYPE) != "archimate:Note":
                logger.debug("DO[%s] - %s[%s]" % (x.tag, x.get("id"), x.get("archimateElement")))
                self.addElement(x)

                nmodel = "DM_%s" % model
                nmodel = nmodel.replace(" ", "_")
                nmodel = nmodel.replace(".", "_")
                nmodel = nmodel.replace("-", "_")
                nmodel = nmodel.replace("&", "and")
                nmodel = nmodel.replace("/", "_")

                self.addRelation(element, x, nmodel)

                xid = x.get("archimateElement")
                logger.debug("  xid : %s" % xid)

                aeid = self.al.findElementByID(xid)[0]
                logger.debug("  AE - %s : %s[%s]" % (aeid.get("name"), aeid.tag, aeid.get(ARCHI_TYPE)))
                self.addElement(aeid)
                self.addRelation(x, aeid, "archimateElement")

                self.exportArchiDO(x)
            else:
                if x.get(ARCHI_TYPE) == "archimate:Note":
                    for k, v in x.attrib.items():
                        logger.debug("    K : %s \t V : %s" % (k, v))


    #
    # export Archimate DiagramObject to Neo4J
    #
    # <child xsi:type="archimate:DiagramObject" id="013b04c7" textAlignment="2" targetConnections="ffa4ea15" archimateElement="88dbc529">
    #   <bounds x="300" y="96" width="120" height="76"/>
    #   <sourceConnection xsi:type="archimate:Connection" id="0a13c5e4" source="013b04c7" target="f959fa51" relationship="57b216b1"/>
    #   <sourceConnection xsi:type="archimate:Connection" id="2365c387" source="013b04c7" target="9770f99b" relationship="390c04ff"/>
    #</child>
    #
    def exportArchiDO(self, x):
        #
        # Iterate through Children of DiagramObject
        #
        for y in list(x):
            #
            #  Find ArchimateElement for DiagramObject
            #
            self.addRelation(x, y, "DiagramObject")

            for z in list(y):
                logger.debug("    z.tag : %s" % z.tag)

                # <documentation>
                # Reporting tool that sits alone. BURT pulls in information form the Tours System
                # (Gates) and Contract System to create a near-real-time report used by Sales organization leadership
                # to identify the percentages of Tours vs. Sales at any given time.
                # </documentation>
                if z.tag == "documentation" and len(z.text) > 0:
                    x.attrib["documentation"] = z.text

                if z.tag == "content" and len(z.text) > 0:
                    x.attrib["content"] = z.text.rtrim()

                # <property key="Comments " value="Align to complete after the Contact and Lead Management project
                # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
                elif z.tag == "property":
                    key = z.get("key")
                    value = z.get("value")
                    x.attrib[key] = value

                elif z.tag == "bounds":
                    attrib = z.attrib
                    zX = attrib["x"]
                    zY  = attrib["y"]
                    zH  = attrib["height"]
                    zW  = attrib["width"]

                    logger.debug("    B - %s : %s : %s : %s" % (zX, zY, zH, zW))

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
                    logger.info("  S - %s -> [%s] -> %s" % ((srcElm.get("name"), relElm.get(ARCHI_TYPE)[10:], tgtElm.get("name"))))

                    self.addElement(srcElm)
                    self.addElement(tgtElm)
                    self.addElement(relElm)

                    self.addRelation(srcElm, tgtElm, rid)

    #
    # Start New Graph DB
    #
    def clearNeo4J(self):

        logger.info("Reset Neo4J Graph DB")
        call([resetNeo4J])

    #
    # Entity Counts
    #
    def neo4jCounts(self):

        logger.info("Neo4J instance : %s" % self.gdb)
        #nj = Neo4JLib(self.gdb)

        qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = self.cypherQuery(qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))

    #
    # Neo4J Indexs and Queries
    #
    def createAllIndexes(self):
        for t in entities:
            self.createIndices(t)

    def createIndices(self, typeName):
        try:
            qs = "CREATE INDEX ON :%s (aid)" % (typeName)
            logger.debug("Index :" + qs)
            query = self.cypherQuery(qs)
        except:
            em = format_exc()
            logger.warn("Warning: %s" % (em))

    def dropAllIndexes(self):
        for t in entities:
            self.dropIndices(t)

    def dropIndices(self, typeName):
        try:
            qs = "DROP INDEX ON :%s (name)" % (typeName)
            logger.debug("Index :" + qs)
            query = self.cypherQuery(qs)
        except:
            em = format_exc()
            logger.warn("Warning: %s" % (em))

    def cypherQuery(self, qs):
        query = neo4j.CypherQuery(self.graph, qs)
        return query.execute().data

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v28.archimate"

    #model = "System Interaction- ToBe"
    #model = "01.1 Market to Leads"

    eain = ExportArchimateIntoNeo4J(fileArchimate, gdb)

    eain.exportArchiDMS()

    ArchiLib.stopTimer(start_time)