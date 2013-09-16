#!/usr/bin/python

#from sklearn.feature_extraction import DictVectorizer
import nltk
import syllabification as s
import stress as util #utility functions

TRAIN_FILENAME = "data/gcide/gc/train"
TEST_FILENAME = "data/gcide/gc/test"

AHEAD = "^" # non-word chars for classifier
BEHIND = "$"

#convert a list of words into a list of 'pieces'
# piece: (syll_def, stress)
# syll_def: [index_in_syllcores, list_of_syllcore_indexes, word]
def get_pieces(wordlist):
  pieces = []
  for word, stressed in wordlist.items():
    sylls = util.split_sylls(stressed)
    nuclei = s.find_all_syll_nuclei(sylls)
    stresses = util.get_stresses(stressed)

    for index in range(0, len(nuclei)):
      piece = (index, nuclei, word)
      stress = stresses[index]
      pieces.append((piece, stress))
  return pieces


# takes
#   the index of a syllable (in the list of syllables), 
#   the index of the syllables in the word
#   the word
# returns
# a featureset: {featurename: feature, ...}
def get_features(index, syllcores, word):
  features = {}
  for funct in featurefuncts:
    features[funct.__name__] = funct(index, syllcores, word)
  return features

# takes a list of 'pieces'
# returns a list of [(featureset, stress_marking)...]
def get_all_features(pieces):
  return [(get_features(piece[0], piece[1], piece[2]), stress)
          for piece, stress in pieces]

# feature functions
# functios which take in the identifying information about a syllable, and return a feature
def position_in_sylls(index, syllcores, word): return index
def position_in_sylls_backward(index, syllcores, word): return len(syllcores) - index
def number_of_sylls(index, syllcores, word): return len(syllcores)
def pos3(index, syllcores, word): return wordat(3, index, syllcores, word)
def pos2(index, syllcores, word): return wordat(2, index, syllcores, word)
def pos1(index, syllcores, word): return wordat(1, index, syllcores, word)
def pos0(index, syllcores, word): return wordat(0, index, syllcores, word)
def posneg1(index, syllcores, word): return wordat(-1, index, syllcores, word)
def posneg2(index, syllcores, word): return wordat(-2, index, syllcores, word)
def posneg3(index, syllcores, word): return wordat(-3, index, syllcores, word)
# distance to prev/next nuclei?

#list of feature functions
featurefuncts = [position_in_sylls, position_in_sylls_backward, number_of_sylls,
                 pos3, pos2, pos1, pos0, posneg1, posneg2, posneg3]

#helper function for feature functions
def wordat(point, index, syllcores, word):
  try:
    return word[syllcores[index]+point]
  except IndexError:
    if point < 0:
      return AHEAD
    if point > 0:
      return BEHIND


#print word

#main
train_wordlist = util.read_in(TRAIN_FILENAME)
test_wordlist = util.read_in(TEST_FILENAME)
train_pieces = get_pieces(train_wordlist)
test_pieces = get_pieces(test_wordlist)
print train_pieces[:5]
train_features = get_all_features(train_pieces)
test_features = get_all_features(test_pieces)
print train_features[:5]

classifier = nltk.NaiveBayesClassifier.train(train_features)
print nltk.classify.accuracy(classifier, test_features)
classifier.show_most_informative_features(10)

print classifier.classify(get_features(0, [1, 4], 'jawbone'))
print classifier.classify(get_features(1, [1, 4], 'jawbone'))




