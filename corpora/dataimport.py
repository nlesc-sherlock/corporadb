import random
import string
import numpy
import gensim
from scipy.io import mmread
from sklearn.metrics import pairwise_distances


letters = string.ascii_lowercase[:12]

def get_random_name(letters, length):
  return ''.join(random.choice(letters) for i in range(length))

class CorporaDataSet:
    def __init__(self, setname):
        self.setname = setname

    def getMetadata(self):
        '''Return the json file containing metadata'''
        return self.setname + '_clean/metadata.json'

    def loadVocabulary(self):
        '''Load vocabulary'''
        id2Word = gensim.corpora.Dictionary.load(self.setname + '.dict')
        id2Word.filter_extremes()
        word2Id = { word:id for id,word in id2Word.iteritems() }
        return word2Id, len(word2Id), word2Id.keys()

    def getWordsInTopicMatrix(self):
        print 'Loading ' + self.setname + '_LDA/wordXtopic.mtx'
        wxt = mmread(self.setname + '_LDA/wordXtopic.mtx')
        return wxt

    def getDocsInTopicMatrix(self):
        print 'Loading ' + self.setname + '_LDA/docXtopic.mtx'
        dxt = mmread(self.setname + '_LDA/docXtopic.mtx')
        return dxt

    def getTopicDistanceMatrix(self, vector):
        return self.find_distance_matrix(vector)

    def find_distance_matrix(self, vector, metric='cosine'):
        '''
        compute distance matrix between topis using cosine or euclidean
        distance (default=cosine distance)
        '''
        if metric == 'cosine':
            distance_matrix = pairwise_distances(vector,
                                                metric='cosine')
            # diagonals should be exactly zero, so remove rounding errors
            numpy.fill_diagonal(distance_matrix, 0)
        if metric == 'euclidean':
            distance_matrix = pairwise_distances(vector,
                                                metric='euclidean')
        return distance_matrix
