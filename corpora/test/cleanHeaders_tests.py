import logging
import unittest
import cleanHeaders
import nose.tools

logging.basicConfig(level=logging.DEBUG)

class cleanHeaders_tests(unittest.TestCase):

    def test_removeQuotedText(self):
        text="Please stop bothering me.\nGoodbye.\n-----Original Message:\nLeave me alone."
        cleantext=cleanHeaders.removeOriginalQuote(text)
        nose.tools.eq_(cleantext,"Please stop bothering me.\nGoodbye.\n")
