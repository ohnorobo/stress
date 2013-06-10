#!/usr/bin/python

#made as a result of of my being totally unable to hear stress



import string
import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict


# . = unstressed
# / = stressed


# TODO
# dictionary doesn't have contractions (it's, that's)
# most longer words don't work (infintesimally) - find a way to break and measure common morphemes?
# fall back on syllables_en.py when unable to find keys in cmudict?
#   this should also work for nonsense words (fribbled, etc)




d = cmudict.dict()

#count syllables in a single word
def count_sylls(word):
    return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]

#count syllables in a string
def get_n_sylls(line):
    return sum(count_sylls(remove_punct(y))[0] for y in line.strip().split())


def remove_non_ascii(s):
    return "".join(i for i in s if ord(i)<128)

def remove_punct(s):
    return ''.join([i for i in s if i not in string.punctuation])

def get_rep(word):
    return d[word.lower()]


def print_stress(word):
    forms = [list(y for y in x if isdigit(y[-1])) for x in d[word.lower()]]
    #print forms
    stress = [list(pick_stress(syll) for syll in sylls) for sylls in forms]
    #print stress

    print " ".join(stress[0])
    print word

def pick_stress(syll):
    if "2" in syll:
        return "/"
    if "1" in syll:
        return "\\"
    if "0" in syll:
        return "."
    else:
        return "error: " + str(syll)


def get_stress_name(line):
    return ""




print get_n_sylls("eat that!")
#print get_rep("word")
#print get_rep("antidisestablishmentarianism")

#print_stress("antidisestablishmentarianism")
#print_stress("inside")
#print_stress("without")


#stuff
#http://www.onebloke.com/2011/06/counting-syllables-accurately-in-python-on-google-app-engine/
#http://stackoverflow.com/questions/1342000/how-to-replace-non-ascii-characters-in-string
