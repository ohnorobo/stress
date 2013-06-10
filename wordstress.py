#!/usr/bin/python
import itertools

### Informal interface: Model
# Models have 2 methods
#   train - takes a set of args,
#           learns about the probability of those args in relation to each other
#   score - takes the same set of args as train,
#           returns the probabilities of the args given what it's learned

# stresses
stress_marks = ["/", "\\", "-"]
GC = "data/gcide/gc/wordlist.2.CIDE" #data

def get_pos():
  pos = []
  f = file("data/gcide/gc/pos.txt")
  for line in f:
    pos.append(line.strip())
  return pos
pos = get_pos() #all parts of speech in data


class CountingDict(dict):
  # a dictionary which allows you to add to ostensible keys
  # cd[key] += 1 adds one, if key doesn't exist it sets cd[key]=1
  # cd.total = returns total count
  def __init__(self):
    self._keys = []
    self.total = 0

  def __getitem__(self, key):
    if key not in self._keys:
      return 0;
    else:
      return dict.__getitem__(self,key)

  def __setitem__(self, key, value):
    if key not in self._keys:
      self._keys.append(key)
      dict.__setitem__(self,key,value)
      #should this be an error?
    else:
      dict.__setitem__(self,key,value)
      self.total += value

  def total(self):
    return self.total



class FullStressModel:

  def __init__(self):
    self.syll_model = SyllStressModel()
    self.word_model = WordStressModel()
    self.pos_model = PartofSpeechStressModel()

  def train(self, word, syll_cores, stresses, pos):
    print "training on ", word, syll_cores, stresses, pos
    self.word_model.train(stresses)
    self.pos_model.train(stresses, pos)
    for syll_core, stress in zip(syll_cores, stresses):
      self.syll_model.train(word, syll_core, stress)

  def score(self, word, syll_cores, stresses, pos=False):
    print word, syll_cores, stresses, pos
    # stuff:
    #   a = score of stress pattern
    #   b = score of each individual stress given its syllable
    #   c = score of stress pattern given pos
    # score = a * bs * c
    score = self.word_model.score(stresses) * \
           reduce(lambda a,b: a*b,
               [self.syll_model.score(word, syll_core, stress)
                 for syll_core, stress in zip(syll_cores, stresses)],
               1)
    print score
    return score

           # self.pos_model.score(stresses, pos) * \

class SyllStressModel:

  def __init__(self):
    # [stress_type -> [character-index -> count]]
    self.counts = dict(zip(stress_marks, list(itertools.repeat(CountingDict(), len(pos)))))
    self.padding = 3 #how many characters we look at to the left/right

  def train(self, word, syll_core, stress):
    print "training on ", word, syll_core, stress
    count = self.counts[stress]

    keys = self._get_keys(word, syll_core)
    for key in keys:
      count[key] += 1

  def _get_keys(self, word, syll_core):
    padded_word = " "*self.padding + word + " "*self.padding

    left = syll_core
    right = syll_core + self.padding*2
    substring = padded_word[left:right]

    return [char+str(i) for i, char in enumerate(substring)]

  def score(self, word, syll_core, stress):
    return 1


class WordStressModel:

  def __init__(self):
    # [stress-seq -> count]
    self.count = CountingDict()
    self.lengths = CountingDict()

  def train(self, stresses):
    print "training on ", stresses
    self.count[frozenset(stresses)] += 1
    self.lengths[len(stresses)] += 1

  def score(self, stresses):
    print stresses
    # return  C(stresses) / C(length of word)
    return self.count[frozenset(stresses)] / self.lengths[len(stresses)]

class PartofSpeechStressModel:

  def __init__(self):
    # [pos -> [stress-seq -> count]]
    self.counts = dict(zip(pos, list(itertools.repeat(CountingDict(), len(pos)))))
    print self.counts

  def train(self, stresses, pos):
    print "training on ", stresses, pos
    count = self.counts[pos]
    count[frozenset(stresses)] += 1

  def score(self, stresses, pos):
    # return P(stresses | pos)
    print stresses, pos
    return self.counts[pos][frozenset(stresses)] / self.counts[pos].total()



import stress as util
def train_all_data():
  global model

  f = file(GC)
  for line in f:
    print line
    word, pos = line.strip().split("\t")
    full_stress = util.derive_stress(word)
    word = util.unstress(word)
    syll_cores = [t[0] for t in full_stress]
    stresses = [stress_marks[t[1]] for t in full_stress]

    print "~~~~~~~~~~~~~~~~~training..."
    print word
    print syll_cores
    print stresses
    print pos

    model.train(word, syll_cores, stresses, pos)


import syllabification as syll
def annotate(word, pos=False):
  global model
  # score for each possible choice of stresses
  # pick best scoring set
  syll_cores = syll.syllabify(word)
  possible_stresses = find_all_possible_stresses(len(syll_cores))
  best = max(possible_stresses, key=lambda possible_stress: model.score(word, possible_stress, pos))
  print best
  print syll_cores

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
      for stress_mark in stress_marks:
        copy = deepcopy(r)
        copy.append(stress_mark)
        solutions.append(copy)
    return solutions

##main
if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    print "usage: ./wordstress.py exampleword"
    exit()
  else:
    model = FullStressModel()
    train_all_data()
    annotation = annotate(sys.argv[1], "n.")
    print annotation

else:
  model = FullStressModel()
  train_all_data()
  #wait


import unittest
class TestWordStress(unittest.TestCase):

  def testCountingDict(self):
    d = CountingDict()

    d["a"] += 1
    self.assertEqual(d["a"], 1)
    d["a"] += 1
    self.assertEqual(d["a"], 2)

    d["b"] += 2
    self.assertEqual(d["b"], 2)

    self.assertEqual("a" in d, True)
    self.assertEqual("c" in d, False)

  def test_find_all_possible_stresses(self):

    self.assertEqual(find_all_possible_stresses(1),
                      [["/"], ["\\"], ["-"]])

    self.assertEqual(find_all_possible_stresses(2),
                      [ ["/", "/"],
                        ["/", "\\"],
                        ["/", "-"],
                        ["\\", "/"],
                        ["\\", "\\"],
                        ["\\", "-"],
                        ["-", "/"],
                        ["-", "\\"],
                        ["-", "-"] ])

    self.assertEqual(len(find_all_possible_stresses(3)), 3**3)
    self.assertEqual(len(find_all_possible_stresses(4)), 3**4)
    self.assertEqual(len(find_all_possible_stresses(5)), 3**5)


