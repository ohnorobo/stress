#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
import math, sys
from timeout import timeout

SMOOTHING = -1000
ALL_DATA_FILENAME = "data/gcide/gc/wordlist.2.CIDE"
TRAIN_FILENAME = "data/gcide/gc/train"
TEST_FILENAME = "data/gcide/gc/test"


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

    @timeout(15)
    def syllabify(self, word):
        possible_syllabifications = self._all_possible_substrings(word)

        #for ps in possible_syllabifications:
        #    pprint((ps, self.score(ps)))

        return max(possible_syllabifications, key=lambda x: self.score(x))


    def score(self, sylls):
        return sum([self._syll_score(syll) for syll in sylls]) * len(sylls)
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
        s = filter(lambda a: a not in stress.INPUT_STRESS_MARKS and not a=='', s)
        return s

def find_all_syll_nuclei(sylls):
    """
    ENGLISH SPECIFIC
    Arguments:
        sylls- list of substrings
    Returns:
        a list of integers reprsenting the indexes of the nuclei
        of the syllables in the word
    syllable cores are an approximate calculation
    """
    cores = []

    for i in xrange(len(sylls)):
        syll = sylls[i]
        prev_sylls = sylls[:i]
        len_prev_sylls = sum(map(len, prev_sylls))

        index_syll_core = stress.find_syllable_core(syll)

        index = len_prev_sylls + index_syll_core
        cores.append(index)

    return cores



def score_accuracy(inputs, correct_outputs, f):
    correct = 0
    incorrect = 0
    correct_nuc = 0
    incorrect_nuc = 0

    for input, c_output in zip(inputs, correct_outputs):
        print "new: ", input

        #try:
        output = f(input)
        if output != c_output:
            incorrect += 1
            print "incorrect: ", (output, c_output)

            nuc_output = find_all_syll_nuclei(output)
            nuc_correct_output = find_all_syll_nuclei(c_output)
            print nuc_output, nuc_correct_output
            if nuc_output == nuc_correct_output:
                correct_nuc += 1
                print "but correct nuclei"
            else:
                incorrect_nuc += 1
                print "also incorrect nuclei"
        else:
            correct += 1
            correct_nuc += 1
            print "correct: ", (output, c_output)

        print "correct: ", correct
        print "incorrect: ", incorrect
        print "percent correct: ", (1.0*correct)/(correct+incorrect)
        print "~~~"
        print "correct_nuc: ", correct_nuc
        print "incorrect_nuc: ", incorrect_nuc
        print "percent correct_nuc: ", (1.0*correct_nuc)/(correct_nuc+incorrect_nuc)
        print "~~~"

        #except Exception:
        #    print "TIMEOUT"

        # to make piping work correctly
        sys.stdout.flush()



import stress, re
def run_tests():
    #train
    data = stress.read_in(TRAIN_FILENAME)
    s = syll_model()

    for word, stressed in data.items():
        sylls = s.split_sylls(stressed)
        s.train(word, sylls)

    pprint( s.syll_counts )


    #test
    data = stress.read_in(TEST_FILENAME)

    words = data.keys()
    stressed = data.values()
    all_sylls = map(s.split_sylls, stressed)
    score_accuracy(words, all_sylls, s.syllabify)


def syllabify(word):
    pass
def get_nuclei(word):
    pass

def load_data():
    data = stress.read_in(ALL_DATA_FILENAME)
    s = syll_model()

    for word, stressed in data.items():
        sylls = s.split_sylls(stressed)
        s.train(word, sylls)

    return s

def print_visual(word, cores):
    stress = " "*len(word)

    for i in cores:
        stress = stress[:i] + "*" + stress[i+1:]

    print stress
    print word


#####main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """
    usage:
        ./syllabification -p or --performance
        run a full suite of performance tests

        ./syllabification example
        returns an output with syllable nuclei marked
        * *   *
        example

        import syllabification as s (in another program)
        s.syllabify("example")
        returns divided syllables
        ["ex", "am", "ple"]

        s.get_nuclei("example")
        returns an array of syllable cores
        [0, 2, 6]
    """

    elif sys.argv[1] in ["--performance", "-p"]:
        run_tests()
    else:
        s = load_data()
        word = sys.argv[1]
        cores = find_all_syll_nuclei(s.syllabify(word))
        print_visual(word, cores)
    exit()
else:
    s = load_data()
    syllabify = s.syllabify
    get_nuclei = lambda x:(find_all_syll_nuclei(s.syllabify(x)))


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

        self.assertEqual(["de", "vour"], s.split_sylls('de*vour"'))

    def test_find_syll_nuclei(self):
        self.assertEqual([0, 4, 6, 10],
                         find_all_syll_nuclei(['arch', 'i', 'man', 'drite'],))
