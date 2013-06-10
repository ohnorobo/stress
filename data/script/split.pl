#!/usr/bin/perl

# creates two split files from a larger file
# one containing 90% of the lines, one containing the other 10%
# takes three filenames
# ex:
# ./split.pl myfile.txt train.txt test.txt

open (CONTENT, $ARGV[0]);

open (TRAIN, '>', $ARGV[1]);
open (TEST, '>', $ARGV[2]);

while (<CONTENT>){
    chomp;
    if (rand() < .9) {
        print TRAIN "$_\n";
    }else{
        print TEST "$_\n";
    }
}

close (TRAIN); 
close (TEST); 
close (CONTENT);

