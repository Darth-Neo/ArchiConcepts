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
gdbTest = LocalGBD

#
# Archimate XML
#
NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]
ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

#
# Directory for Archimate File
#
dirTest = os.getcwd() + os.sep + "test" + os.sep
dirRun = os.getcwd() + os.sep

directory = dirRun


fileArchimateTest   = dirTest + "Testing.archimate"
fileArchimateModel  = directory + 'archi.archimate'
fileArchimateImport = directory + "import_artifacts.archimate"

fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v28.archimate"

#
# Concept Files Used
#
fileConceptsArch           = directory + "archi.p"
fileConceptsPPTX           = directory + "pptx.p"
fileConceptsExport         = directory + "export.p"
fileConceptsImport         = directory + "export.p"
fileConceptsBatches        = directory + "batches.p"
fileConceptsTraversal      = directory + "traversal.p"
fileConceptsEstimation     = directory + "Estimation.p"
fileConceptsRequirements   = directory + "reqs.p"
fileConceptsDeDups         = directory + "dedups.p"
fileConceptsRelations      = directory + "rel.p"
fileConceptsDocuments      = directory + "documents.p"
fileConceptsChunks         = directory + "chunks.p"
fileConceptsNodes          = directory + "nodes.p"
fileConceptsNGramsSubject  = directory + "ngramsubject.p"
fileConceptsNGramFile      = directory + "ngrams.p"
fileConceptsNGramScoreFile = directory + "ngramscore.p"

#
# Common Filenames
#

filePPTXIn    = directory + "test_in.pptx"
filePPTXOut   = directory + "test_out.pptx"

fileExcelIn  = directory + 'Template_Estimate.xlsx'
fileExcelOut = directory + 'Template_Estimate_new.xlsx'

fileCSVExport = directory + "export.csv"
fileCSVExportTime = directory + "export" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileReportExport     = directory + "report.csv"
fileReportExportTime = directory + "report" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileCSVQueryExport      = directory + "ExportQuery.csv"
fileCSVQueryExportTime  = directory + "ExportQuery" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileImageExport      = directory + "export.png"
fileImageExportTime  = directory + "export" + time.strftime("%Y%d%m_%H%M%S") +".png"

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