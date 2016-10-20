import logging
import unittest
import os
import cleanHeaders
import nose.tools

logging.basicConfig(level=logging.DEBUG)

class cleanHeaders_tests(unittest.TestCase):

    def test_removeQuotedText1(self):
        text="Please stop bothering me.\nGoodbye.\n-----Original Message:\nLeave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.")

    def test_removeQuotedText2(self):
        text="Please stop bothering me.\nGoodbye.\n-----Original message:\nLeave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.")

    def test_removeQuotedText3(self):
        text="Please stop bothering me.\nGoodbye.\n--Original message:\nLeave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.")

    def test_removeQuotedText4(self):
        text="Please stop bothering me.\nGoodbye.\nPietje wrote:\n>Leave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.")

    def test_removeQuotedText4(self):
        text="Please stop bothering me.\nGoodbye.\n--- Forwarded by Pietje:\n>Leave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.")

    def test_ExtractEmailBody(self):
        curdir=os.path.abspath(os.path.dirname(__file__))
        filepath=os.path.join(curdir,"testdata","73.")
        body,mdat=cleanHeaders.extractEmailBody(filepath)
        nose.tools.ok_(body.startswith("Phillip,"))
        nose.tools.eq_(mdat["From"],"jwills3@swbell.net")

    def test_removeQuotedText6(self):
        curdir=os.path.abspath(os.path.dirname(__file__))
        filepath=os.path.join(curdir,"testdata","73.")
        body,mdat=cleanHeaders.extractEmailBody(filepath)
        cleantext=cleanHeaders.removeOriginalQuote(body)
        print cleantext
        nose.tools.ok_(cleantext.endswith("Jim Wills"))

    def test_preProcess(self):
        curdir=os.path.abspath(os.path.dirname(__file__))
        inputpath=os.path.join(curdir,"testdata")
        outputpath=os.path.join(curdir,"output")
        cleanHeaders.preProcess(inputpath,outputpath)
        nose.tools.ok_(os.path.exists(os.path.join(outputpath,"metadata.json")))
        nose.tools.ok_(os.path.exists(os.path.join(outputpath,"73.")))
        for f in os.listdir(outputpath):
            os.remove(os.path.join(outputpath,f))
        os.rmdir(outputpath)
