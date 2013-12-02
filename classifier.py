#!/usr/bin/python

#from sklearn.feature_extraction import DictVectorizer
import nltk
import syllabification as s
import stress as util #utility functions
import pprint

TRAIN_FILENAME = "data/gcide/gc/train"
TEST_FILENAME = "data/gcide/gc/test"
ALL_FILENAME = "data/gcide/gc/wordlist.2.CIDE"

AHEAD = "^" # non-word chars for classifier
BEHIND = "$"



##### LOW CLASSIFIER #####

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
def pos_in_sylls(index, syllcores, word): return index
def pos_in_sylls_backward(index, syllcores, word): return (len(syllcores) - 1) - index
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
featurefuncts = [pos_in_sylls, pos_in_sylls_backward, number_of_sylls,
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
def get_word_stressed(low_classifier, word):
  syll_cores = s.get_nuclei(word)
  full_stress = []
  for index in range(len(syll_cores)):
    stress = low_classifier.classify(get_features(index, syll_cores, word))
    full_stress.append((syll_cores[index], stress))
  return full_stress

def get_syll_probs(low_classifier, piece):
  return low_classifier.prob_classify(get_features(piece[0], piece[1], piece[2]))

def print_stressed_word(low_classifier, word):
  stresses = get_word_stressed(low_classifier, word)
  print util.print_stress(stresses)
  print word


def test_low_classifier():

  train_wordlist = util.read_in(TRAIN_FILENAME)
  test_wordlist = util.read_in(TEST_FILENAME)
  train_pieces = get_pieces(train_wordlist)
  test_pieces = get_pieces(test_wordlist)
  #print train_pieces[:5]
  train_features = get_all_features(train_pieces)
  test_features = get_all_features(test_pieces)
  #print train_features[:5]

  classifier = nltk.NaiveBayesClassifier.train(train_features)
  print nltk.classify.accuracy(classifier, test_features)
  classifier.show_most_informative_features(10)

  for word, correct in train_wordlist.items():
    print_stressed_word(classifier, word)
    print "  (correct " + correct + ")"

def get_low_classifier():
  all_wordlist = util.read_in(ALL_FILENAME)
  all_pieces = get_pieces(all_wordlist)
  all_features = get_all_features(all_pieces)
  return nltk.NaiveBayesClassifier.train(all_features)


##### HIGH CLASSIFIER #####

from wordstress import WordStressModel
def get_high_classifier():
  all_wordlist = util.read_in(ALL_FILENAME)
  model = WordStressModel()
  for word, stressed in all_wordlist.items():
    stress = [syll[1] for syll in util.derive_stress(stressed)]
    #print "stressed", stressed
    #print "derived stress", util.derive_stress(stressed)
    #if (stress != [0]):
    #  print "training on", stress
    #else:
    # print "bad"
    model.train(stress)
  print "model"
  #pprint.pprint(model)
  return model


###Score

from copy import deepcopy
def find_all_possible_stresses(n):
  # given a length return all possible ways to stress it
  # using our predefined stress marks
  # ex: 1 -> ["/"], ["\"], ["-"]
  # should return 3^n solution for each n

  if n == 0:
     return [[]]
  else:
     solutions = []
     recursive_case = find_all_possible_stresses(n-1)
     for r in recursive_case:
       for stress_mark in [0, 1, 2]:
         copy = deepcopy(r)
         copy.append(stress_mark)
         solutions.append(copy)
     return solutions

def pick_stress(word):
  syll_nuclei = s.get_nuclei(word)
  potential_stresses = find_all_possible_stresses(len(syll_nuclei))

  best_stress = max(potential_stresses, key=lambda x: score(word, x, syll_nuclei))
  return zip(syll_nuclei, best_stress)

def score(word, stresses, syll_nuclei):
  global high
  global low

  #print stresses

  word_score = high.score(stresses)
  syll_scores = [score_stress(word, stresses[i], syll_nuclei, i, low) for i in range(len(stresses))]
  #print "word score", word_score
  #print "syll scores", syll_scores
  return pow(word_score, 2) * reduce(lambda x, y: x*y, syll_scores, 1)

def score_stress(word, stress, nuclei, index, low):
  probs = low.prob_classify(get_features(index, nuclei, word))
  #print stress
  #print probs._prob_dict
  return probs.prob(stress)

def run_performance_test():
  all_wordlist = util.read_in(ALL_FILENAME)

  correct_count = 0
  incorrect_count = 0

  for word, stressed in all_wordlist.items():
    actual_stress = util.derive_stress(stressed)
    actual_just_stress = [syll[1] for syll in actual_stress]

    found_stress = pick_stress(word)
    found_just_stress = [syll[1] for syll in found_stress]

    if (actual_just_stress == found_just_stress):
      correct_count += 1
      print "CORRECT"
      print_score(correct_count, incorrect_count)

      print util.print_stress(actual_stress)
      print word
    else:
      incorrect_count += 1
      print "FAILED"
      print_score(correct_count, incorrect_count)

      print "correct stress"
      print util.print_stress(actual_stress)
      print word
      print "found stress"
      print util.print_stress(found_stress)
      print word
    print " "
    sys.stdout.flush() # make piping work correctly

def print_score(cc, icc):
      print("correct", cc, "incorrect", icc)
      percentage = float(cc) / float(cc + icc)
      print percentage


#globals
low = get_low_classifier() #classifier for individual syllables
high = get_high_classifier() #'classifier' for entire stress patterns

#main
import sys
if __name__ == "__main__":
  if (sys.argv > 1):
    if (sys.argv[1] in ["-p", "--performance"]):
      run_performance_test()
    else:
      for word in sys.argv[1:]:
        stresses = pick_stress(word)
        print util.print_stress(stresses)
        print word




#for word, stressed in test_wordlist.items()[:10]:
#  print util.print_stress(get_word_stressed(classifier, word))
#  print word
#  print stressed
#  print ""
