#!/usr/bin/python
#
# Natural Language Processing of Concepts from Archimate Information
#
# __author__ = u'morrj140'
# __VERSION__ = u'0.3'
#
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel
import nltk
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.stem import PorterStemmer, WordNetLemmatizer
from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


class Collocations(object):
    concepts = None

    conceptsNGram = None
    conceptNGramScore = None
    conceptsNGramSubject = None

    ngramFile = fileConceptsNGramFile
    ngramScoreFile = fileConceptsNGramScoreFile
    ngramSubjectFile = fileConceptsNGramsSubject

    def __init__(self):
        self.conceptsNGram = Concepts(u"n-gram", u"NGRAM")
        self.conceptsNGramScore = Concepts(u"NGram_Score", u"Score")
        self.conceptsNGramSubject = Concepts(u"Subject", u"Subjects")

    def getCollocationConcepts(self):
        return self.conceptsNGram, self.conceptsNGramScore, self.conceptsNGramSubject

    def find_collocations(self, concepts):
        self.concepts = concepts

        lemmatizer = WordNetLemmatizer()

        stopset = set(stop)
        filter_stops = lambda w: len(w) < 3 or w in stopset

        words = list()
        dictWords = dict()

        n = 0
        for document in self.concepts.getConcepts().values():
            n += 1
            logger.info(u"%d - Document %s" % (n, document.name[:25]))
            for concept in document.getConcepts().values():

                if not (concept.name is None):
                    logger.info(u"Word %s" % concept.name)

                    for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                        logger.debug(u"Word: " + word + u" POS: " + pos)
                        lemmaWord = lemmatizer.lemmatize(word.lower())
                        logger.debug(u"Word: " + word + u" Lemma: " + lemmaWord)
                        words.append(lemmaWord)

                        if pos[0] == u"N":
                            dictWords[lemmaWord] = word

        if False:
            for x in dictWords:
                logger.info(u"noun : %s" % x)

        bcf = BigramCollocationFinder.from_words(words)
        tcf = TrigramCollocationFinder.from_words(words)

        bcf.apply_word_filter(filter_stops)
        tcf.apply_word_filter(filter_stops)
        tcf.apply_freq_filter(3)

        listBCF = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 100)

        for bigram in listBCF:
            concept = u' '.join([bg for bg in bigram])
            e = self.conceptsNGram.addConceptKeyType(concept, u"BiGram")
            logger.info(u"Bigram  : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)

        listTCF = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 100)

        for trigram in listTCF:
            concept = ' '.join([bg for bg in trigram])
            e = self.conceptsNGram.addConceptKeyType(concept, u"TriGram")
            logger.info(u"Trigram : %s" % concept)
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept)):
                e.addConceptKeyType(word, pos)

        bcfscored = bcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)
        lt = sorted(bcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, u"BiGram")
            for x in score[0]:
                e.addConceptKeyType(x, u"BWord")
            e.count = count
            logger.debug(u"bcfscored: %s=%s" % (name, count))

        tcfscored = tcf.score_ngrams(TrigramAssocMeasures.likelihood_ratio)
        lt = sorted(tcfscored, key=lambda c: c[1], reverse=True)
        for score in lt:
            name = ' '.join([w for w in score[0]])
            count = float(score[1])
            e = self.conceptsNGramScore.addConceptKeyType(name, u"TriGram")
            for x in score[0]:
                e.addConceptKeyType(x, u"TWord")
            e.count = count
            logger.debug(u"tcfscored: %s = %s" % (name, count))

        Concepts.saveConcepts(self.conceptsNGramScore, self.ngramScoreFile)
        Concepts.saveConcepts(self.conceptsNGram, self.ngramFile)

        for concept in self.conceptsNGram.getConcepts().values():
            for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(concept.name)):
                if pos[0] == u"N":
                    e = self.conceptsNGramSubject.addConceptKeyType(word, pos)
                    e.addConceptKeyType(concept.name, u"NGRAM")

        Concepts.saveConcepts(self.conceptsNGramSubject, self.ngramSubjectFile)


