import re
import xml.etree.cElementTree as ET
import nltk
from nltk.corpus import stopwords
from pprint import pprint

book = open("Blithedale_Romance.txt", "r")

## get title and author from beginning of text
book.readline()
title_str = "\n<booktitle>" + book.readline()[:-1] + "</booktitle>\n"
book.readline()
book.readline()
book.readline()
author_str = "<author>" + book.readline()[:-1] + "</author>"

text = book.read()

chapterReg = re.compile('^[IVX]+\.\s[A-Z\,\- \']+', re.M)
paraReg    = re.compile('\\n\\n[\\n]*')
remBadPara1 = re.compile('</chaptertitle></paragraph>')
remBadPara2 = re.compile('<paragraph></chapter>')

chaps = chapterReg.findall(text)
chaps = ["<chaptertitle>" + chap + "</chaptertitle>" for chap in chaps]
#[print(chap) for chap in chaps]


chapSplit = chapterReg.split(text)
#print(len(chapSplit), len(chaps))
for i in range(len(chapSplit) - 2):
    newChap = "\n<chapter>" + chaps[i] + chapSplit[i+1] + '</chapter>'
    newChap = paraReg.sub("</paragraph>\n<paragraph>",newChap)
    chapSplit[i] = newChap

BookXML = "".join(chapSplit)

## calculate word frequency, top 50
default_stopwords = set(nltk.corpus.stopwords.words('english'))
words = nltk.word_tokenize(text)
words = [word for word in words if len(word) > 1]
words = [word for word in words if not word.isnumeric()]
words = [word.lower() for word in words]
words = [word for word in words if word not in default_stopwords]
fdist = nltk.FreqDist(words)
freqs = list()
for word, frequency in fdist.most_common(50):
    freqs.append(u'<pair><word>{}</word><freq>{}</freq></pair>'.format(word, frequency))
#print (freqs)
freqs2 = "\n".join(freqs)
#print(freqs2)

quoteReg = re.compile('\"([^\"]+)\"')
#print(quoteReg.findall(BookXML))
BookXML = quoteReg.sub(r"<quote>\1</quote>", BookXML)

BookXML = remBadPara1.sub("</chaptertitle>\n", BookXML)
BookXML = remBadPara2.sub("</chapter>\n", BookXML)
BookXML = author_str + title_str + freqs2 + BookXML
BookXML = "<root><book>\n" + BookXML + "</book></root>"
#pprint(chapSplit[-3])
#pprint(BookXML)


out = open("BookXML.xml", "w")
out.write(BookXML)


# print(title)

titleReg = re.compile('[A-Z]')
