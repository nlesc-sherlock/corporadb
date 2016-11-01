import logging
import unittest
import os
import gensim
import corpora.buildDict
import nose.tools

logging.basicConfig(level=logging.DEBUG)

class buildDict_tests(unittest.TestCase):

    def test_buildDict(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        inputdir = os.path.join(curdir,"testdata","dict")
        output = os.path.join(curdir,"test.dict")
        corpora.buildDict.generateDictionary(inputdir,output)
        nose.tools.ok_(os.path.exists(output))
        newDic = gensim.corpora.Dictionary.load(output)
        nose.tools.ok_("investment" in newDic.itervalues())
        # TODO: Shouldn't this be filtered out?
        nose.tools.ok_("charset=us-ascii" in newDic.itervalues())
        os.remove(output)
