#!/usr/bin/python
#
# Testing all modules
#
__author__ = u'morrj140'
__VERSION__ = u'0.2'

from nl_lib.Concepts import Concepts

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(logging.INFO)

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph

from al_Constants import *

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

import pytest


dirTest = u"test" + os.sep

fileArchimate      = dirTest + u"Testing.archimate"

conceptsExport     = dirTest  + u"export.p"
conceptsEstimation = dirTest  + u"estimation.p"
conceptsArchi      = dirTest  + u"archi.p"

exportCSV          = dirTest  + u"export.csv"
exportReportCSV    = dirTest  + u"report.csv"


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
            logger.info(u"remove : %s" % lf)
            os.remove(lf)


def neo4jCounts(gdb):

    if True:
        logger.info(u"Neo4J instance : %s" % gdb)
        nj = Neo4JLib(gdb)

        qs = u"MATCH (n) RETURN n.typeName, count(n.typeName) order by count(n.typeName) DESC"
        lq, qd = nj.cypherQuery(qs)

        logger.info(u"Neo4J Counts")
        for x in sorted(lq[1:], key=lambda c: int(c[2]), reverse=True):
            logger.info(u"%4d : %s" % (x[2], x[0]))

        return True

    else:
        return False

@pytest.mark.NeoJ
def test_importConceptsIntoNeo4J(fileArchimate, gdb):

    assert (os.path.isfile(fileArchimate) is True)
    icnj = ConceptsImportNeo4J(fileArchimate, gdb, ClearNeo4J=True)

    assert (os.path.isfile(fileConceptsExport) is True)
    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    icnj.importNeo4J(importConcepts)

#
# Counts
#
@pytest.mark.Archimate
def test_ArchiCounts(cleandir, fileArchimate):
    assert (os.path.isfile(fileArchimate) is True)

    al = ArchiLib(fileArchimateTest)

    lc = al.logTypeCounts()

    assert (len(lc) > 0)

#
# Export Archimate XML
#

@pytest.mark.Archimate
def test_ExportArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()

    assert (os.path.isfile(fileConceptsExport) is True)

@pytest.mark.Archimate
def test_ExportArchiFolderModels(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    folder = "Scenarios"

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    eafm.exportArchiFolderModels(folder)

    assert (os.path.isfile(fileConceptsExport) is True)

@pytest.mark.Archimate
def test_ArchimateConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

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

    assert (os.path.isfile(fileConceptsArch) is True)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchiModel, fileArchConcepts)

@pytest.mark.Archimate
def test_CreateArchimateConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    logger.info(u"Using : %s" % fileArchimate)

    concepts = Concepts(fileArchimate, u"Archimate")

    al = ArchiLib(fileArchimate)

    lc = al.logTypeCounts()

    assert (len(lc) > 0)

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info(u"Saved concepts to : %s" % fileConceptsArch)

    assert (os.path.isfile(fileConceptsArch) is True)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchimateModel, fileConceptsArch)