class DocumentsSimilarity(object):
    conceptsDoc = None
    conceptsSimilarity = None
    conceptsSimilarityFile = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None
    topics = None
    topicConcepts = None
    lemmatizer = None
    df = None

    def __init__(self, al):
        self.num_topics = 100
        self.num_words = 50
        self.similarity = 0.95
        self.al = al

        self.conceptsSimilarityFile = u"GapsSimilarity.p"

    def createTopics(self, concepts):

        self.concepts = concepts

        self.tm = TopicsModel(directory=os.getcwd() + os.sep)

        logger.debug(u"--Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadConceptsWords(self.concepts)

        logger.info(u"--Read %s Documents, with %s words." % (str(len(self.documentsList)), str(self.wordcount)))

        logger.info(u"--Compute Topics--")
        self.topics = self.tm.computeTopics(self.documentsList, nt=self.num_topics, nw=self.num_words)

        if False:
            logger.info(u"--Log Topics--")
            self.tm.logTopics(self.topics)

        # self.listTopics = [x[0].encode('ascii', errors="ignore").strip() for x in self.topics]
        self.listTopics = [x[0] for x in self.topics]

        logger.info(u"--Saving Topics--")

        self.topicConcepts = self.tm.saveTopics(self.topics)

    def findSimilarties(self):

        logger.info(u"Compute Similarity")

        self.conceptsSimilarity = Concepts(u"ConceptsSimilarity", u"Similarities")

        # Compute similarity between documents / concepts
        similarityThreshold = self.similarity

        for document in self.documentsList:
            indexNum = self.documentsList.index(document)

            self.df = self.concepts.getConcepts().keys()

            logger.info(u"++conceptsDoc %s" % (self.df[indexNum]))
            logger.info(u"  documentsList[" + str(indexNum) + u"]=" + u"".join(x + u" " for x in document))

            # Show common topics
            d = [unicode(x).strip().replace(u"'", u"") for x in document]
            e = [unicode(y).strip().replace(u"\"", u"") for y in self.listTopics]

            s1 = set(e)
            s2 = set(d)
            common = s1 & s2
            lc = [x for x in common]
            logger.info(u"  Common Topics : %s{%s}" % (lc, self.al.dictName[document][ARCHI_TYPE]))

            self.doComputation(indexNum, similarityThreshold, tfAddWords=True)

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info(u"Saved Concepts : %s" % conceptsSimilarityFile)

        return self.conceptsSimilarity

    def doComputation(self, j, similarityThreshold, tfAddWords=True):
        logger.debug(u"--doComputation--")
        pl = self.tm.computeSimilar(j, self.documentsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug(u"   similarity above threshold - %2.3f" % (100.0 * float(pl[0][0])))
            logger.debug(u"   pl:" + str(pl))

            for l in pl:
                if l[1] != l[2]:
                    logger.debug(u"  l:" + str(l))
                    l1 = u"".join(x + u" " for x in l[1])
                    ps = self.conceptsSimilarity.addConceptKeyType(l1, u"Similar")
                    ps.count = TopicsModel.convertMetric(l[0])

                    l2 = u"".join(x + " " for x in l[2])
                    pt = ps.addConceptKeyType(l2, u"Concept")

                    common = set(l[1]) & set(l[2])
                    lc = [x for x in common]

                    logger.debug(u"  l    : %s" % l)
                    logger.debug(u"  l[1] : %s" % (l1))
                    logger.debug(u"  l[2] : %s" % (l2))
                    logger.debug(u"  Common : %s" % (lc))

                    if tfAddWords is True:
                        for x in common:
                            if not x in stop:
                                logger.debug(u"word : %s" % x)
                                pc = pt.addConceptKeyType(x, u"CommonTopic")
                                pc.count = len(lc)

        else:
            logger.debug(u"   similarity below threshold")


def gapSimilarity(fileArchimate, searchTypes):

    lemmatizer = WordNetLemmatizer()

    logger.info(u"Using : %s" % fileArchimate)

    al = ArchiLib(fileArchimate)

    nl = al.getTypeNodes(searchTypes)

    logger.info(u"Find Words...")
    concepts = Concepts(u"Word", u"Topic")

    n = 0
    for sentence in nl:
        n += 1

        if sentence is None:
            continue

        logger.info(u"%s" % sentence)

        c = concepts.addConceptKeyType(u"Document" + str(n), nl[sentence][ARCHI_TYPE])
        d = c.addConceptKeyType(sentence, nl[sentence][ARCHI_TYPE])

        cleanSentence = u' '.join([word for word in sentence.split(u" ") if word not in stop])
        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(cleanSentence)):
            if len(word) > 1 and pos[0] == u"N":
                lemmaWord =lemmatizer.lemmatize(word.lower())
                e = d.addConceptKeyType(lemmaWord, u"LemmaWord")
                f = e.addConceptKeyType(pos, u"POS")

    if False:
        concepts.logConcepts()

    if True:
        logger.info(u"Find Collocations...")
        fc = Collocations()
        fc.find_collocations(concepts)

    if True:
        npbt = DocumentsSimilarity(al)

        logger.info(u"Create Topics")
        npbt.createTopics(concepts)

        if True:
            logger.info(u"Find Similarities")

            nc = npbt.findSimilarties()

            logger.debug(u"Topics")
            listTopics = list()
            ncg = npbt.topicConcepts.getConcepts().values()
            for x in ncg:
                logger.info(u"%s[%d]" % (x.name, x.count))
                lt = (x.name, x.count)
                listTopics.append(lt)

            logger.info(u"Topics Sorted")
            with open(u"topic_sort.txt", "wb") as f:
                for x in sorted(listTopics, key=lambda c: abs(c[1]), reverse=False):
                    output = "Topic : %s[%d]" % (x[0], x[1])
                    logger.info(output)
                    f.write(output + os.linesep)


def sortConcepts(concepts,  n=0):
    pc = concepts.getConcepts()
    spaces = u" " * n

    for p in pc.values():
        if p.typeName in (u"Concept", u"Similar"):
            logger.info(u"%s%s[%s] -> Count=%s" % (spaces, p.name, p.typeName, p.count))
            sortConcepts(p, n+1)

if __name__ == u"__main__":

    if True:
        fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v3.14.archimate"

        searchTypes = list()
        searchTypes.append(u"archimate:ApplicationComponent")
        searchTypes.append(u"archimate:ApplicationFunction")
        searchTypes.append(u"archimate:ApplicationService")
        searchTypes.append(u"archimate:DataObject")
        searchTypes.append(u"archimate:BusinessEvent")
        searchTypes.append(u"archimate:BusinessProcess")
        searchTypes.append(u"archimate:BusinessObject")

        gapSimilarity(fileArchimate, searchTypes)
    else:
        conceptsSimilarityFile = u"GapsSimilarity.p"
        concepts = Concepts.loadConcepts(conceptsSimilarityFile)
        sortConcepts(concepts)
