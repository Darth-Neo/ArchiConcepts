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
def fileArchimate():
    return fileArchimateTest

@pytest.fixture(scope="module")
def cleandir():
    cwd = os.getcwd()

    listFiles = list()
    listFiles.append(fileCSVExport)
    listFiles.append(fileImageExport)

    listFiles.append(fileConceptsEstimation)
    listFiles.append(fileConceptsExport)
    listFiles.append(fileConceptsRelations)
    listFiles.append(fileConceptsRequirements)
    listFiles.append(fileConceptsArch)
    listFiles.append(fileConceptsBatches)
    listFiles.append(fileConceptsChunks)
    listFiles.append(fileConceptsPPTX)

    listFiles.append(fileArchimateImport)

    for lf in listFiles:
        if os.path.exists(lf):
            logger.info("remove : %s" % lf)
            os.remove(lf)

def neo4jCounts(gdb):

    try:
        logger.info("Neo4J instance : %s" % gdb)
        nj = Neo4JLib(gdb)

        qs = "MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = nj.cypherQuery(qs)

        logger.info("Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info("%4d : %s" % (x[2], x[0]))

        return True

    except:
        return False

@pytest.mark.NeoJ
def test_importConceptsIntoNeo4J(fileArchimate, gdb):

    assert (os.path.isfile(fileArchimate)  == True)
    icnj = ConceptsImportNeo4J(fileArchimate, gdb, ClearNeo4J=True)

    assert (os.path.isfile(fileConceptsExport)  == True)
    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    icnj.importNeo4J(importConcepts)

#
# Counts
#
@pytest.mark.Archi
def test_ArchiCounts(cleandir, fileArchimate):
    assert (os.path.isfile(fileArchimate)  == True)

    al = ArchiLib(fileArchimateTest)

    lc = al.logTypeCounts()

    assert (len(lc) > 0)

#
# Export Archimate XML
#
@pytest.mark.Archi
def test_ExportArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()

    assert (os.path.isfile(fileConceptsExport)  == True)

@pytest.mark.Archi
def test_ExportArchiFolderModels(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    folder = "Scenarios"

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    eafm.exportArchiFolderModels(folder)

    assert (os.path.isfile(fileConceptsExport)  == True)

@pytest.mark.Archi
def test_ArchimateConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileConceptsArch, "Archimate")

    al = ArchiLib(fileArchimate)

    lc = al.logTypeCounts()

    assert (len(lc) > 0)

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)

    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info("Saved concepts to : %s" % fileConceptsArch)

    assert (os.path.isfile(fileConceptsArch)  == True)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchiModel, fileArchConcepts)

@pytest.mark.Archi
def test_CreateArchimateConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchimate, "Archimate")

    al = ArchiLib(fileArchimate)

    lc = al.logTypeCounts()

    assert (len(lc) > 0)

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info("Saved concepts to : %s" % fileConceptsArch)

    assert (os.path.isfile(fileConceptsArch)  == True)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchimateModel, fileConceptsArch)

@pytest.mark.Archi
def test_CreateArchiFromConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)
    assert (os.path.isfile(fileConceptsImport)  == True)

    logger.info("Using : %s" % fileArchimate)
    logger.info("Loading : %s" % fileConceptsImport)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsImport)

    concepts = Concepts.loadConcepts(fileConceptsImport)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML(fileArchimateImport)

    assert (os.path.isfile(fileArchimateImport)  == True)

