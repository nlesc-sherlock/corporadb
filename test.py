from corpora.dataimport import CorporaDataSet
import numpy as np
import json

# dataset = CorporaDataSet('data/spark/data/enron_mail_translated_en')
dataset = CorporaDataSet('data/enron_mail_small')


numTopics = 25

print 'Loading metadata...'
try:
    filename = dataset.getMetadata()
    with open(filename, 'r') as f:
        data = f.read()
        metadata = json.loads(data.decode('cp1252'))
        numEmails = len(metadata)
except:
    print "Problems loading metadata file..."
print '  Number of emails',numEmails

print 'Loading vocabulary...'
worddict, numWords, randwords = dataset.loadVocabulary()

assert len(worddict)==numWords, 'Number of words in vocab do not match!'
assert len(randwords)==numWords, 'Number of random in vocab do not match!'
assert sorted(worddict.keys()) == sorted(randwords), 'Words in vocabulary do not match!'
print '  Number of words',numWords

print 'Loading WordsxTopics...'
# normalized probability matrix, words in a topic
wordprob = dataset.getWordsInTopicMatrix()
print '1) Loaded  : ',wordprob.shape
print '1) Expected: ',(numTopics, numWords)
assert wordprob.shape == (numTopics, numWords), 'WordsxTopics matrix shape missmatch'
for s in wordprob.sum(axis=0):
    np.testing.assert_almost_equal(s, 1.0, 6, 'WordsxTopics - does not add to 1!')

print 'Loading DocxTopics...'
# normalized probability matrix, emails in a topic
email_prob = dataset.getDocsInTopicMatrix()
print '2) Loaded  : ',email_prob.shape
print '2) Expected: ',(numTopics, numEmails)
assert email_prob.shape == (numTopics, numEmails), 'DocxTopics matrix shape missmatch'
# Cannot guarantee every document adds up to 1
# for s in email_prob.sum(axis=0):
#     np.testing.assert_almost_equal(s, 1.0, 6, 'DocxTopics - does not add to 1!')

print 'Loading distances...'
# distance matrix between topics
distance_matrix = dataset.getTopicDistanceMatrix(wordprob)
assert distance_matrix.shape == (numTopics, numTopics), 'Distance matrix shape missmatch'
for e in distance_matrix.diagonal():
    np.testing.assert_almost_equal(e, 0.0, 6, 'DistanceMatris - diagonal element not 0!')
