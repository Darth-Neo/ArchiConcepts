#!/usr/bin/env python
#
# Export Archimate into Neo4J
#
# __author__ = u'morrj140'
# __VERSION__ = u'0.3'
import os
import sys
import time
from subprocess import call

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.ArchiLib import ArchiLib
from al_lib.Neo4JLib import Neo4JLib
from al_lib.Constants import *

from al_Constants import *

from py2neo import neo4j, node, rel


class ExportArchimateIntoNeo4J (object):
    listModels = None
    listRelations = None
    fileArchimate = None
    gdb = None
    textExport = None
    errorNodes = None

    nMin = 0
    nMax = 76
    nSpaces = 0

    def __init__(self, gdb, fileArchimate=None, subdirArchimate=None, Reset=True):

        self.listRelations = list()
        self.listModels = list()
        self.textExport = list()
        self.errorNodes = list()

        self.gdb = gdb

        logger.info(u"Neo4J instance : %s" % self.gdb)
        self.graph = neo4j.GraphDatabaseService(self.gdb)

        if fileArchimate is not None:
            self.fileArchimate = fileArchimate

            logger.info(u"Using : %s" % fileArchimate)
            self.fileArchimate = fileArchimate
            self.al = ArchiLib(fileArchimate)

            if Reset:
                self.clearNeo4J()

            self.listDiagramModels()

        elif subdirArchimate is not None:
            self.fileArchimate = None
            self.subdirArchimate = subdirArchimate

        else:
            raise Exception

    #
    # Get all DiagramModels from Archimate XML
    #
    def listDiagramModels(self, folder=u"Views"):

        dm = self.al.getElementsFromFolder(folder)

        for x in dm.iter():
            if ARCHI_TYPE in x.attrib and x.attrib[ARCHI_TYPE] == DIAGRAM_MODEL:
                logger.debug(u"Exporting model : %s" % (x.get(u"name")))
                self.listModels.append(x)

        logger.info(u"Found %d Models" % len(self.listModels))

    def exportArchiElements(self):

        logger.info(u"Export Archimate Elements")

        n = 0

        for x in self.al.tree.getroot().iter():
            try:
                n += 1
                if ARCHI_TYPE in x.attrib and x.attrib[ARCHI_TYPE] in entities.values():
                    logger.debug(u"EL : %s[%s]" % (x.get(u"name"), x.get(ARCHI_TYPE)))
                    parentPath = self.getParentPath(x)
                    x.attrib[u"parentPath"] = parentPath
                    self.addElement(x)

                elif ARCHI_TYPE in x.attrib and x.attrib[ARCHI_TYPE] in relations.values():
                    logger.debug(u"EL : %s[%s]" % (x.get(u"name"), x.get(ARCHI_TYPE)))
                    parentPath = self.getParentPath(x)
                    x.attrib[u"parentPath"] = parentPath
                    self.addElement(x)

                    sid = x.get(u"source")
                    srcElm = self.al.findElementByID(sid)[0]

                    tid = x.get(u"target")
                    tgtElm = self.al.findElementByID(tid)[0]

                    self.addRelation(srcElm, tgtElm, x.get(ARCHI_TYPE)[10:])
            except Exception, msg:
                logger.warn(u"Something is not present : %s" % (msg))
                return

        logger.info(u"Exported %d Elements" % n)
    #
    # Iterate through all DiagramModels
    #

    def exportArchiDMS(self):

        for x in self.listModels:
            model = x.get(u"name")

            logger.info(u"Model - %s" % model)

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

        if element is None:
            return

        logger.info(u"Model : %s[%s]" % (model, element.get(u"id")))
        self.addElement(element)
        parentPath = self.getParentPath(element)
        model = u"%s/%s" % (parentPath, model)

        nmodel = u"DM_%s" % self._cleanString(model)

        #
        # Iterate through DiagramObject's
        #
        for x in list(element):
            logger.info(u"DO[%s] - %s[%s]" % (x.tag, x.get(u"id"), x.get(u"archimateElement")))

            if x.get(ARCHI_TYPE) != u"archimate:Note":
                try:
                    self.textExport.append(u"%s,%s,%s,%s" % (nmodel, x.get(u"name"), x.get(ARCHI_TYPE)[10:], u"ModelObject"))
                except Exception, msg:
                    logger.warn(u"Something is not present : %s" % (msg))
                    continue

                self.addElement(x)
                self.addRelation(element, x, u"ModelObject")

                xid = x.get(u"archimateElement")
                logger.debug(u"  xid : %s" % xid)

                try:
                    aeid = self.al.findElementByID(xid)[0]
                except Exception, msg:
                    logger.warn(u"Something is not present : %s" % (msg))
                    continue

                logger.debug(u"  AE - %s : %s[%s]" % (aeid.get(u"name"), aeid.tag, aeid.get(ARCHI_TYPE)))
                self.addElement(aeid)
                self.addRelation(x, aeid, u"ArchimateElement")

                self.exportArchiDO(x, model)
            else:
                if x.get(ARCHI_TYPE) == u"archimate:Note":
                    for k, v in x.attrib.items():
                        logger.debug(u"    K : %s \t V : %s" % (k, v))

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
            self.addRelation(x, y, u"DiagramObject")

            for z in list(y):
                try:
                    logger.debug(u"    z.tag : %s" % z.tag)

                    if z.tag == u"documentation" and len(z.text) > 0:
                        x.attrib[u"documentation"] = z.text

                    if z.tag == u"content" and len(z.text) > 0:
                        x.attrib[u"content"] = z.text.rtrim()

                    elif z.tag == u"property":
                        key = z.get(u"key")
                        value = z.get(u"value")
                        x.attrib[key] = value

                    elif z.tag == u"bounds":
                        attrib = z.attrib
                        zX = attrib[u"x"]
                        zY = attrib[u"y"]
                        zH = attrib[u"height"]
                        zW = attrib[u"width"]

                        logger.debug(u"    B - %s : %s : %s : %s" % (zX, zY, zH, zW))

                        x.attrib[u"x"] = zX
                        x.attrib[u"y"] = zY
                        x.attrib[u"height"] = zH
                        x.attrib[u"width"] = zW

                    elif z.tag == u"sourceConnection":
                        src = z.get(u"source")
                        srcDO = self.al.findDiagramObject(src)[0].attrib
                        sid = srcDO[u"archimateElement"]
                        srcElm = self.al.findElementByID(sid)[0]

                        trc = z.get(u"target")
                        tgtDO = self.al.findDiagramObject(trc)[0].attrib
                        tid = tgtDO[u"archimateElement"]
                        tgtElm = self.al.findElementByID(tid)[0]

                        rrc = z.get(u"relationship")
                        relElm = self.al.findElementByID(rrc)[0]

                        rid = relElm.get(ARCHI_TYPE)[10:]
                        logger.info(u"  S - %s -> [%s] -> %s" % ((srcElm.get(u"name"), relElm.get(ARCHI_TYPE)[10:], tgtElm.get(u"name"))))

                        self.textExport.append(u"%s,%s,%s,%s" % (model, srcElm.get(u"name"), relElm.get(ARCHI_TYPE)[10:], tgtElm.get(u"name")))

                        self.addElement(srcElm)
                        self.addElement(tgtElm)
                        self.addElement(relElm)

                        self.addRelation(srcElm, tgtElm, rid)
                except Exception, msg:
                    logger.warn(u"Something is not present : %s" % (msg))


    def _progress(self):
        if self.nSpaces < self.nMax:
            self.nSpaces += 1

        else:
            self.nSpaces = 0

        space = u" " * self.nSpaces

        logger.info(u"%s. :)" % space)

    #
    # Add an Archimate Element to Neo4J
    #
    def addElement(self, x):

        # self.progress()

        prop = dict()

        try:
            if x.get(ARCHI_TYPE) in relations.values():
                logger.debug(u"Adding Relationship - %s" % x.get(ARCHI_TYPE))
            else:
                logger.debug(u"Adding %s[%s]" % (x.get(u"name"), x.get(ARCHI_TYPE)))

        except Exception, msg:
            logger.warn(u"Opps... : %s" % (msg))
            return None

        x.attrib[u"parentPath"] = self.getParentPath(x)

        ps = ""
        if x.get(ARCHI_TYPE) is not None:
            typeName = x.get(ARCHI_TYPE)[10:]
        else:
            typeName = x.tag

        if x.attrib is not None:
            prop = x.attrib

        if x is not None and x.text is not None:
            prop[u"text"] = self._cleanString(x.text)

        if x is not None and x.tag is not None:
            prop[u"tag"] = x.tag

        #
        #  Iterate through DiagramObject Children
        #
        for y in list(x):

            logger.debug(u"y.tag : %s" % y.tag)
            if y.tag == u"documentation":
                logger.debug(u"  documentation : %s" % y.tag)
                prop[u"documentation"] = self._cleanString(y.text)

            if y.tag == u"content":
                logger.debug(u"content : %s" % y.tag)
                prop[u"content"] = self._cleanString(y.text)

            #
            #  <property key="Comments " value="Align to complete after the Contact and Lead Management project
            # is complete. Implementation will likely be 3rd or 4th quarter 2016."/>
            #
            elif y.tag == u"property":
                try:
                    logger.debug(u"property : %s" % y.tag)
                    key = self._cleanString(y.get(u"key")).replace(" ", "_")
                    value = self._cleanString(y.get(u"value")).replace(" ", "_")
                    logger.debug(u"k[v] : %s[%s]" % (key, value))
                    prop[key] = value

                except Exception, msg:
                    logger.warn(u"Something is not present : %s" % (msg))


        # updateTime = time.time()
        # strUpdateTime = time.asctime(time.localtime(updateTime))
        #
        # This would be nice, but you loose the ability to merge nodes
        # prop["LastUpdate"] = strUpdateTime

        #
        # Get the properties
        #
        for k, v in prop.items():

            if k is None or v is None:
                continue

            if k == u"id":
                logger.debug(u"k=%s\t V=%s" % (k, v))
                ps += u" a%s:\"%s\", " % (k, v)

            elif k == u"name":
                kk = self._cleanString(k)
                if len(kk) > 0 and len(v) > 0:
                    logger.debug(u"k=%s\t V=%s" % (kk, v))
                    ps += u" a%s:\"%s\", " % (kk, v)

            elif k == u"aname":
                kk = self._cleanString(k)
                if len(kk) > 0 and len(v) > 0:
                    logger.debug(u"k=%s\t V=%s" % (kk, v))
                    ps += u" a%s:\"%s\", " % (kk, v)

            elif k is not None and k <> ARCHI_TYPE:
                kk = self._cleanString(k)
                if len(kk) > 0 and len(v) > 0:
                    logger.debug(u"k=%s\t V=%s" % (k, v))
                    ps += u" %s:\"%s\", " % (k, v)

        # remove the last comma
        ps = ps[:-2]

        logger.debug(u"properties : .%s." % ps)

        qs = u"MERGE (n:%s {%s, typeName:\"%s\"}) return n" % (typeName, ps, typeName)
        logger.debug(u"    Node Query : '%s'" % qs)

        return self.cypherQuery(qs)
    #
    # Add an Archimate Relations to Neo4J
    #

    def addRelation(self, parentElement, childElement, relation):

        logger.debug(u"Adding %s[%s] -> %s -> %s[%s]" % (parentElement.get(u"name"),
                                                         parentElement.get(ARCHI_TYPE),
                                                         relation,
                                                         childElement.get(u"name"),
                                                         childElement.get(ARCHI_TYPE)))

        pid = parentElement.get(u"id")
        cid = childElement.get(u"id")

        qs = u"MATCH (n { aid:'%s'}), (m { aid:'%s'}) MERGE (n)-[r:%s]->(m) RETURN r" % \
             (pid, cid, relation.replace(u" ", u"_"))

        logger.debug(u"    Rel Query : '%s'" % qs)

        self.listRelations.append(qs)

    def createRelations(self):

        for x in self.listRelations:
            logger.debug(u"    REL Query %s" % x)
            self.cypherQuery(x)

    #
    # Start New Graph DB
    #
    def clearNeo4J(self):

        logger.info(u"Reset Neo4J Graph DB")
        call([resetNeo4J])

    #
    # Entity Counts
    #
    def neo4jCounts(self):

        logger.info(u"Neo4J instance : %s" % self.gdb)

        qs = u"MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = self.cypherQuery(qs)

        logger.info(u"Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info(u"%4d : %s" % (x[2], x[0]))

    #
    # Neo4J Indexs and Queries
    #
    def createAllIndexes(self):
        for t in entities:
            self.createIndices(t)

    def createIndices(self, typeName):
        try:
            qs = u"CREATE INDEX ON :%s (aid)" % (typeName)
            logger.debug(u"Index :" + qs)

            self.cypherQuery(qs)
        except Exception, msg:
            logger.warn(u"Warning: %s" % (msg))

    def dropAllIndexes(self):
        for t in entities:
            self.dropIndices(t)

    def dropIndices(self, typeName):
        try:
            qs = u"DROP INDEX ON :%s (name)" % (typeName)
            logger.debug(u"Index :" + qs)
            self.cypherQuery(qs)

        except Exception, msg:
            logger.warn(u"Warning: %s" % (msg))

    def cypherQuery(self, qs):
        try:
            query = neo4j.CypherQuery(self.graph, qs)
            return query.execute().data
        except Exception, msg:
            logger.warn(u"Warning: %s" % (msg))
            return None

    #
    # Helper Functions
    #
    def getParentPath(self, element):
        ps = u""

        try:
            parent = element.getparent()

            while parent is not None:
                ps = u"/%s" % parent.get(u"name") + ps
                parent = parent.getparent()

            return ps

        except Exception, msg:
            logger.warn(u"Warning: %s" % (msg))
            return None

    def exportCSV(self):

        f = open(fileCSVExport, 'w')

        m = 0
        for x in self.textExport:
            f.write("%s%s" % (x, os.linesep))

        f.close()

    def _cleanString(self, s):

        if s is None:
            return u"None"

        s = s.replace(os.linesep, u" ")
        s = s.replace(u".", u"_")
        s = s.replace(u"-", u"_")
        s = s.replace(u"&", u"and")
        s = s.replace(u"/", u"_")
        s = s.replace(u"\"", u"'")

        return s

    def doDirectoryOfModels(self):

        if self.subdirArchimate is None:
            raise Exception

        errors = list()

        clearFlag = False

        numFilesParsed = 0
        for root, dirs, files in os.walk(self.subdirArchimate, topdown=True):
            logger.info(u"%s : %s : %s" % (root, dirs, files))

            for name in files:

                if name[-9:] == u"archimate":
                    logger.debug(u"%s" % (name))

                    nameFile = os.path.join(root, name)

                    logger.info(u"Exporting : %s" % (nameFile))

                    global fileArchimate

                    fileArchimate=nameFile

                    self.al = ArchiLib(fileArchimate)

                    # if clearFlag == True:
                    #    eain = ExportArchimateIntoNeo4J(self.gdb, fileArchimate=nameFile, Reset=True)
                    #    clearFlag = False
                    # else:
                    #    eain = ExportArchimateIntoNeo4J(self.gdb, fileArchimate=nameFile, Reset=False)

                    # Export just Archimate Elements
                    self.exportArchiElements()

                    # Export Archimate Diagram Models
                    self.exportArchiDMS()

                    # Create an export of all model relationships
                    # eain.exportCSV()


if __name__ == u"__main__":

    start_time = ArchiLib.startTimer()

    File_Only = True
    Neo4j_Reset = False

    if File_Only:

        LocalGBD  = u"http://localhost:7474/db/data/"

        fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/Kronos_v14.archimate"
        assert (os.path.isfile(fileConceptsArch) is True)
        
        # fileArchimate = os.getcwd() + os.sep + u"import_artifacts.archimate"

        logger.info(u"Exporting : %s" % (fileArchimate))

        eain = ExportArchimateIntoNeo4J(LocalGBD, fileArchimate=fileArchimate, Reset=Neo4j_Reset)

        # Export just Archimate Elements
        eain.exportArchiElements()

        # Export Archimate Diagram Models
        # Export Archimate Diagram Models
        eain.exportArchiDMS()

        # Create an export of all model relationships
        # eain.exportCSV()
    else:
        global gdb

        # gdb = u"http://localhost:7574/db/data/"
        gdb  = u"http://localhost:7474/db/data/"
        subdirArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/Library"

        eain = ExportArchimateIntoNeo4J(gdb, fileArchimate=None, subdirArchimate=subdirArchimate, Reset=False)

        eain.doDirectoryOfModels()

    ArchiLib.stopTimer(start_time)