#
# Create Relations
#
@pytest.mark.Archi
def test_CreateRelations(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    cr = CreateRelationsInArchi(fileArchimate)

    cr.createRelations(fileArchimateImport)

    assert (os.path.isfile(fileArchimateImport)  == True)

#
# Analysis
#
@pytest.mark.Archi
def test_DependancyAnalysisFromArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    assert (len(concepts.getConcepts())  > 0)
    assert (os.path.isfile(fileConceptsTraversal)  == True)
    assert (os.path.isfile(fileConceptsBatches)  == True)

@pytest.mark.Archi
def test_NamedEntityAnalysis(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    ane = AnalyzeNamedEntities(fileArchimate, fileConceptsRequirements)

    ane.analyzeNamedEntities()

    assert (os.path.isfile(fileConceptsRelations)  == True)

@pytest.mark.Archi
def test_RequirementAnalysis(cleandir, fileArchimate):

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

    assert (os.path.isfile(conceptsFile)  == True)

    chunks = Chunks(concepts)
    chunks.createChunks()

    assert (os.path.isfile(fileConceptsChunks)  == True)

#
# Similarity
#
@pytest.mark.Archi
def test_GapSimilarity(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    gapSimilarity(fileArchimate)

    assert (os.path.isfile(fileConceptsNGramFile)  == True)
    assert (os.path.isfile(fileConceptsNGramScoreFile)  == True)
    assert (os.path.isfile(fileConceptsNGramsSubject)  == True)

#
# PPTX
#
@pytest.mark.PPTX
def test_CreatePPTXFromArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate)  == True)

    cpfa = ArchiCreatePPTX(fileArchimate, filePPTXIn, filePPTXOut)

    cpfa.buildPPTX()

    assert (os.path.isfile(filePPTXOut)  == True)

@pytest.mark.PPTX
def test_PPTXCrawl(fileArchimate):

    assert (os.path.isfile(filePPTXIn)  == True)

    logger.info("Using : %s" % filePPTXIn)

    cpptx = PPTXCreateArchil(filePPTXIn, fileArchimate)

    c = cpptx.crawlPPTX()

    Concepts.saveConcepts(c, fileConceptsPPTX)

    assert (os.path.isfile(fileConceptsPPTX)  == True)

#
# Neo4j Tests
#
@pytest.mark.Neo4J
def test_Neo4jCounts(gdb):

    assert(neo4jCounts(gdb) == True)

@pytest.mark.Neo4J
def test_ExportNeo4j(cleandir, gdb):

    assert(neo4jCounts(gdb) == True)

    concepts = Concepts("Neo4J", "Neo4J Graph DB")

    nj = Neo4JLib(gdb)

    nj.exportNeo4JToConcepts(concepts, fileNodes=fileConceptsNodes)

    assert (os.path.isfile(fileConceptsNodes)  == True)


#
# Create Estimate
#
@pytest.mark.Neo4J
def test_CreateEstimate(cleandir, gdb):

    assert(neo4jCounts(gdb) == True)

    nj = Neo4JLib(gdb)

    qs = "MATCH "
    qs = qs +    "(n0:ApplicationFunction)-- (r0)"
    qs = qs + "-- (n1:ApplicationComponent)--(r1)"
    qs = qs + "-- (n2:ApplicationService)--  (r2)"
    qs = qs + "-- (n3:BusinessProcess)--     (r3)"
    qs = qs + "-- (n4:BusinessObject) "
    qs = qs + "Return n0, r0, n1, r1, n2, r2, n3, r3, n4, n4.PageRank, n4.RequirementCount, n4.Degree"

    lq, qd = nj.cypherQuery(qs)

    assert (os.path.isfile(fileExcelIn)  == True)

    nj.queryExportExcel(lq)

    assert (os.path.isfile(fileExcelOut)  == True)

    logger.info("%d rows returned" % len(lq))


#
# Graphics
#
@pytest.mark.Graphics
def test_GraphConcepts(cleandir):

    assert (os.path.isfile(fileConceptsNGramsSubject)  == True)

    c = Concepts("GraphConcepts", "GRAPH")
    concepts = Concepts.loadConcepts(fileConceptsNGramsSubject)

    # c.logConcepts()

    #graph = PatternGraph()
    graph = GraphVizGraph()

    cg = ConceptsGraph(graph=graph, fileImage=fileImageExport)

    cg.conceptsGraph(concepts)

    assert (os.path.isfile(fileImageExport)  == True)

#
# Analyze Graph
#
@pytest.mark.Neo4J
def test_AnalyzeGraph(cleandir, gdb):

    assert(neo4jCounts(gdb) == True)

    ag = AnalyzeGraph(gdb)

    assert (os.path.isfile(fileConceptsExport)  == True)

    ag.analyzeNetworkX(fileConceptsExport)


def test_QueryGraph(cleandir, gdb):
    queryGraph(gdb)

if __name__ == "__main__":
    pass

