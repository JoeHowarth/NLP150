import nltk
from nltk import ngrams, word_tokenize, RegexpTokenizer, FreqDist, sent_tokenize
from pprint import pprint
import numpy as np
import pandas as pd
from random import random

## books liscensces removed
#books = ["SHolmes.txt","Frankenstein.txt","Dracula.txt", "TheYellowWallpaper.txt"]
#books = ["Frankenstein.txt","Dracula.txt", "TheYellowWallpaper.txt"]
books = ["Frankenstein.txt","Dracula.txt","SHolmes.txt"]

raws = []
for book in books:
    f = open(book,"r")
    raws.append(f.read())
    f.close()
# make lowercase
raws = [raw.lower() for raw in raws]

# separate into sentences
sent_texts = [sent_tokenize(raw) for raw in raws]

# tokenize sentence strings to lists of tokens
tokenizer = RegexpTokenizer(r'[a-z][a-z\']*').tokenize
texts = []
print(len(sent_texts))
for i in range(len(sent_texts)):
    texts.append( [tokenizer(sent) for sent in sent_texts[i]] )

def bigramCounts (sents, lexicon):
    #len_lex = len(lexicon)
    prev = ['start0'] + lexicon
    curr = ['end1']   + lexicon

    #listBigram = []

   # print(type(prev),type(curr),prev)
    counts = pd.DataFrame(0, prev, curr)
    for sent in sents:
        len_sent = len(sent)

        if (len_sent == 0):
            continue

        # count start marker
        counts.at['start0',sent[0]] += 1

        for i in range(len_sent - 1):
            counts.at[sent[i],sent[i+1]] += 1

        # for end marker
        counts.at[sent[len_sent - 1], 'end1'] += 1
    return counts

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

flattened = [word for text in texts for sent in text for word in sent]

## set of words in each book
book_lexicon = []
for i in range(len(texts)):
    flat = [word for sent in texts[i] for word in sent]
    book_lexicon.append(sorted(set(flat)))

# list of bigrams occuring greater than min_num times
def freq_bigrams(sents, lexicon, min_num):
    listBigram = bigramList(sents)
    fdist = FreqDist(listBigram)
    big_bgram = [ k for k,v in fdist.items() if v>min_num]
    return big_bgram

# list of trigrams occuring greater than min_num times
def freq_trigrams(sents, lexicon, min_num):
    listBigram = trigramList(sents)
    fdist = FreqDist(listBigram)
    big_bgram = [ k for k,v in fdist.items() if v>min_num]
    return big_bgram

frank_common = freq_trigrams(texts[0] ,book_lexicon[0], 6)
drac_common = freq_trigrams(texts[1] ,book_lexicon[1], 6)
yellow_common = freq_trigrams(texts[2] ,book_lexicon[2], 6)

## how many
print(len(frank_common),len(drac_common),len(yellow_common))

fl = len(frank_common)
dl = len(drac_common)
yl = len(yellow_common)

FnD = set(frank_common).intersection(drac_common)
FnY = set(frank_common).intersection(yellow_common)
DnY = set(drac_common).intersection(yellow_common)

print("Trigrams in common between:")
print("Frankenstein and Dracula: ",len(FnD))
print("Frankenstein and The Yellow Wallpaper: ",len(FnY))
print("Dracula and The Yellow Wallpaper: ",len(DnY))
print("Normalized:")
print(round(100*len(FnD)/(fl+dl), 4), "% ",round(100*len(FnY)/(fl+yl), 4), "% ",round(100*len(DnY)/(dl+yl), 4), "% ")
print("Therefore Frankenstein and Dracula are the most similar, followed by Frankenstein and The Yellow Wallpaper")


counts = [bigramCounts(texts[i], book_lexicon[i]) for i in range(3)]
#counts_smooth = [count.add(0.001) for count in counts]

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


print("")
print("Now that Shelly has chosed Stoker as the winner, here is their conversation")
for i in range(5):
    print("Shelly: ",make_sentence(probs[0]))
    print("Stoker: ",make_sentence(probs[1]))
    print("")

print("")
print("Not quite sure how they became authors...")
