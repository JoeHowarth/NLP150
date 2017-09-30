import nltk
from nltk import ngrams, word_tokenize, RegexpTokenizer, FreqDist, sent_tokenize
from pprint import pprint
import numpy as np
import pandas as pd
from random import random
import math

## books liscensces removed
#books = ["SHolmes.txt","Frankenstein.txt","Dracula.txt", "TheYellowWallpaper.txt"]
#books = ["Frankenstein.txt","Dracula.txt", "TheYellowWallpaper.txt"]
books = ["SHolmes.txt","Frankenstein.txt","Dracula.txt"]

raws = []
for book in books:
    f = open(book,"r")
    raws.append(f.read())
    f.close()
## make lowercase
raws = [raw.lower() for raw in raws]

## separate into sentences

sent_texts = [sent_tokenize(raw) for raw in raws]

## tokenize sentence strings to lists of tokens

tokenizer = RegexpTokenizer(r'[a-z][a-z\']*').tokenize
texts = []
#print(len(sent_texts))

for i in range(len(sent_texts)):
    texts.append( [tokenizer(sent) for sent in sent_texts[i]] )

## make lexicon
book_lexicon = []
for i in range(len(texts)):
    flat = [word for sent in texts[i] for word in sent]
    book_lexicon.append(sorted(set(flat)))

## Tokens per book
flats = [[T for s in text for T in s] for text in texts]

#################
### Functions ###
#################

def bigramList (sents):
    listBigram = []

    for sent in sents:
        len_sent = len(sent)
        if (len_sent == 0):
            continue

        # count start marker
        listBigram.append(('start0',sent[0]))

        for i in range(len_sent - 1):
            listBigram.append((sent[i],sent[i+1]))

        # for end marker
        listBigram.append((sent[len_sent - 2],'end1'))
    return listBigram
def trigramList (sents):

    listBigram = []

    for sent in sents:
        len_sent = len(sent)
        if (len_sent < 2):
            continue

        # count start marker
        listBigram.append(('start0',sent[0],sent[1]))

        for i in range(len_sent - 2):
            listBigram.append((sent[i],sent[i+1],sent[i+2]))

        # for end marker
        listBigram.append((sent[len_sent - 3], sent[len_sent - 2],'end1'))
    return listBigram

def sublinear_tf (fdist):
    return {k: (1+ math.log(v)) for k,v in fdist.items()}

def inv_doc_freq (ngs):
    idfs = {}
    ## make lexicon of n-grams for each book
    lexs = [set(ngL) for ngL in ngs]
    num_books = len(ngs)
    lex_comb = set().union(*lexs)
    for ngram in lex_comb:
        num_matches = sum([ngram in lex for lex in lexs])
        idfs[ngram] = 1 + math.log(num_books / num_matches )
    #print(idfs.keys())
    return idfs

def tfidf(ngs):
    idfs = inv_doc_freq(ngs)
    tfidf_books = []

    for ngL in ngs:
        book_tfidf = []
        fdist = FreqDist(ngL)
        tfDict = sublinear_tf(fdist)

        for term in idfs.keys():
            tf = tfDict.get(term, 0)
            book_tfidf.append(tf * idfs.get(term, 0))

        tfidf_books.append(book_tfidf)
    return tfidf_books

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude


ngs = [bigramList(text) for text in texts]
rep_tfidf = tfidf(ngs)
means = [np.mean(x) for x in rep_tfidf]
#[print(mean) for mean in means]

tfidf_comparisons = []
for i, doc_0 in enumerate(rep_tfidf):
    for j, doc_1 in enumerate(rep_tfidf):
        if (j >= i):
            tfidf_comparisons.append((round(cosine_similarity(doc_0, doc_1),4), books[i], books[j]))

best_matches = []
for x in sorted(tfidf_comparisons, reverse=True):
    if (x[0] != 1.0):
        print(x)
        best_matches.append(x[1])


################
## Generation ##
################


def bigramCounts (sents, lexicon):
    prev = ['start0', 'unk1'] + (lexicon)
    curr = ['end1', 'unk1'] + lexicon

    counts = pd.DataFrame(0.0, prev, curr)
    for sent in sents:
        len_sent = len(sent)

        if (len_sent < 2):
            continue

        # count start marker
        counts.at['start0',sent[0]] += 10

        for i in range(len_sent - 1):
            counts.at[sent[i],sent[i+1]] += 1

        # for end marker
        counts.at[sent[len_sent - 1], 'end1'] += 1
    return counts

counts = [bigramCounts(texts[i], book_lexicon[i]) for i in range(3)]
probs = [count.div(count.sum(axis=1), axis=0) for count in counts]

def choose_word(prob, prev_word):
    P = prob.loc[prev_word,:].as_matrix()
    x = random()
    for i in range(len(P)):
        x -= P[i]
        if x <= 0:
            word = list(prob)[i]
            break;
    return word

def make_sentence(prob):
    sentence = ""
    word = choose_word(prob, "start0")

    while (word != "end1"):
        sentence += word + " "
        word = choose_word(prob, word)
    return sentence

#### Shelly and best
print("----------------------")
print("")
print("Now that Shelly has chosen Stoker as the winner, here is their conversation")
print("")


for i in range(3):
    print("Shelly: ",make_sentence(probs[0]))
    print("Stoker: ",make_sentence(probs[1]))
    print("")

print("")
print("Not quite sure how they became authors...")

#### Worst and their best

print("")
print("----------------------")
print()
print("Poor Sir Aurthor Connon Doyle...")
print("Here's his conversation with his best match: Stoker!")
print("Take that Shelly!")
print("")

for i in range(3):
    print("Shelly: ",make_sentence(probs[0]))
    print("Stoker: ",make_sentence(probs[2]))
    print("")

print("")
print("Not quite sure how they became authors...")
print("...Either")
