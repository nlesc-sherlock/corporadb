import logging
import unittest
import os
import tokenizer
import tokenization
import nose.tools
import tempfile
import cleanHeaders

logging.basicConfig(level=logging.DEBUG)

class tokenization_tests(unittest.TestCase):

    def test_tokenize_str(self):
        s = "...Hello! This is{} a message@, that needs to be tokenized\n, is this the purpose of\tthis test (or not)?"
        t = tokenizer.Tokenizer()
        tokens = t.tokenize(s)
        nose.tools.eq_(tokens,["message","needs","tokenized","purpose","test"])

    def test_tokenize_file(self):
        s = "...Hello! This is{} a message@, that needs to be tokenized..."
        f = tempfile.TemporaryFile(mode="w + b + r")
        f.write(s)
        t = tokenizer.Tokenizer()
        f.seek(0)
        ftokens = t.tokenize_file(f)
        stokens = t.tokenize(s)
        nose.tools.eq_(ftokens,stokens)

    def test_tokenize_mail(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(curdir,"testdata","73.")
        body,mdat = cleanHeaders.extractEmailBody(filepath)
        t = tokenizer.Tokenizer()
        tokens = t.tokenize(body)
        nose.tools.ok_("investment" in tokens)
        nose.tools.ok_("is" not in tokens)
