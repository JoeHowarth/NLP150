import xml.etree.ElementTree as ET
import nltk.classify
from nltk.classify import maxent
import random
import math
from nltk.corpus import stopwords
from pprint import pprint
import numpy as np
stpwords = stopwords.words('english')
import re
import pickle
import sys
from nltk import ngrams, RegexpTokenizer, FreqDist


## extra output for debugging
debug = 0
real = True
output = False

def main():
    trainfile = ""
    testfile = ""
    if len(sys.argv) == 2:
        trainfile = sys.argv[1]
        # print("hi",trainfile)

    elif len(sys.argv) == 3:
        trainfile = sys.argv[1]
        testfile = sys.argv[2]
        # print("hi",trainfile, testfile)
    else:
        trainfile = "TrainingSet.xml"
        testfile = trainfile

    train_xml = get_xml(trainfile)[:]
    test_xml = get_xml(testfile)[:]

    train, Ytrain, train_ID, test, Ytest, test_ID = revs_labels(train_xml, test_xml)
    num_features = 300
    num_bigrams = 40
    num_trigrams = 2
    all_words, all_bigrams, all_trigrams, feat_words, feat_bigrams, feat_trigrams = get_vocab(train, num_features, num_bigrams, num_trigrams)
    # all_words, all_bigrams, feat_words, feat_bigrams = get_vocab(train, num_features, num_bigrams)

    x_feat_list = features(train, feat_words, feat_bigrams, feat_trigrams)
    y_feat_list = features(test, feat_words, feat_bigrams, feat_trigrams)
    test_zip = list(zip (y_feat_list, Ytest))
    train_zip = list(zip (x_feat_list, Ytrain))

    # quick test
    v = 0.05

    # normal
    # v = 0.01

    # long
    # v = 0.005
    model, pred = run_model(train_zip, test_zip, y_feat_list, v, output=output)
    for ID,pred in list(zip(test_ID, pred)):
        print("%s\t%s"% (ID.strip(), pred))

def get_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    root = [rev for rev in root]
    return root

def run_model(train_zip, test_zip, y_feat_list, v=0.01, output=True):
    encoding = maxent.TypedMaxentFeatureEncoding.train(train_zip)
    if output:
        trace = 3
    else:
        trace = 0
    model = maxent.MaxentClassifier.train(train_zip, encoding=encoding, trace=trace, min_lldelta=v)
    if output: print(nltk.classify.accuracy(model, test_zip))
    pred = model.classify_many(y_feat_list)
    return model, pred




def revs_labels(train_xml, test_xml):
    train  = [0] * len(train_xml)
    Ytrain = [0] * len(train_xml)
    train_ID = [0] * len(train_xml)
    for i in range(len(train_xml)):
        train[i] = train_xml[i].find("review_text").text.lower()
        y = float(train_xml[i].find("rating").text)
        if (y < 3):
            Ytrain[i] = 'neg'
        else:
            Ytrain[i] = 'pos'
        # train_ID[i] = train_xml[i].find("unique_id").text
        train_ID[i] = train_xml[i].find("asin").text



    # train[0].find("review_text").text
    test  = [0] * len(test_xml)
    Ytest = [0] * len(test_xml)
    test_ID  = [0] * len(test_xml)
    for i in range(len(test_xml)):
        test[i] = test_xml[i].find("review_text").text.lower()
        if not real:
            Ytest[i] = str(int(float(test_xml[i].find("rating").text)))
            y = float(test_xml[i].find("rating").text)
            if (y < 3):
                Ytest[i] = 'neg'
            else:
                Ytest[i] = 'pos'
        # test_ID[i] = test_xml[i].find("unique_id").text
        test_ID[i] = test_xml[i].find("asin").text

    return train, Ytrain, train_ID, test, Ytest, test_ID


def get_vocab(train, num_words=500, num_bigrams=50, num_trigrams=10):
    tokenizer = RegexpTokenizer(r'[a-z][a-z\']*').tokenize
    tokenized = [tokenizer(rev) for rev in train]

    all_words = [x for rev in tokenized for x in rev]
    all_words = [x for x in all_words if x not in stpwords]
    all_bigrams = list(ngrams(all_words, 2))
    all_trigrams = list(ngrams(all_words, 3))

    word_fdist = FreqDist(all_words)
    bigram_fdist = FreqDist(all_bigrams)
    trigram_fdist = FreqDist(all_trigrams)

    feat_words = word_fdist.most_common(num_words)
    feat_bigrams = bigram_fdist.most_common(num_bigrams)
    feat_trigrams = trigram_fdist.most_common(num_trigrams)

    feat_words = [a for a,b in feat_words]
    feat_bigrams = [a for a,b in feat_bigrams]
    feat_trigrams = [a for a,b in feat_trigrams]


    return all_words, all_bigrams, all_trigrams, feat_words, feat_bigrams, feat_trigrams
#     return all_words, all_bigrams, feat_words, feat_bigrams



def features (revs, words, bigrams, trigrams):
    feat_list = []
    tokenizer = RegexpTokenizer(r'[a-z][a-z\']*').tokenize
    for text in revs:
        feat = {}
        tokens = [x for x in tokenizer(text) if x not in stpwords]
        text_bigrams = list(ngrams(tokens, 2))
        text_trigrams = list(ngrams(tokens, 3))
#         print(text_trigrams)
        for bg in bigrams:
            feat[bg] = int(bg in text_bigrams)
        for tg in trigrams:
            feat[tg] = int(tg in text_trigrams)
        for word in words:
            feat[word] = int(word in text)
        feat_list.append(feat)

    return feat_list

def find_best_feats(model, num_features=100):
    from contextlib import redirect_stdout
    ## nltk's most informative features prints to std out
    #  extract labels from output

    with open('help.txt', 'w') as f:
        with redirect_stdout(f):
            model.show_most_informative_features(300)
    with open('help.txt', 'r') as f:
        idk = re.findall(u'\s[a-z][a-z\']*=', f.read())

        idk = [re.findall(u'[a-z\']+', s) for s in idk]
        idk = [x for y in idk for x in y]
    with open('most_helpful.txt', 'wb') as f:
        pickle.dump(idk, f)
    return idk



def check_acc(pred, Ytest):
    thing = list(zip(pred, Ytest))

    correct = 0
    total = 0
    for (p,r) in thing:
        if p == r:
            correct += 1
    #         print("correct", p,r)
        else:
    #         print("incorrect", p,r)
            total += 1
    #     print(p,r)
    print(correct, total)
    # pprint(thing)

    if debug > 1:
        print(Ytrain.count('pos'),Ytrain.count('neg'), len(Ytrain))
        print(Ytest.count('pos'),Ytest.count('neg'), len(Ytest))

        print(Ytrain[:150])
         #pprint(list(zip(Ytrain[250:255],train[250:255])))



if __name__ == "__main__":
    main()
