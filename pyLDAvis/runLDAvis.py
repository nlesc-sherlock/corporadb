#!/usr/bin/env ipython

import numpy
import pyLDAvis
import argparse
from corpora.dataimport import CorporaDataSet
from scipy.io import mmread

topic_word_key = "topic_term_dists"
topic_doc_key = "doc_topic_dists"
doc_length_key = "doc_lengths"
vocabulary_key = "vocab"
word_freq_key = "term_frequency"

def get_data(setname):
    dataset = CorporaDataSet(setname)
#    topic_word_array = dataset.getWordsInTopicMatrix()
#    topic_doc_array = dataset.getDocsInTopicMatrix()
    topic_word_array = dataset.getDocsInTopicMatrix()
    topic_doc_array = dataset.getWordsInTopicMatrix().T
    doc_length_array = numpy.full([topic_doc_array.shape[0]],1)
    vocabulary = dataset.loadVocabulary()[0].keys()
    print "topic word array shape: ",topic_word_array.shape
    print "topic doc shape: ",topic_doc_array.shape
    print "vocabulary: ",len(vocabulary)
    wordfreqs = mmread(setname + ".mtx").sum(1)
    word_freq_array = numpy.array(wordfreqs)[:,0]

    return {topic_word_key:topic_word_array,
            topic_doc_key:topic_doc_array,
            doc_length_key:doc_length_array,
            vocabulary_key:vocabulary,
            word_freq_key:word_freq_array}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Display LDA topic data")
    parser.add_argument("prefix")
    args = parser.parse_args()
    modeldata = get_data(args.prefix)
    movies_vis_data = pyLDAvis.prepare(**modeldata)
    pyLDAvis.show(movies_vis_data)
