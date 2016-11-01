import logging
import unittest
import os
import nose.tools
import corpora.buildDict
from corpora.buildDocumentMatrix import buildMatrix

logging.basicConfig(level=logging.DEBUG)

class buildDocumentMatrix_tests(unittest.TestCase):

    def test_buildMatrix(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        inputdir = os.path.join(curdir,"testdata","dict")
        dictfile = os.path.join(curdir,"test.dict")
        outputfile = os.path.join(curdir,"test_matrix")
        corpora.buildDict.generateDictionary(inputdir,dictfile)
        buildMatrix(dictfile,os.path.join(curdir,"testdata","input"),outputfile)
        nose.tools.ok_(os.path.exists(outputfile + ".mtx"))
        os.remove(dictfile)
        os.remove(outputfile + ".mtx")
