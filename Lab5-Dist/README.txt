Note: I tried using a vocab of the 20000 most frequent words, but
      this caused memory errors when using SVD so I used a 5000 word vocab
      instead.

### PART 2 ###
PPMI version
````````````
1.)
bird is to sky as fish is to
Answer:
  1st) sky
  2nd) fish
  3rd) like

2.)
water is to waves as air is to
Answer:
  1st) waves
  2nd) air
  3rd) one
  4th) would

3.)
black is to black as white is to
Answer:
  1st) white  <------------------ interestingly black did NOT show up and
  2nd) one                            and white is the answer, soo... YEAH
  3rd) like
  3rd) first


### PART 3 ###
SVD version
```````````
1.)
bird is to sky as fish is to
Answer:
  1st) sky
  2nd) fish
  3rd) like

2.)
water is to waves as air is to
Answer:
  1st) waves
  2nd) air
  3rd) tsunami   <---------  not what we're looking for, but waves ~ tsunami
  4th) one

3.)
water is to waves as air is to
Answer:
  1st) white  <-------------   same as ppmi version...
  2nd) one
  3rd) would
  4th) like

Comments:
    Unfortunately this technique does not seem to produce good results for
    answering analogies. This is probably because I had to use a substantially
    reduced vocab size to make the co-variance matrix.

### PART 4 ###
``````````````
Analogy:    skull is to hamlet as horcrux is to voldemort
Definitely won't be able to solve that one, expecially because those words
aren't in my matrix muhahahahah
