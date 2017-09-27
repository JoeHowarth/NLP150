import nltk

# opens files
flip = open("flip.txt", "r")
flop = open("flop.txt", "w")
original = flip.read()

# reversed by char
print(original[::-1], file=flop)

# reversed by  words
split_words = original.split()
reversed_words = split_words[::-1]
print("".join(reversed_words), file=flop)

# find words in emma by Jane Austen
emma = nltk.corpus.gutenberg.words('austen-emma.txt')
print(len(emma), file=flop)

# Make note of two different expressions or wordings
#  that you use for which the literal meaning in no
#  way corresponds to the meaning you intended.
print("not your cup of tea", file=flop)
print("shoot yourself in the foot", file=flop)


flop.close()
