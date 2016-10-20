#!/usr/bin/env python

import random
import string
import datetime
import collections
import yaml
import numpy
from sklearn.metrics import pairwise_distances


letters = string.ascii_lowercase[:12]

def get_random_name(letters, length):
  return ''.join(random.choice(letters) for i in range(length))



def create_dict(lst,keys):
  ddict = collections.defaultdict(dict)
  for num in range(0,len(lst[0])):
    for idx,name in enumerate(keys):
      ddict[num][name] = lst[idx][num]
  return ddict

class fill_db:

  def __init__(self):
    self.create_dummy_data()


  def create_dummy_data(self):
    self.read_metadata_json('../data/metadata.json')
    self.create_random_words(10000)
    self.numtopics = 10
    # normalized probability matrix, words in a topic
    self.wordprob = self.create_probabilities(self.numtopics, self.lenwords)
    # normalized probability matrix, emails in a topic
    self.num_emails = len(self.metadata)
    self.email_prob = self.create_probabilities(self.numtopics, self.num_emails)
    # distance matrix between topics
    self.find_distance_matrix(self.wordprob)
    import pdb; pdb.set_trace()

  def read_metadata_json(self, filename):
    '''
    read metadata from json filename
    '''
    with open(filename, 'r') as f:
      self.metadata = yaml.load(f)


  def create_random_words(self, num_words):
    '''
    create a random list of words
    '''
    # create n random words
    randwords = set([get_random_name
                         (letters, random.randint(2,12))
                         for i in range(0,num_words)])
    randwords = [x for x in randwords]
    # create dictionary
    self.worddict = collections.defaultdict(dict)
    for i in range(0, len(randwords)):
      self.worddict[randwords[i]] = i
    self.lenwords = len(randwords)


  def create_probabilities(self, collection, item):
    '''
    create probabilities of each word in each topic
    '''
    a = numpy.random.randn(collection, item)
    row_sums = a.sum(axis=1)
    probabilities = a / row_sums[:, numpy.newaxis]
    return probabilities


  def find_distance_matrix(self, vector, metric='cosine'):
    '''
    compute distance matrix between topis using cosine or euclidean
    distance (default=cosine distance)
    '''
    if metric == 'cosine':
      self.distance_matrix = pairwise_distances(vector,
                                                metric='cosine')
      # diagonals should be exactly zero, so remove rounding errors
      numpy.fill_diagonal(self.distance_matrix, 0)
    if metric == 'euclidean':
      self.distance_matrix = pairwise_distances(vector,
                                                metric='euclidean')


if __name__=="__main__":
  fill_db()
