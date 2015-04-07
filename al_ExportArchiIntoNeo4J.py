
#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = 'morrj140'
__VERSION__ = '0.3'
import os
import sys
import time
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
resetNeo4J = "/Users/morrj140/Development/neo4j/bin/reset.sh"

class ExportArchimateIntoNeo4J (object):
    listModels    = None
    listRelations = None
    fileArchimate = None
    gdb = None
    textExport = None
    errorNodes = None

    nMin = 0
    nMax = 76
    nSpaces = 0

    def __init__(self, gdb, fileArchimate=None, subdirArchimate=None, Reset=True):

        if fileArchimate <> None:
            self.fileArchimate = fileArchimate
        else:
            if subdirArchimate <> None:
                self.subdirArchimate = subdirArchimate
            else:
                self.subdirArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/ExportIntoNeo4J"
                self.fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V4.archimate"

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

        self.listDiagramModels()

        self.textExport = list()

        self.errorNodes  = list()

    #
    # Get all DiagramModels from Archimate XML
    #
    def listDiagramModels(self, folder="Views"):

        dm = self.al.getElementsFromFolder(folder)

        for x in dm.iter():
            if x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] == DIAGRAM_MODEL:
                logger.debug("Exporting model : %s" % (x.get("name")))
                self.listModels.append(x)

        logger.info("Found %d Models" % len(self.listModels))

    def exportArchiElements(self):

        logger.debug("Export Archimate Elements")

        n = 0

        for x in self.al.tree.getroot().iter():
            try:
                n += 1
                if x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] in entities.values():
                    logger.debug("EL : %s[%s]" % (x.get("name"), x.get(ARCHI_TYPE)))
                    parentPath = self.getParentPath(x)
                    x.attrib["parentPath"] = parentPath
                    self.addElement(x)

                elif x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] in relations.values():
                    logger.debug("EL : %s[%s]" % (x.get("name"), x.get(ARCHI_TYPE)))
                    parentPath = self.getParentPath(x)
                    x.attrib["parentPath"] = parentPath
                    self.addElement(x)

                    sid = x.get("source")
                    srcElm = self.al.findElementByID(sid)[0]

                    tid = x.get("target")
                    tgtElm  = self.al.findElementByID(tid)[0]

                    self.addRelation(srcElm, tgtElm, x.get(ARCHI_TYPE)[10:])
            except:
                em = format_exc()
                logger.warn("Something is not present : %s" % (em))

        logger.info("Exported %d Elements" % n)
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
        parentPath = self.getParentPath(element)
        model = "%s/%s" % (parentPath, model)

        nmodel = "DM_%s" % self._cleanString(model)

        #
        # Iterate through DiagramObject's
        #
        for x in list(element):
            logger.debug("DO[%s] - %s[%s]" % (x.tag, x.get("id"), x.get("archimateElement")))

            if x.get(ARCHI_TYPE) != "archimate:Note":
                try:
                    self.textExport.append("%s,%s,%s,%s" % (nmodel, x.get("name"), x.get(ARCHI_TYPE)[10:], "ModelObject"))
                except:
                    em = format_exc()
                    logger.warn("Warning: %s" % (em))
                    continue

                self.addElement(x)
                self.addRelation(element, x, "ModelObject")

                xid = x.get("archimateElement")
                logger.debug("  xid : %s" % xid)

                try:
                    aeid = self.al.findElementByID(xid)[0]
                except:
                    em = format_exc()
                    logger.warn("aeid[0] not present : %s" % (em))
                    continue

                logger.debug("  AE - %s : %s[%s]" % (aeid.get("name"), aeid.tag, aeid.get(ARCHI_TYPE)))
                self.addElement(aeid)
                self.addRelation(x, aeid, "ArchimateElement")

                self.exportArchiDO(x, model)
            else:
                if x.get(ARCHI_TYPE) == "archimate:Note":
                    for k, v in x.attrib.items():
                        logger.debug("    K : %s \t V : %s" % (k, v))


    #
    # export Archimate DiagramObject to Neo4J
    #
    def exportArchiDO(self, x, model):
        #
        # Iterate through Children of DiagramObject
        #
        for y in list(x):
            #
            #  Find ArchimateElement for DiagramObject
            #
            self.addRelation(x, y, "DiagramObject")

            for z in list(y):
                try:
                    logger.debug("    z.tag : %s" % z.tag)

                    if z.tag == "documentation" and len(z.text) > 0:
                        x.attrib["documentation"] = z.text

                    if z.tag == "content" and len(z.text) > 0:
                        x.attrib["content"] = z.text.rtrim()

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

                        self.textExport.append("%s,%s,%s,%s" % (model, srcElm.get("name"), relElm.get(ARCHI_TYPE)[10:], tgtElm.get("name")))

                        self.addElement(srcElm)
                        self.addElement(tgtElm)
                        self.addElement(relElm)

                        self.addRelation(srcElm, tgtElm, rid)
                except:
                    em = format_exc()
                    logger.warn("Warning: %s" % (em))

    def _progress(self):
        if self.nSpaces < self.nMax:
            self.nSpaces += 1

        else:
            self.nSpaces = 0

        space = " " * self.nSpaces

        logger.info("%s. :)" % space)

    #
    # Add an Archimate Element to Neo4J
    #
    def addElement(self, x):

        #self.progress()

        if x.get(ARCHI_TYPE) in relations.values():
            logger.debug("Adding Relationship - %s" % x.get(ARCHI_TYPE))
        else:
            logger.debug("Adding %s[%s]" % (x.get("name"), x.get(ARCHI_TYPE)))

        x.attrib["parentPath"] = self.getParentPath(x)

        ps = ""
        if x.get(ARCHI_TYPE) != None:
            typeName = x.get(ARCHI_TYPE)[10:]
        else:
            typeName = x.tag

        if x.attrib == None:
            prop = dict()
        else:
            prop = x.attrib

        if x.text != None:
            prop["text"] = self._cleanString(x.text)

        if x.tag != None:
            prop["tag"] = x.tag

        #
        #  Iterate through DiagramObject Children
        #
        for y in list(x):

            logger.debug("y.tag : %s" % y.tag)
            if y.tag == "documentation":
                logger.debug("  documentation : %s" % y.tag)
                prop["documentation"] = self._cleanString(y.text)

            if y.tag == "content":
                logger.debug("content : %s" % y.tag)
                prop["content"] = self._cleanString(y.text)

            #
            #  <property key="Comments " value="Align to complete after the Contact and Lead Management project
            # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
            #
            elif y.tag == "property":
                try:
                    logger.debug("property : %s" % y.tag)
                    key = self._cleanString(y.get("key")).replace(" ", "_")
                    value = self._cleanString(y.get("value")).replace(" ", "_")
                    logger.debug("k[v] : %s[%s]" % (key, value))
                    prop[key] = value

                except:
                    em = format_exc()
                    logger.warn("Warning: %s" % (em))


        # updateTime = time.time()
        # strUpdateTime = time.asctime(time.localtime(updateTime))
        #
        # This would be nice, but you loose the ability to merge nodes
        # prop["LastUpdate"] = strUpdateTime

        #
        # Get the properties
        #
        for k, v in prop.items():

            if k == "id":
                logger.debug("k=%s\t V=%s" % (k, v))
                ps = ps + " a%s:\"%s\", " % (k, v)
                continue

            elif k == "name":
                kk = self._cleanString(k)
                logger.debug("k=%s\t V=%s" % (kk, v))
                ps = ps + " a%s:\"%s\", " % (kk, v)
                continue

            elif k <> ARCHI_TYPE:
                logger.debug("k=%s\t V=%s" % (k, v))
                ps = ps + " %s:\"%s\", " % (k, v)

        # remove the last comma
        ps = ps[:-2]

        logger.debug("properties : .%s." % ps)

        qs = "MERGE (n:%s {%s, typeName:\"%s\"}) return n" % (typeName, ps, typeName)
        logger.debug("    Node Query : '%s'" % qs)
        nodeReturn = self.cypherQuery(qs)

        return self.cypherQuery(qs)
    #
    # Add an Archimate Relations to Neo4J
    #
    def addRelation (self, parentElement, childElement, relation):

        logger.debug("Adding %s[%s] -> %s -> %s[%s]" % (parentElement.get("name"), parentElement.get(ARCHI_TYPE), relation,
                                                       childElement.get("name"), childElement.get(ARCHI_TYPE)))

        pid = parentElement.get("id")
        cid = childElement.get("id")

        qs = "MATCH (n { aid:'%s'}), (m { aid:'%s'}) MERGE (n)-[r:%s]->(m) RETURN r" % (pid, cid, relation.replace(" ", "_"))
        logger.debug("    Rel Query : '%s'" % qs)
        self.listRelations.append(qs)

    def createRelations(self):

        for x in self.listRelations:
            logger.debug("    REL Query %s" % x)
            query = self.cypherQuery(x)

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
        try:
            query = neo4j.CypherQuery(self.graph, qs)
            return query.execute().data
        except:
            em = format_exc()
            logger.warn("Warning: %s" % (em)) 
            return None

    #
    # Helper Functions
    #
    def getParentPath(self, element):
        ps = ""

        parent = element.getparent()

        while parent != None:
            ps = "/%s" % parent.get("name") + ps
            parent = parent.getparent()

        return ps

    def exportCSV(self):

        f = open(fileCSVExport,'w')

        m = 0
        for x in self.textExport:
            f.write("%s\n" % x)

        f.close()

    def _cleanString(self, s):

        if s == None:
            return ""

        s = s.replace(".", "_")
        s = s.replace("-", "_")
        s = s.replace("&", "and")
        s = s.replace("/", "_")
        s = s.replace("\"", "'")

        return s.lstrip(" ").rstrip(" ")

    def doDirectoryOfModels(self):

        if self.subdirArchimate == None:
            return

        errors = list()

        clearFlag = True

        numFilesParsed = 0
        for root, dirs, files in os.walk(self.subdirArchimate, topdown=True):
            logger.info("%s : %s : %s" % (root, dirs, files))

            for name in files:

                if name[-9:] == "archimate":
                    logger.debug("%s" % (name))

                    nameFile = os.path.join(root, name)

                    logger.info("Exporting : %s" % (nameFile))

                    if clearFlag == True:
                        eain = ExportArchimateIntoNeo4J(gdb, fileArchimate=nameFile, Reset=True)
                        clearFlag = False
                    else:
                        eain = ExportArchimateIntoNeo4J(gdb, fileArchimate=nameFile, Reset=False)

                    # Export just Archimate Elements
                    eain.exportArchiElements()

                    # Export Archimate Diagram Models
                    eain.exportArchiDMS()

                    # Create an export of all model relationships
                    #eain.exportCSV()


if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    #subdirArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/ExportIntoNeo4J"

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V6.archimate"

    logger.info("Exporting : %s" % (fileArchimate))

    eain = ExportArchimateIntoNeo4J(gdb, fileArchimate=fileArchimate, Reset=True)

    # Export just Archimate Elements
    eain.exportArchiElements()

    # Export Archimate Diagram Models
    eain.exportArchiDMS()

    # Create an export of all model relationships
    #eain.exportCSV()

    ArchiLib.stopTimer(start_time)