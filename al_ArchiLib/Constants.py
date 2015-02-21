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