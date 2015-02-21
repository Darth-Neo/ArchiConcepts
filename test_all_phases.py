#!/usr/bin/python
#
# Testing all modules
#
__author__ = 'morrj140'
__VERSION__ = '0.2'

from nl_lib.Concepts import Concepts

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(logging.INFO)

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportArchi import ExportArchi
from al_ArchiLib.ConceptsImportNeo4J import ConceptsImportNeo4J
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph
from al_ArchiLib.Neo4JLib import Neo4JLib
from al_ArchiLib.ConceptsImportArchi import ConceptsImportArchi
from al_ArchiLib.ArchiCreatePPTX import ArchiCreatePPTX
from al_ArchiLib.CreateRelationsInArchi import CreateRelationsInArchi
from al_ArchiLib.DependencyAnalysis import DependancyAnalysis
from al_ArchiLib.ExportFolderModels import ExportArchiFolderModels
from al_ArchiLib.ConceptsGraph import ConceptsGraph
from al_ArchiLib.AnalyzeNamedEntities import AnalyzeNamedEntities
from al_ArchiLib.PPTXCreateArchi import PPTXCreateArchil
from al_RequirementAnalysis import Chunks
from al_GapSimilarity import gapSimilarity
from al_QueryGraph import queryGraph

from al_Constants import *

import pytest

@pytest.fixture(scope="module")
def gdb():
    return gdbTest

@pytest.fixture(scope="module")
def graph():
    return Neo4JLib(gdbTest)

@pytest.fixture(scope="module")
def fileArchimate():
    return fileArchimateTest

def test_AnalyzeGraph(gdb):
    start_time = ArchiLib.startTimer()

    ag = AnalyzeGraph(gdb)

    ag.analyzeNetworkX(fileConceptsExport)

    ArchiLib.stopTimer(start_time)

def test_ArchiCounts(fileArchimate):
    al = ArchiLib(fileArchimateTest)

    al.logTypeCounts()

def test_CreateArchiFromConcepts(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    logger.info("Using : %s" % fileArchimate)
    logger.info("Loading :" + fileConceptsImport)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsImport)

    concepts = Concepts.loadConcepts(fileConceptsImport)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML()


def test_ArchimateConcepts(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileConceptsArch, "Archimate")

    al = ArchiLib(fileArchimateTest)

    al.logTypeCounts()

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info("Saved concepts to : %s" % fileConceptsArch)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchiModel, fileArchConcepts)


def test_CreateEstimate(gdb):
    nj = Neo4JLib(gdb)

    qs = "MATCH "
    qs = qs +    "(n0:ApplicationFunction)-- (r0)"
    qs = qs + "-- (n1:ApplicationComponent)--(r1)"
    qs = qs + "-- (n2:ApplicationService)--  (r2)"
    qs = qs + "-- (n3:BusinessProcess)--     (r3)"
    qs = qs + "-- (n4:BusinessObject) "
    qs = qs + "Return n0, r0, n1, r1, n2, r2, n3, r3, n4, n4.PageRank, n4.RequirementCount, n4.Degree"

    lq, qd = nj.cypherQuery(qs)

    nj.queryExportExcel(lq)

    logger.info("%d rows returned" % len(lq))

def test_CreatePPTXFromArchi(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    cpfa = ArchiCreatePPTX(fileArchimate, filePPTXIn, filePPTXOut)

    cpfa.buildPPTX()


def test_CreateRelations(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    cr = CreateRelationsInArchi(fileArchimate)

    cr.createRelations()

def test_CreateArchimateConcepts(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchimate, "Archimate")

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info("Saved concepts to : %s" % fileConceptsArch)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchimateModel, fileConceptsArch)


def test_DependancyAnalysisFromArchi(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

def test_ExportArchi(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()


def test_ExportArchiFolderModels(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    folder = "Scenarios"

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    eafm.exportArchiFolderModels(folder)

def ttest_ExportNeo4j(gdb):

    concepts = Concepts("Neo4J", "Neo4J Graph DB")

    nj = Neo4JLib(gdb)

    nj.exportNeo4JToConcepts(concepts)

def test_GraphConcepts():

    c = Concepts("GraphConcepts", "GRAPH")
    concepts = Concepts.loadConcepts(fileConceptsNGramsSubject)

    # c.logConcepts()

    #graph = PatternGraph()
    graph = GraphVizGraph()

    cg = ConceptsGraph(graph=graph, fileImage=fileImageExport)

    cg.conceptsGraph(concepts)


def test_NamedEntityAnalysis(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    ane = AnalyzeNamedEntities(fileArchimate, fileConceptsRequirements)

    ane.analyzeNamedEntities()


def test_Neo4jCounts(gdb):

    logger.info("Neo4J instance : %s" % gdb)
    nj = Neo4JLib(gdb)

    qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
    lq, qd = nj.cypherQuery(qs)

    logger.info("Neo4J Counts")
    for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
        logger.info("%4d : %s" % (x[2], x[0]))

def test_PPTXCrawl(fileArchimate):

    assert (os.path.isfile(filePPTXIn)  == True)

    logger.info("Using : %s" % filePPTXIn)

    cpptx = PPTXCreateArchil(filePPTXIn, fileArchimateModel)

    c = cpptx.crawlPPTX()

    c.logConcepts()

    Concepts.saveConcepts(c, fileConceptsPPTX)

def test_RequirementAnalysis(fileArchimate):

    assert (os.path.isfile(filePPTXIn)  == True)

    al = ArchiLib(fileArchimate)

    conceptsFile = fileConceptsRequirements

    searchTypes = list()
    searchTypes.append("archimate:Requirement")
    nl = al.getTypeNodes(searchTypes)

    logger.info("Find Words in Requirements...")
    concepts = Concepts("Requirement", "Requirements")
    n = 0
    for sentence in nl:
        n += 1
        logger.debug("%s" % sentence)

        c = concepts.addConceptKeyType("Document" + str(n), "Document")
        d = c.addConceptKeyType(sentence, "Sentence" + str(n))

        if True and sentence != None:
            cleanSentence = ' '.join([word for word in sentence.split(" ") if word not in stop])
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                if len(word) > 1 and pos[0] == "N":
                    e = d.addConceptKeyType(word, "Word")
                    f = e.addConceptKeyType(pos, "POS")

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Saved : %s" % conceptsFile)

    chunks = Chunks(concepts)
    chunks.createChunks()

def test_GapSimilarity(fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    gapSimilarity(fileArchimate)

def test_QueryGraph(gdb):
    queryGraph(gdb)

if __name__ == "__main__":
    pass

