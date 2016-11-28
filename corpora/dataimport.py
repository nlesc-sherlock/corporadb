import random
import string
import collections
import numpy
from sklearn.metrics import pairwise_distances

letters = string.ascii_lowercase[:12]

def get_random_name(letters, length):
  return ''.join(random.choice(letters) for i in range(length))

class CorporaDataSet:
    def __init__(self, setname):
        self.setname = setname

    def getMetadata(self):
        '''Return the metadata'''
        return '../data/metadata.json'

    def loadVocabulary(self):
        '''Load vocabulary'''
        num_words = 10000
        # create n random words
        randwords = set([get_random_name
                             (letters, random.randint(2,12))
                             for i in range(0,num_words)])
        randwords = [x for x in randwords]
        # create dictionary
        worddict = collections.defaultdict(dict)
        for i in range(0, len(randwords)):
            worddict[randwords[i]] = i
        lenwords = len(randwords)
        randwords = randwords
        return worddict, lenwords, randwords

    def getWordsInTopicMatrix(self, collection, item):
        return self.create_probabilities(collection, item)

    def getDocsInTopicMatrix(self, collection, item):
        return self.create_probabilities(collection, item)

    def create_probabilities(self, collection, item):
        '''
        create probabilities of each word in each topic
        '''
        a = numpy.abs(numpy.random.randn(collection, item))
        row_sums = a.sum(axis=0)
        probabilities = a / row_sums[numpy.newaxis, :]
        return probabilities

    def getTopicDistanceMatrix(self, vector):
        self.find_distance_matrix(vector)

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
