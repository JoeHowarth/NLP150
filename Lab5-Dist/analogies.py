import pickle, re, numpy as np, pandas as pd, math, sys
from pprint import pprint


## set file names
mat_file = 'matrix5000.hdf'
ppmi_file = 'ppmi5000.hdf'
svd_file = 'svd5000.hdf'

if (len(sys.argv) != 1):
    sentence = sys.argv[1:]
    main_loop(sentence)

while True:
    print("    X is to Y as A is to")
    sentence = input()
    sentence = sentence.split()

    if sentence[0] is "quit":
        break

    main_loop(sentence)

#################################################
## input a list of words, print most likely answer based on ppmi and svd models
# Example:
    # fly(1b) is to plane(1a) as drive(2b) is to
    # ||wx − wdrive + wfly − wplane||2
    # ||wx + (− an2b + an1b − an1a)||2
    # ||wx + comb||2
#################################################
def main_loop(sentence):

    an1b = sentence[0]
    an1a = sentence[3]
    an2b = sentence[5]
    print("words: ",an1b, an1a, an2b)

    ## open ppmi matrix
    matrix = pd.read_hdf(ppmi_file,'mat1')

    ## perform calc
    dists = vecThing(an1a, an1b, an2b, matrix)
    dists = pd.Series(dists, index=matrix.index).sort_values()
    print("PPMI best fits:")
    print(dists[:4])
    print()

    ## open ppmi matrix
    matrix = pd.read_hdf(svd_file,'mat1')
    matrix = matrix.iloc[:,:1000]

    ## perform calc
    dists = vecThing(an1a, an1b, an2b, matrix)
    dists = pd.Series(dists, index=matrix.index).sort_values()
    print("PPMI best fits:")
    print(dists[:6])

def vecThing(an1a, an1b, an2b, matrix):
    v1a = matrix.loc[an1a].values
    v1b = matrix.loc[an1b].values
    v2b = matrix.loc[an2b].values

    comb = v1b - v1a - v2b

    dists = np.linalg.norm(matrix.values + comb, axis=1) ** 2
    return dists
