import logging
import unittest
import os
import corpora.tokenizer
import corpora.tokenization
import nose.tools
import tempfile
import corpora.cleanHeaders

logging.basicConfig(level=logging.DEBUG)

class tokenization_tests(unittest.TestCase):

    def test_tokenize_str(self):
        s = "...Hello! This is{} a message@, that needs to be tokenized\n, is this the purpose of\tthis test (or not)?"
        t = corpora.tokenizer.Tokenizer()
        tokens = t.tokenize(s)
        nose.tools.eq_(tokens,["message","needs","tokenized","purpose","test"])

    def test_tokenize_file(self):
        s = "...Hello! This is{} a message@, that needs to be tokenized..."
        f = tempfile.TemporaryFile(mode="w + b + r")
        f.write(s)
        t = corpora.tokenizer.Tokenizer()
        f.seek(0)
        ftokens = t.tokenize_file(f)
        stokens = t.tokenize(s)
        nose.tools.eq_(ftokens,stokens)

    def test_tokenize_mail(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(curdir,"testdata","input","73.")
        body,mdat = corpora.cleanHeaders.extractEmailBody(filepath)
        t = corpora.tokenizer.Tokenizer()
        tokens = t.tokenize(body)
        nose.tools.ok_("investment" in tokens)
        nose.tools.ok_("is" not in tokens)

    def test_doTokenization(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        inputdir = os.path.join(curdir,"testdata","input")
        outputdir = os.path.join(curdir,"tokens","input")
        corpora.tokenization.doTokenization(inputdir,outputdir)
        filepath = os.path.join(outputdir,"73.")
        nose.tools.ok_(os.path.exists(filepath))
        tokens = []
        with open(filepath) as f:
            tokens = [s[:-1] for s  in f.readlines()] # Strip EOL characters
        os.remove(filepath)
        os.rmdir(outputdir)
        os.rmdir(os.path.join(curdir,"tokens"))
        nose.tools.ok_("investment" in tokens)
        nose.tools.ok_("is" not in tokens)
