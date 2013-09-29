Usage


###classifier.py

In progress. Does stress classification on a list of input words.

Example:

    ./classifier.py twas brillig and the slithy toves

     /
    twas
      /  -
    brillig
    /
    and
      /
    the
      /  -
    slithy
     / -
    toves

###syllabification.py

####command line

run a full suite of performance tests

    ./syllabification.py -p or --performance

return an output with syllable nuclei marked

    ./syllabification example
    * *   *
    example

####import

    import syllabification as s

return divided syllables, [62% accuracy]

    s.syllabify("example")
    ["ex", "am", "ple"]

return an array of syllable cores, [88% accuracy]

    s.get_nuclei("example")
    [0, 2, 6]
