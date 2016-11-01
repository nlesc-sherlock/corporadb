from __future__ import print_function
import nltk
import pattern.en as nlp
import re


class Tokenizer(object):

    """ Stores a corpus along with its dictionary. """

    standard_nlp_tags = frozenset([
        # None, u'(', u')', u',', u'.', u'<notranslation>damesbladen', # extras
        # u'CC', # conjunction
        # u'CD', # cardinal (numbers)
        # u'DT', # determiner (de, het)
        u'FW',  # foreign word
        # u'IN', #conjunction
        u'JJ',  # adjectives -- # u'JJR', u'JJS',
        # u'MD', # Modal verb
        u'NN', u'NNP', u'NNPS', u'NNS',  # Nouns
        # u'PRP', # Pronouns -- # u'PRP$',
        u'RB',  # adverb
        u'RP',  # adverb
        # u'SYM', # Symbol
        # u'TO', # infinitival to
        # u'UH', # interjection
        u'VB', u'VBD', u'VBG', u'VBN', u'VBP', u'VBZ',  # Verb forms
    ])
    standard_stopwords = frozenset(
        nltk.corpus.stopwords.words('english') +
        ['', '.', ',', '?', '(', ')', ',', ':', "'",
         u'``', u"''", ';', '-', '!', '%', '&', '...', '=', '>', '<',
         '#', '_', '~', '+', '*', '/', '\\', '[', ']', '|', '|', '{', '}','@',
         u'\u2019', u'\u2018', u'\u2013', u'\u2022',
         u'\u2014', u'\uf02d', u'\u20ac', u'\u2026'])

    def __init__(self, nlp_tags=None, exclude_words=None, filters=[]):
        """
        Parameters
        ----------
        nlp_tags : list or set of str
            Natural language processing codes of word semantics to keep as
            relevant tokens when tokenizing. See Tokenizer.standard_nlp_tags
            for an example
        exclude_words : list or set of str
            Exact words and symbols to filter out.
        filters : list of function (str -> str)
            Filters to filter out raw text, in order.
        """
        if nlp_tags is None:
            self.nlp_tags = Tokenizer.standard_nlp_tags
        else:
            self.nlp_tags = frozenset(nlp_tags)

        if exclude_words is None:
            self.exclude_words = Tokenizer.standard_stopwords
        else:
            self.exclude_words = frozenset(exclude_words)

        self.filters = filters

    def tokenize_file(self, f):
        try:
            return self.tokenize(f.read())
        except AttributeError:
            with open(f, 'rb') as fp:
                return self.tokenize(fp.read())

    def tokenize(self, text):
        """
        Tokenize words in a text and return the relevant ones

        Parameters
        ----------
        text : str
            Text to tokenize.
        """
        for f in self.filters:
            text = f(text)

        words = []
        for s in nlp.split(nlp.parse(text)):
            for word, tag in s.tagged:
                if tag in self.nlp_tags:
                    word = word.lower()
                    if word not in self.exclude_words:
                        words.append(word)

        return words

forward_pattern = re.compile('[\r\n]>[^\r\n]*[\r\n]')
html_patten = re.compile('<[^<]+?>')
mime_pattern = re.compile('=\d\d')
dot_pattern = re.compile('\.\.+')
startdot_pattern = re.compile('\s[.,;?:&!]+(\S)')


def filter_email(text):
    """ Filters reply/forward text, html, mime encodings and dots from emails.
    """
    text = forward_pattern.sub('\n', text)
    text = html_patten.sub(' ', text)
    text = mime_pattern.sub(' ', text)
    text = dot_pattern.sub('. ', text)

    idx = 0
    m = startdot_pattern.search(text, idx)
    while m:
        text = text[:m.start()] + ' ' + m.group(1) + text[m.end():]
        idx = m.end()
        m = startdot_pattern.search(text, idx)

    return text
