#!/usr/bin/python
#
# Archimate Libray Constants
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import time

#
# IP of Neo4J Graph
#
LocalGBD  = "http://localhost:7474/db/data/"
RemoteGDB = "http://10.92.82.60:7574/db/data/"
gdb = LocalGBD

fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v27.archimate"

fileImportPPTX       = 'import_pp.archimate'
filePPTXArchimate    = "pp_models.archimate"
fileArchiModel       = 'archi.archimate'
fileImportConcepts   = "import_concepts.archimate"

#
# Test Archimate File
#
fileArchimateTest = os.getcwd() + "./test/Testing.archimate"

#
# Concept Files Used
#
fileArchConcepts           = "archi.p"
filePPTXConcepts           = "pptx.p"
fileConceptsExport         = "export.p"
fileTimeConceptsExport     = "export" + time.strftime("%Y%d%m_%H%M%S") +".p"
fileConceptsBatches        = "batches.p"
fileConceptsTraversal      = "traversal.p"
fileEstimationConcepts     = "Estimation.p"
fileRequirementsConcepts   = "req.p"
fileRelationsConcepts      = "rel.p"
fileConceptsDocuments      = "documents.p"
fileConceptsChunks         = "chunks.p"
fileNeo4JNodes             = "nodes.p"

#
# PowerPoint Filename
#
filePPTX = 'test.pptx'
fileTPPTX = 'tested.pptx'

#
# Script to reset Neo4J
#
resetNeo4J = "/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"
