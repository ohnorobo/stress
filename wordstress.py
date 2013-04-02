#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

#little model to learn stress data for words
#and add stress for unknown words

DATA_FILENAME = "data/gcide/gcide-0.51/clean.lower.undup.CIDE"

CHAR_LIST =["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v" "w" "x", "y", "z", "à", "á", "â", "ã", "ä", "æ", "ç", "è", "é", "ê", "î", "ï", "ñ", "ó", "ô", "ö", "ù", "û", "ü", "œ"]

VOWEL_LIST =["a", "e", "i", "o", "u", "à", "á", "â", "ã", "ä", "æ", "è", "é", "ê", "î", "ï","ó", "ô", "ö", "ù", "û", "ü", "œ"]

CONSONANT_LIST =[ "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v" "w" "x", "y", "z", "ç", "ñ"]

#marks for input stress, strong, mid, weak
INPUT_STRESS_MARKS = ["\"", "`", "*"]

#marks for stress. strong, mid, weak
OUTPUT_STRESS_MARKS = ["/", "\\", "-"]





#break down into syllabification and stress?

#break down words into # and index of syllable cores
#   first check that this will work

#then mark syllable cores for intensity

# default

# break down into default : (1, 0) (3, 1)
#                            1= index of stress
#                            0= intensity (0=most, higher=less)
#  / -
# default


#takes a word with stress marking
# ex : ab*al`ien*a"tion    n.
#returns a list of tuples of syllable-core index to stress level
# ex : [(0, 2),(2, 1),(4, 2),(7, 0),(9, 2)]
def derive_stress(word):
    stresses = []

    #single syllable words
    if all(not mark in word for mark in INPUT_STRESS_MARKS):
        word += INPUT_STRESS_MARKS[0]

    #weak final stress
    if all(word[-1] != mark for mark in INPUT_STRESS_MARKS):
        word += INPUT_STRESS_MARKS[-1]

    split = re.split('([\*|\"|`])', word)

    length = 0
    for i in xrange(len(split)/2):
        syll = split[i*2]
        stress_mark = split[i*2 + 1]
        stresses.append((length + find_syllable_core(syll),
                         INPUT_STRESS_MARKS.index(stress_mark)))
        length += len(syll)
    return stresses

    # TODO how to deal with multi-word or hyphenated words
    # missing final stress marks?






# given a syllable (orthographic) give the index of its code
# if the core is multichar give the index of the first
# it's not clear if this is possible, but worth trying
# "ba" => 1
# "ab" => 0
# "this" => 2
# "sprig" => 3
# "thought" => 2
# "rhyme" => 2
# "you" => 1
def find_syllable_core(syll):
    if any(vowel in syll for vowel in VOWEL_LIST):
        return min(filter(lambda x: x!=-1, [syll.find(vowel) for vowel in VOWEL_LIST]))
    elif "y" in syll:
        return syll.index("y")
    elif "r" in syll:
        return syll.index("r")
    #TODO more heuristics? l, w, m, n, etc cores
    else:
        return floor(len(syll)/2)

    # TODO maybe add a mitigating factor to force the core toward
    # the center of a long syllable





#takes a list of stress tuples
# ex : [(0, 2),(2, 1),(4, 2),(7, 0),(9, 2)]
#prints a stress representation
# ex : - \ -  / -
#      abalienation
def print_stress(stresses):
    s = [" "]*(stresses[-1][0] + 1)
    for stress in stresses:
        s[stress[0]] = OUTPUT_STRESS_MARKS[stress[1]]
    return "".join(s)


#remove any instance of " * or `
def unstress(word):
    for stress_mark in INPUT_STRESS_MARKS:
        word = word.replace(stress_mark, "")
    return word


def read_in(filename):
    data = {}
    f = open(filename, "r")

    for line in f:
        l = line.split('\t')
        stressed_word = l[0]
        pos = l[1] #part pf speech

        unstressed_word = unstress(stressed_word)

        #currently ignoring pos, and multiple stresses for different poses
        data[unstressed_word] = stressed_word

    return data




#main
if __name__ == "__main__":
    data = read_in(DATA_FILENAME)

    for word in data.keys():
        stressed_word = data[word]
        stresses = derive_stress(stressed_word)

        print print_stress(stresses)
        print word
        print ""






import unittest

class TestWordStress(unittest.TestCase):

    def test_derive_stress(self):
        self.assertEqual([(0, 2),(2, 1),(4, 2),(7, 0),(9, 2)],
            derive_stress("ab*al`ien*a\"tion"))

    def test_print_stress(self):
        self.assertEqual("- \ -  / -",
            print_stress([(0, 2),(2, 1),(4, 2),(7, 0),(9, 2)]))



