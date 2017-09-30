import nltk
from nltk import ngrams, word_tokenize, RegexpTokenizer, FreqDist

## books liscensces removed

raws = []
f = open("SHolmes.txt","r")
raws = f.read()
f = open("Frankenstein.txt","r")
b_fra = f.read()
f = open("Dracula.txt","r")
b_dra = f.read()

tokenizer = RegexpTokenizer(r'[A-Za-z\']+').tokenize
#tokenizer = word_tokenize()



t_hol = tokenizer(b_hol)
t_fra = tokenizer(b_fra)
t_dra = tokenizer(b_dra)

n = 3
ng_hol = ngrams(t_hol, n)
ng_fra = ngrams(t_fra, n)
ng_dra = ngrams(t_dra, n)

ngs = [ng_hol, ng_fra, ng_dra]


#compute frequency distribution for all the bigrams in the text
fdists = [FreqDist(ng) for ng in ngs]

common_ngs = []
for fdist in fdists:
    print(type(fdist))
    common_ngs.append([k for k,v in fdist if v>4])

for k,v in fdists[0].items():
    if( v > 4):
        print (k,v)
