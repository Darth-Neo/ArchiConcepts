#! env python

__author__ = 'morrj140'

from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

def createTagCloud(tcFileName):
    d = path.dirname(__file__)

    words = open(path.join(d, tcFileName)).read()

    # remove URLs, RTs, and twitter handles
    no_urls_no_tags = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                ])

    wordcloud = WordCloud(
                          font_path='/Users/morrj140/Development/src/kivy/Kivy/kivy/data/fonts/DroidSans.ttf',
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=1800,
                          height=1400
                         ).generate(no_urls_no_tags)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('./my_twitter_wordcloud_1.png', dpi=300)
    plt.show()

if __name__ == u"__main__":
    tcFileName = "const.txt"
    createTagCloud(tcFileName)