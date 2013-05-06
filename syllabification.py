#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
import math

SMOOTHING = -1000
DATA_FILENAME = "data/gcide/gc/wordlist.2.CIDE"


##TODO
# properly strip data
# remove multi/hyphenated words


from operator import mul
def product(list):
    reduce(mul, list, 1)

#unused?? TODO
def nCr(n,r):
    # with replacement
    n = n+r-1
    f = math.factorial
    return f(n) / f(r) / f(n-r)


class syll_model:
    """given a word be able to split it into syllables"""

    #Noisy channel model

    def __init__(self):
        self.syll_counts = {} #len => {syll => count}
        self.total_count = {} #len => count


    def train(self, word, sylls):
        """
        given a word and its correct syllabification learn how to syllabify things

        Args:
            word- string
            sylls- a lit of substrings
        """
        for syll in sylls:

            l = len(syll)

            if not l in self.syll_counts:
                self.syll_counts[l] = {}
                self.total_count[l] = 0

            if syll in self.syll_counts[l]:
                #print "adding", syll, self.syll_counts[l][syll]
                self.syll_counts[l][syll] += 1
            else:
                self.syll_counts[l][syll] = 1

            self.total_count[l] += 1

    def syllabify(self, word):
        possible_syllabifications = self._all_possible_substrings(word)

        #for ps in possible_syllabifications:
        #    pprint((ps, self.score(ps)))

        return max(possible_syllabifications, key=lambda x: self.score(x))


    def score(self, sylls):
        return sum([self._syll_score(syll) for syll in sylls]) / len(sylls)
        #divide by len so words with fewer sylls aren't penalized


    def _syll_score(self, syll):
        if len(syll) in self.syll_counts and syll in self.syll_counts[len(syll)]:
            #print (1.0 * self.syll_counts[len(syll)][syll])
            #print  sum(self.total_count.values())
            #print  (1.0 * self.syll_counts[len(syll)][syll]) / sum(self.total_count.values())

            count = self.syll_counts[len(syll)][syll]
            total = sum(self.total_count.values())
            space_size = 26^len(syll)

            return math.log( (1.0 * count * space_size) / total )
        else:
            return SMOOTHING


    def _all_possible_substrings(self, word):
        """ given a string return all substring sequences that make up the whole string

        "abc" = [ ["a", "bc"],
                  ["a", "b", "c"]
                  ["ab", "c"],
                  ["abc"] ]

        """
        if len(word) == 0:
            return [[]]

        else:
            substrings = []

            for index in xrange(len(word)):
                left = word[:index+1]
                right = word[index+1:]

                r_all = self._all_possible_substrings(right)

                for r in r_all:
                    substrings.append( [left] + r )

            return substrings


    def split_sylls(self, word):
        """ takes a word with stress marking: 'ab*al`ien*a"tion'
            returns the divided sylls: ['ab' 'al' 'ien' 'a' 'tion']
        """

        s = re.split('([\*|\"|`])', word)
        s = filter(lambda a: a not in wordstress.INPUT_STRESS_MARKS, s)
        return s




def score_accuracy(inputs, correct_outputs, f):
    correct = 0
    incorrect = 0
    correct_ex = []
    incorrect_ex = []

    for input, c_output in zip(inputs, correct_outputs):
        print "new: ", input

        output = f(input)
        if output != c_output:
            incorrect += 1
            incorrect_ex.append((output, c_output))
            print "incorrect: ", (output, c_output)
        else:
            correct += 1
            correct_ex.append((output, c_output))
            print "correct: ", (output, c_output)

        print "correct: ", correct
        print "incorrect: ", incorrect
        print "percent correct: ", (1.0*correct)/(correct+incorrect)



#####main
import wordstress, re

data = wordstress.read_in(DATA_FILENAME)
s = syll_model()

for word, stressed in data.items():
    sylls = s.split_sylls(stressed)
    s.train(word, sylls)

pprint( s.syll_counts )

#for word, stressed in data.items()[:100]:
#    print stressed
#    print s.syllabify(word)

#words, stressed = data.items()
words = data.keys()
stressed = data.values()
all_sylls = map(lambda w: s.split_sylls(w), stressed)
score_accuracy(words, all_sylls, s.syllabify)






import unittest
class TestSyllabification(unittest.TestCase):

    def test_all_possible_substrings(self):
        s = syll_model()

        sub = s._all_possible_substrings("a")
        self.assertEqual(sub, [["a"]])

        sub = s._all_possible_substrings("ab")
        self.assertEqual(sub, [["a", "b"], ["ab"]])

        sub = s._all_possible_substrings("abc")
        self.assertEqual(sub, [['a', 'b', 'c'], ['a', 'bc'], ['ab', 'c'], ['abc']])

    def test_split_sylls(self):
        s = syll_model()

        self.assertEqual(['ab', 'al', 'ien', 'a', 'tion'],
                         s.split_sylls('ab*al`ien*a"tion'))
