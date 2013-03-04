#!/usr/bin/python


import stress
import unittest

class TestStressFunctions(unittest.TestCase):


    #the interesting problem here is that you actually want to check stress and count feet simultaniously, not do stress/syllables on their own. Since often the stress/feet have an extra syllable/pause (causura) floating around which is going to mess up counts, but which could be heuristically ignored if they're calculated together



    # stress tests

    # pyrric    =  ..
    # iambic    =  ./
    # trochaic  =  /.
    # spondaic  =  //

    # tribraich   =  ...
    # dactlic     =  /..
    # amphibrach  =  ./.
    # anapestic   =  ../
    # bacchic     =  .//
    # antibacchic =  //.
    # cretic      =  /./
    # molossus    =  ///

    # ionic       =  ..//
        # "as it slowly, as it sadly"
    # choriamb    =  /../

    '''
    def test_iambic_word(self):
        self.assertEqual("iambic", stress.get_stress_name("behold"))
        self.assertEqual("iambic", stress.get_stress_name("inscribe"))
        self.assertEqual("iambic", stress.get_stress_name("amuse"))

    def test_trochaic_word(self):
        self.assertEqual("trochaic", stress.get_stress_name("slacker"))
        self.assertEqual("trochaic", stress.get_stress_name("dental"))
        self.assertEqual("trochaic", stress.get_stress_name("chosen"))

    def test_spondaic_word(self):
        self.assertEqual("spondaic", stress.get_stress_name("breakdown"))
        self.assertEqual("spondaic", stress.get_stress_name("bathrobe"))
        self.assertEqual("spondaic", stress.get_stress_name("football"))

    #tribrach

    def test_dactylic_word(self):
        self.assertEqual("dactylic", stress.get_stress_name("changeable"))
        self.assertEqual("dactylic", stress.get_stress_name("buffalo"))
        self.assertEqual("dactylic", stress.get_stress_name("glycerin"))

    def test_amphibrach_word(self):
        self.assertEqual("amphibrach", stress.get_stress_name("changeable"))

    def test_anapestic_word(self):
        self.assertEqual("anapestic", stress.get_stress_name("understand"))
        self.assertEqual("anapestic", stress.get_stress_name("anapest"))
        self.assertEqual("anapestic", stress.get_stress_name("contradict"))

    #bacchic

    #antibacchic

    #cretic

    #molossus


    ###################

    #no line test for pyrric

    def test_iambic_line(self):
        text = "Soft, what light through yonder window breaks?"
        self.assertEqual("iambic", stress.get_stress_name(text))

    def test_trochaic_line(self):
        text = "Once upon a midnight dreary, while I pondered weak and weary,"
        self.assertEqual("trochaic", stress.get_stress_name(text))

    #spondaic

    #no line test for tribrach

    def test_dactylic_line(self):
        text = "Just for a handful of silver he left us"
        self.assertEqual("dactylic", stress.get_stress_name(text))

    def test_amphibrach_line(self):
        text = "No former performer's performed this performance!"
        self.assertEqual("amphibrach", stress.get_stress_name(text))

        text = "It's four in the morning, the end of December"
        self.assertEqual("amphibrach", stress.get_stress_name(text))

    def test_anapestic_line(self):
        text = "In the blink of an eye"
        self.assertEqual("anapestic", stress.get_stress_name(text))

    def test_bacchic_line(self):
        text = "When day breaks the fish bite at small flies."
        self.assertEqual("bacchic", stress.get_stress_name(text))

    def test_antibacchic_line(self):
        text = "Blind luck is loved more than hard thinking."
        self.assertEqual("antibacchic", stress.get_stress_name(text))

    def test_cretic_line(self):
        text = "Shall I die? Shall I fly?"
        self.assertEqual("cretic", stress.get_stress_name(text))

    def test_molossus_line(self):
        text = "Awaiting the sensation of a short, sharp shock"
        self.assertEqual("molossus", stress.get_stress_name(text))
    '''


    # feet tests
    # Monometer   One Foot
    # Dimeter Two Feet
    # Trimeter    Three Feet
    # Tetrameter  Four Feet
    # Pentameter  Five Feet
    # Hexameter   Six Feet
    # Heptameter  Seven Feet
    # Octameter   Eight Feet




    #syllable counting (not feet)

    def test_one(self):
        text = "that"
        self.assertEqual(1, stress.get_n_sylls(text))

    def test_two(self):
        text = "that is"
        self.assertEqual(2, stress.get_n_sylls(text))
        text = "inside"
        self.assertEqual(2, stress.get_n_sylls(text))

    def test_three(self):
        text = "what is it"
        self.assertEqual(3, stress.get_n_sylls(text))
        text = "example"
        self.assertEqual(3, stress.get_n_sylls(text))

    def test_four(self):
        text = "which witch is which?"
        self.assertEqual(4, stress.get_n_sylls(text))
        text = "therefore I am"
        self.assertEqual(4, stress.get_n_sylls(text))
        text = "indecisive"
        self.assertEqual(4, stress.get_n_sylls(text))

    def test_five(self):
        text = "if that's what you want"
        self.assertEqual(5, stress.get_n_sylls(text))
        text = "as in the English"
        self.assertEqual(5, stress.get_n_sylls(text))
        text = "automatically"
        self.assertEqual(5, stress.get_n_sylls(text))

    def test_six(self):
        text = "If the world was crazy"
        self.assertEqual(6, stress.get_n_sylls(text))
        text = "unfortunate actions"
        self.assertEqual(6, stress.get_n_sylls(text))
        text = "verisimilitude"
        self.assertEqual(6, stress.get_n_sylls(text))

    def test_seven(self):
        text = "all things wise and wonderful"
        self.assertEqual(7, stress.get_n_sylls(text))
        text = "infinitesimally"
        self.assertEqual(7, stress.get_n_sylls(text))

    def test_eight(self):
        text = "less than ideal circumstances"
        self.assertEqual(8, stress.get_n_sylls(text))
        text = "interdisciplinarity"
        self.assertEqual(8, stress.get_n_sylls(text))

if __name__ == '__main__':
    unittest.main()


#http://web.cn.edu/kwheeler/documents/Examples%20of%20Iambs.pdf
#https://en.wikipedia.org/wiki/Foot_(prosody)
