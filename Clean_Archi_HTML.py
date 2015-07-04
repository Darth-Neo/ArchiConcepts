#! env python
# __author__ = 'morrj140'

from BeautifulSoup import *

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def outputSoup(soup, filename=u"index.html"):
    with open(filename, u'w') as f:
        f.write(soup.prettify())

if __name__ == u"__main__":

    dirHTML = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC2.14/"
    fileHTML = u"model.html"
    indexHTML = dirHTML + u"index.html"

    reportFile = dirHTML + fileHTML

    with open(reportFile, "r") as f:
        html = f.read()
        logger.info(u"%s[%d]=%s" % (fileHTML, len(html), type(html)))

    soup = BeautifulSoup(html)

    sp = soup.find(u"span", {u"class": u"i18n-relations"}).parent

    sp.extract()

    outputSoup(soup, indexHTML)