@pytest.mark.Archimate
def test_CreateArchiFromConcepts(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)
    assert (os.path.isfile(fileConceptsImport) is True)

    logger.info(u"Using : %s" % fileArchimate)
    logger.info(u"Loading : %s" % fileConceptsImport)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsImport)

    concepts = Concepts.loadConcepts(fileConceptsImport)

    # Create Subfolder
    folder = u"Implementation & Migration"
    subfolder = u"Dependancy Analysis - %s" % time.strftime(u"%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML(fileArchimateImport)

    assert (os.path.isfile(fileArchimateImport) is True)

#
# Create Relations
#
@pytest.mark.Archimate
def test_CreateRelations(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    cr = CreateRelationsInArchi(fileArchimate)

    cr.createRelations(fileArchimateImport)

    assert (os.path.isfile(fileArchimateImport) is True)

#
# Analysis
#
@pytest.mark.Archimate
def test_DependancyAnalysisFromArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    assert (len(concepts.getConcepts()) > 0)
    assert (os.path.isfile(fileConceptsTraversal) is True)
    assert (os.path.isfile(fileConceptsBatches) is True)

@pytest.mark.Archimate
def test_NamedEntityAnalysis(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    ane = AnalyzeNamedEntities(fileArchimate, fileConceptsRequirements)

    ane.analyzeNamedEntities()

    assert (os.path.isfile(fileConceptsRelations) is True)

@pytest.mark.Archimate
def test_RequirementAnalysis(cleandir, fileArchimate):

    assert (os.path.isfile(filePPTXIn) is True)

    al = ArchiLib(fileArchimate)

    conceptsFile = fileConceptsRequirements

    searchTypes = list()
    searchTypes.append(u"archimate:Requirement")
    nl = al.getTypeNodes(searchTypes)

    logger.info(u"Find Words in Requirements...")
    concepts = Concepts(u"Requirement", u"Requirements")
    n = 0
    for sentence in nl:
        n += 1
        logger.debug(u"%s" % sentence)

        c = concepts.addConceptKeyType(u"Document" + unicode(n), u"Document")
        d = c.addConceptKeyType(sentence, u"Sentence" + unicode(n))

        if True and sentence is not None:
            cleanSentence = ' '.join([word for word in sentence.split(" ") if word not in stop])
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
                if len(word) > 1 and pos[0] == u"N":
                    e = d.addConceptKeyType(word, u"Word")
                    f = e.addConceptKeyType(pos, u"POS")

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info(u"Saved : %s" % conceptsFile)

    assert (os.path.isfile(conceptsFile) is True)

    chunks = Chunks(concepts)
    chunks.createChunks()

    assert (os.path.isfile(fileConceptsChunks) is True)

#
# Similarity
#
@pytest.mark.Archimate
def test_GapSimilarity(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    gapSimilarity(fileArchimate)

    assert (os.path.isfile(fileConceptsNGramFile) is True)
    assert (os.path.isfile(fileConceptsNGramScoreFile) is True)
    assert (os.path.isfile(fileConceptsNGramsSubject) is True)

#
# PPTX
#
@pytest.mark.PPTX
def test_CreatePPTXFromArchi(cleandir, fileArchimate):

    assert (os.path.isfile(fileArchimate) is True)

    cpfa = ArchiCreatePPTX(fileArchimate, filePPTXIn, filePPTXOut)

    cpfa.buildPPTX()

    assert (os.path.isfile(filePPTXOut) is True)

@pytest.mark.PPTX
def test_PPTXCrawl(fileArchimate):

    assert (os.path.isfile(filePPTXIn) is True)

    logger.info(u"Using : %s" % filePPTXIn)

    cpptx = PPTXCreateArchil(filePPTXIn, fileArchimate)

    c = cpptx.crawlPPTX()

    Concepts.saveConcepts(c, fileConceptsPPTX)

    assert (os.path.isfile(fileConceptsPPTX) is True)

#
# Neo4j Tests
#
@pytest.mark.Neo4J
def test_Neo4jCounts(gdb):
    nj = Neo4JLib(gdb)
    sl = nj.neo4jCounts()
    assert(sl is not None)

@pytest.mark.Neo4J
def test_ExportNeo4j(cleandir, gdb):

    nj = Neo4JLib(gdb)

    assert(nj.neo4jCounts() is not None)

    concepts = Concepts(u"Neo4J", u"Neo4J Graph DB")

    nj.exportNeo4JToConcepts(concepts, fileNodes=fileConceptsNodes)

    assert (os.path.isfile(fileConceptsNodes) is True)


#
# Create Estimate
#
@pytest.mark.Neo4J
def test_CreateEstimate(cleandir, gdb):

    nj = Neo4JLib(gdb)

    assert(nj.neo4jCounts() is not None)

    qs = u"MATCH (n0:ApplicationFunction)-- (r0)"
    qs = u"%s -- (n1:ApplicationComponent)--(r1)" % qs
    qs = u"%s -- (n2:ApplicationService)--  (r2)" % qs
    qs = u"%s -- (n3:BusinessProcess)--     (r3)" % qs
    qs = u"%s -- (n4:BusinessObject) " % qs
    qs = u"%s Return n0, r0, n1, r1, n2, r2, n3, r3, n4, n4.PageRank, n4.RequirementCount, n4.Degree" % qs

    lq, qd = nj.cypherQuery(qs)

    assert (lq is not None)
    assert (qd is not None)

    assert (os.path.isfile(fileExcelIn) is True)

    nj.queryExportExcel(lq, fileIn=fileExcelIn, fileOut=fileExcelOut)

    assert (os.path.isfile(fileExcelOut) is True)

    logger.info(u"%d rows returned" % len(lq))


#
# Graphics
#
@pytest.mark.Graphics
def test_GraphConcepts(cleandir):

    assert (os.path.isfile(fileConceptsNGramsSubject) is True)

    c = Concepts(u"GraphConcepts", u"GRAPH")
    concepts = Concepts.loadConcepts(fileConceptsNGramsSubject)

    # c.logConcepts()

    # graph = PatternGraph()
    graph = GraphVizGraph()

    cg = ConceptsGraph(graph=graph, fileImage=fileImageExport)

    cg.conceptsGraph(concepts)

    assert (os.path.isfile(fileImageExport) is True)

#
# Analyze Graph
#
@pytest.mark.Neo4J
def test_AnalyzeGraph(cleandir, gdb):

    nj = Neo4JLib(gdb)

    assert(nj.neo4jCounts() is not None)

    ag = AnalyzeGraph(gdb)

    assert (os.path.isfile(fileConceptsExport) is True)

    ag.analyzeNetworkX(None, fileConceptsExport)

def test_QueryGraph(cleandir, gdb):
    queryGraph(gdb)

if __name__ == u"__main__":
    pass

