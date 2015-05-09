#!/usr/bin/python
#
# Archimate Libray Constants
#
__author__ = u'morrj140'
__VERSION__ = u'0.1'

import os
import time

#
# Script to reset Neo4J
#
#resetNeo4J = u"/Users/morrj140/Development/neo4j/bin/reset.sh"
resetNeo4J = u"/home/james.morris/bin/reset.sh"

#
# IP of Neo4J Graph
#
LocalGBD  = u"http://localhost:7474/db/data/"
RemoteGDB = u"http://10.92.82.60:7574/db/data/"
gdb = LocalGBD
gdbTest = LocalGBD

#
# Archimate XML
#
NS_MAP={u'xsi': u'http://www.w3.org/2001/XMLSchema-instance', u'archimate': u'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP[u"xsi"]
ARCHIMATE_NS   =  NS_MAP[u"archimate"]
ARCHI_TYPE = u"{%s}type" % NS_MAP[u"xsi"]

#
# Directory for Archimate File
#
dirTest = os.getcwd() + os.sep + u"test" + os.sep
dirRun = os.getcwd() + os.sep
directory = dirTest


fileArchimateTest   = dirTest + u"Testing.archimate"
fileArchimateModel  = directory + u'archi.archimate'
fileArchimateImport = directory + u"import_artifacts.archimate"

#
# Concept Files Used
#
fileConceptsArch           = directory + u"archi.p"
fileConceptsPPTX           = directory + u"pptx.p"
fileConceptsExport         = directory + u"export.p"
fileConceptsImport         = directory + u"export.p"
fileConceptsBatches        = directory + u"batches.p"
fileConceptsTraversal      = directory + u"traversal.p"
fileConceptsEstimation     = directory + u"Estimation.p"
fileConceptsRequirements   = directory + u"reqs.p"
fileConceptsDeDups         = directory + u"dedups.p"
fileConceptsRelations      = directory + u"rel.p"
fileConceptsDocuments      = directory + u"documents.p"
fileConceptsChunks         = directory + u"chunks.p"
fileConceptsNodes          = directory + u"nodes.p"
fileConceptsNGramsSubject  = directory + u"ngramsubject.p"
fileConceptsNGramFile      = directory + u"ngrams.p"
fileConceptsNGramScoreFile = directory + u"ngramscore.p"

#
# Common Filenames
#

filePPTXIn    = directory + u"test_in.pptx"
filePPTXOut   = directory + u"test_out.pptx"

fileExcelIn  = directory + u'Template_Estimate.xlsx'
fileExcelOut = directory + u'Template_Estimate_new.xlsx'

fileCSVExport = directory + u"export.csv"
fileCSVExportTime = directory + u"export" + time.strftime(u"%Y%d%m_%H%M%S") + u".csv"

fileReportExport     = directory + u"report.csv"
fileReportExportTime = directory + u"report" + time.strftime(u"%Y%d%m_%H%M%S") + u".csv"

fileCSVQueryExport      = directory + u"ExportQuery.csv"
fileCSVQueryExportTime  = directory + u"ExportQuery" + time.strftime(u"%Y%d%m_%H%M%S") + u".csv"

fileImageExport      = directory + u"export.png"
fileImageExportTime  = directory + u"export" + time.strftime(u"%Y%d%m_%H%M%S") + u".png"

#
# Archimate Edges
#
relations = {u"TriggeringRelationship" : u"archimate:TriggeringRelationship",
                    u"UsedByRelationship" : u"archimate:UsedByRelationship",
                    u"AccessRelationship" : u"archimate:AccessRelationship",
                    u"FlowRelationship" : u"archimate:FlowRelationship",
                    u"AssignmentRelationship" : u"archimate:AssignmentRelationship",
                    u"AssociationRelationship" : u"archimate:AssociationRelationship",
                    u"RealisationRelationship" : u"archimate:RealisationRelationship",
                    u"CompositionRelationship" : u"archimate:CompositionRelationship",
                    u"AssignmentRelationship" : u"archimate:AssignmentRelationship",
                    u"AggregationRelationship": u"archimate:AggregationRelationship",
                    u"SpecialisationRelationship" : u"archimate:SpecialisationRelationship"}

#
# Archimate Nodes
#
entities = {u"BusinessEvent" : u"archimate:BusinessEvent",
            u"BusinessObject" : u"archimate:BusinessObject",
            u"BusinessProcess" : u"archimate:BusinessProcess",
            u"ApplicationService" : u"archimate:ApplicationService",
            u"ApplicationComponent" : u"archimate:ApplicationComponent",
            u"ApplicationFunction" : u"archimate:ApplicationFunction",
            u"DataObject" : u"archimate:DataObject",
            u"Requirement" : u"archimate:Requirement",
            u"Stakeholder" : u"archimate:Stakeholder",
            u"WorkPackage"  : u"archimate:WorkPackage"}

folders = {u"Business", u"Application", u"Technology", u"Motivation", u"Implementation & Migration", u"Connectors", u"Relations" }

DIAGRAM_MODEL = u"archimate:ArchimateDiagramModel"
DIAGRAM_OBJECT = u"archimate:DiagramObject"