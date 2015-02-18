#!/usr/bin/python
#
# Archimate Libray Constants
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import time
#
# Archimate XML
#
NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]
ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

#
# IP of Neo4J Graph
#
LocalGBD  = "http://localhost:7474/db/data/"
RemoteGDB = "http://10.92.82.60:7574/db/data/"
gdb = LocalGBD

#
# file of Archimate XML
#
fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v24.archimate"
CleanNeo4j = False

#fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v34.archimate"
#CleanNeo4j = False

fileImportPPTX       = 'import_pp.archimate'
filePPTXArchimate    = "pp_models.archimate"
fileArchiModel       = 'archi.archimate'
fileImportConcepts   ="import_concepts.archimate"

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
filePPTXIn = 'test.pptx'
filePPTXOut = 'test_out.pptx'
filePPTXCrawl = "test" + os.sep + "test_example.pptx"

#
# Estimate Template
#
fileExcelIn = 'Template_Estimate.xlsx'
#fileExcelOut = 'Template_Estimate_%s_new.xlsx' % time.strftime("%Y%d%m_%H%M%S")
fileExcelOut = 'Template_Estimate_new.xlsx'

csvFileExport ="export.csv"
csvTimeFileExport ="export" + time.strftime("%Y%d%m_%H%M%S") +".csv"

csvQueryExport      = "ExportQuery.csv"
csvTimeQueryExport  = "ExportQuery" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileExportImage      = "export.png"
fileTimeExportImage  = "export" + time.strftime("%Y%d%m_%H%M%S") +".png"

#fileReportExport="report" + time.strftime("%Y%d%m_%H%M%S") +".csv"
fileReportExport="report.csv"


#
# Script to reset Neo4J
#
resetNeo4J = "/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"

#
# Archimate Edges
#
relations = {"TriggeringRelationship" : "archimate:TriggeringRelationship",
                    "UsedByRelationship" : "archimate:UsedByRelationship",
                    "AccessRelationship" : "archimate:AccessRelationship",
                    "FlowRelationship" : "archimate:FlowRelationship",
                    "AssignmentRelationship" : "archimate:AssignmentRelationship",
                    "AssociationRelationship" : "archimate:AssociationRelationship",
                    "RealisationRelationship" : "archimate:RealisationRelationship",
                    "CompositionRelationship" : "archimate:CompositionRelationship"}

#
# Archimate Nodes
#
entities = {"BusinessEvent" : "archimate:BusinessEvent",
            "BusinessObject" : "archimate:BusinessObject",
            "BusinessProcess" : "archimate:BusinessProcess",
            "ApplicationService" : "archimate:ApplicationService",
            "ApplicationComponent" : "archimate:ApplicationComponent",
            "DataObject" : "archimate:DataObject",
            "Requirement" : "archimate:Requirement",
            "Stakeholder" : "archimate:Stakeholder",
            "WorkPackage"  : "archimate:WorkPackage"}

DIAGRAM_MODEL = "archimate:ArchimateDiagramModel"