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
# Test Archimate File
#
dirTest = os.getcwd() + os.sep + "test" + os.sep
fileArchimateTest = dirTest + "Testing.archimate"

gdbTest = "http://localhost:7474/db/data/"

#
# Script to reset Neo4J
#
resetNeo4J = "/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"

#
# Concept Files Used
#
fileConceptsArch           = dirTest + "archi.p"
fileConceptsPPTX           = dirTest + "pptx.p"
fileConceptsExport         = dirTest + "export.p"
fileConceptsBatches        = dirTest + "batches.p"
fileConceptsTraversal      = dirTest + "traversal.p"
fileConceptsEstimation     = dirTest + "Estimation.p"
fileConceptsRequirements   = dirTest + "req.p"
fileConceptsRelations      = dirTest + "rel.p"
fileConceptsDocuments      = dirTest + "documents.p"
fileConceptsChunks         = dirTest + "chunks.p"
fileConceptsNodes          = dirTest + "nodes.p"
fileConceptsNGramsSubject  = dirTest + "ngramsubject.p"

#
# Common Filenames
#

filePPTXIn    = dirTest + "test_in.pptx"
filePPTXOut   = dirTest + "test_out.pptx"

fileExcelIn  = dirTest + 'Template_Estimate.xlsx'
fileExcelOut = dirTest + 'Template_Estimate_new.xlsx'

fileCSVExport = dirTest + "export.csv"
fileCSVExportTime = dirTest + "export" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileReportExport     = dirTest + "report.csv"
fileReportExportTime = dirTest + "report" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileCSVQueryExport      = dirTest + "ExportQuery.csv"
fileCSVQueryExportTime  = dirTest + "ExportQuery" + time.strftime("%Y%d%m_%H%M%S") +".csv"

fileImageExport      = dirTest + "export.png"
fileImageExportTime  = dirTest + "export" + time.strftime("%Y%d%m_%H%M%S") +".png"

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
