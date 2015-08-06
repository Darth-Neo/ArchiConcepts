#! env python
# __author__ = 'morrj140'

from bs4 import *

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def outputSoup(soup, filename=u"index.html"):
    with open(filename, u'w') as f:
        utf8_S = soup.prettify().encode("utf-8", errors="ignore")
        ascii_S = utf8_S.decode("ascii", errors="ignore")
        f.write(ascii_S)

if __name__ == u"__main__":

    dirHTML = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC3.1/"
    fileHTML = u"model.html"
    indexHTML = dirHTML + u"index.html"

    reportFile = dirHTML + fileHTML

    with open(reportFile, "r") as f:
        html = f.read()
        logger.info(u"%s[%d]=%s" % (fileHTML, len(html), type(html)))

    soup = BeautifulSoup(html)

    #
    # Insert MailTo
    # - <a href="mailto:james.m.morris@disney.com?Subject=DVC" target="_top">Inaccuracies?</a>
    # "/html/body/div[1]/nav/div[1]/span"
    sp = soup.body.div.nav.div.span

    st = soup.new_tag(u"a")
    st[u"href"] = u"mailto:james.m.morris@disney.com?Subject=DVC\" target=\"_top\""
    st.string = u"Inaccuracies?"

    sp.append(st)

    #
    # Remove relations due to size
    sp = soup.find("span", {u"class": u"i18n-relations"}).parent
    sp.extract()

    outputSoup(soup, indexHTML)
