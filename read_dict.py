# -*- coding: utf8 -*-

__date__ = 'January 2016'
__version__ = '2.0'
__author__ = 'Stephan Tulkens, Ben Verhoeven'

from __future__ import division
from __future__ import print_function

import re

from codecs import open
from collections import defaultdict, Counter


class DictFeaturizer(object):

    def __init__(self, path):

        self.dict = {}

        with open(path, "r", encoding='utf-8') as f:
            for line in f:
                line = line.lower().strip().split(",")

                allwords = set(line[1:])
                wildcards_app = set([x[:-1].replace("*", "").replace("+", "") for x in allwords if x[-1] == u'*'])
                pluscards_app = set([x[:-1].replace("*", "").replace("+", "") for x in allwords if x[-1] == u'+'])
                wildcards_pre = set([x[1:].replace("*", "").replace("+", "") for x in allwords if x[0] == u'*'])
                pluscards_pre = set([x[1:].replace("*", "").replace("+", "") for x in allwords if x[0] == u'+'])
                normal = allwords - wildcards_app - pluscards_app - wildcards_pre - pluscards_pre

                regex = []

                if wildcards_app:
                    regex.append(u"({0})".format(u"|".join([u"{0}\w*".format(x) for x in wildcards_app])))
                if pluscards_app:
                    regex.append(u"({0})".format(u"|".join([u"{0}\w+".format(x) for x in pluscards_app])))
                if wildcards_pre:
                    regex.append(u"({0})".format(u"|".join([u"\w*{0}".format(x) for x in wildcards_pre])))
                if pluscards_pre:
                    regex.append(u"({0})".format(u"|".join([u"\w+{0}".format(x) for x in pluscards_pre])))

                if regex:
                    if len(regex) > 1:
                        regex = re.compile(u"|".join(regex))
                    else:
                        regex = re.compile(regex[0])

                self.dict[line[0]] = (normal, regex)

    def featurize(self, text, output='rel'):
        """
        param: text: a tokenized string representation.
        type: text: str
        return: a frequency dictionary for each category in the dictionary.
        type: return: dict
        """

        # decide on relative or absolute frequency
        if output == 'abs':  # absolute frequency as output
            div = 1
        elif output == 'rel':  # relative frequency as output
            div = len(text)
        else:
            return ValueError(u"Wrong frequency specification! Must be 'rel' or 'abs")

        # Make frequency dictionary of the text to diminish number of runs in further for loop
        freq_dict = self.freqdict(text)

        features = dict()

        for key, wordlists in self.dict.items():

            normal, wildcards = wordlists
            freq = 0

            if wildcards:

                for word, count in freq_dict.items():
                    if word in normal:
                        freq += count
                        continue
                    if wildcards.match(word):
                        freq += count
                features[key] = freq / div

            else:

                for word, count in freq_dict.items():
                    if word in normal:
                        freq += count
                        continue
                features[key] = freq / div

        return features

    @staticmethod
    def freqdict(text):
        """This function returns a frequency dictionary of the input list. All wordlist are transformed to lower case."""

        return Counter(text.lower().split())