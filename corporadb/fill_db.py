#!/usr/bin/env python

import random
import string
import datetime
import collections
import yaml
import numpy
from sklearn.metrics import pairwise_distances
from dbase import *
from numpy import array as nparray
from numpy import append as npappend
from numpy import ravel as npravel
from dateutil.parser import parse as dateparse
import pytz

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
  def __init__(self, dbname):
    self.create_dummy_data()
    self.connection, self.cursor = connectToDB(dbname)
    self.fill_database()
    commitToDB(self.connection, self.cursor)
    closeDBConnection(self.connection, self.cursor)
    del self.connection, self.cursor

  def create_dummy_data(self):
    self.datasetname = 'sherlock'
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
    self.randwords = randwords

  def create_probabilities(self, collection, item):
    '''
    create probabilities of each word in each topic
    '''
    a = numpy.abs(numpy.random.randn(collection, item))
    row_sums = a.sum(axis=0)
    probabilities = a / row_sums[numpy.newaxis, :]
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

  def insert_into_database(self, table, rows, value):
    row_sql = ', '.join(map(str, rows))
    if len(value) == 1:
      self.cursor.execute("INSERT INTO {} ({}) VALUES ('{}')".format(
                          table, row_sql, value[0]))
    else:
      try:
        self.cursor.execute("INSERT INTO {} ({}) VALUES {}".format(
                            table, row_sql, tuple(value)))
      except Exception:
        self.cursor.execute("INSERT INTO {} ({}) VALUES ".format(
          table, row_sql) + "(" + ",".join("?"*len(value)) +")", tuple(value))
        import pdb; pdb.set_trace()
    return self.cursor.lastrowid


  def fill_database(self):
    # Add new dataset
    self.add_dataset('dataset', nparray(['name']), nparray([self.datasetname]))
    # add lda_settings (only contains number_of_topics for now)
    self.add_lda_settings('lda_settings', nparray(['number_of_topics']),
                          nparray([self.numtopics]))
    self.add_lda('lda', (), ())
    if self.insert:
      # add topics
      topic_ids = self.add_topics()
      self.add_topic_distances(topic_ids)
      self.add_emails(topic_ids)
      word_ids = self.add_words()
      self.add_topic_words(topic_ids, word_ids)

  def check_dataset(self):
    '''
    check if dataset is already in database
    if found set self.dataset_id to the entry in the database
    return boolean
    '''
    self.cursor.execute('select rowid, name from dataset')
    citems = self.cursor.fetchall()
    names = [citem['name'] for citem in citems]  # get all names
    if names:
      try:
        idx = numpy.where(numpy.array(names)==self.datasetname)[0][0]
        self.dataset_id = citems[idx]['rowid']
        return True
      except IndexError:
        return False
    else:
      return False

  def check_lda_settings(self):
    '''
    check if lda_settings is already in database
    if found set self.lda_settings_id to the entry in the database
    return boolean
    '''
    self.cursor.execute('select rowid, number_of_topics from lda_settings')
    citems = self.cursor.fetchall()
    ntopics = [citem['number_of_topics'] for citem in citems]
    try:
      idx = numpy.where(numpy.array(ntopics)==self.numtopics)[0][0]
      self.lda_settings_id = citems[idx]['rowid']
      return True
    except IndexError:
      return False

  def check_lda(self):
    '''
    check if lda is already in database
    if found set self.insert to False, else self.insert=True
    '''
    self.cursor.execute('select rowid, dataset_id, lda_settings_id from lda')
    citems = self.cursor.fetchall()
    found_lda = [True if (citem['lda_settings_id']==self.lda_settings_id and
                          citem['dataset_id']==self.dataset_id)
                 else  False for citem in citems]
    if True in found_lda:
      return False
    else:
      return True

  def add_dataset(self, table, rows, value):
    '''
    check if dataset has already an entry in the database
    if not found insert dataset into database,
    else get dataset_id from database
    '''
    if not self.check_dataset():
      self.dataset_id = self.insert_into_database(table, rows, value)

  def add_lda_settings(self, table, rows, value):
    '''
    Check if lda_settings is already in the database
    if not found insert lda_settings into the database,
    else get lda_settings_id from the database
    '''
    if not self.check_lda_settings():
      self.lda_settings_id = self.insert_into_database(table, rows, value)

  def add_lda(self, table, rows, value):
    '''
    Add lda to lda table
    '''
    self.insert = self.check_lda()
    if self.insert:
      rows = npappend(rows, ('lda_settings_id', 'dataset_id'))
      value = npappend(value, (self.lda_settings_id, self.dataset_id))
      self.lda_id = self.insert_into_database(table, rows, value)

  def add_topics(self):
    '''
    Insert all topics into database
    '''
    for idx in range(0,self.numtopics):
      try:
        topic_ids = npappend(topic_ids, self.add_topic('topic', nparray(['name']), nparray([get_random_name(letters, 5)])))
      except NameError:
        topic_ids = self.add_topic('topic', nparray(['name']), nparray([get_random_name(letters, 5)]))
    return topic_ids

  def add_topic(self, table, rows, value):
    '''
    Add topic to topics table
    '''
    rows = npappend(rows, ('lda_id'))
    value = npappend(value, (self.lda_id))
    return self.insert_into_database(table, rows, value)

  def add_topic_distances(self, topic_ids):
    '''
    Add distances between all topics
    '''
    for idx1, topic in enumerate(topic_ids):
      for idx2, topic2 in enumerate(topic_ids):
        rows = nparray(['topic_id1', 'topic_id2', 'distance'])
        values = nparray([topic, topic2, self.distance_matrix[idx1, idx2]])
        self.add_distance_to_topic('distance', rows, values)

  def add_distance_to_topic(self, table, rows, value):
    '''
    Add topic to topics table
    '''
    rows = npappend(rows, ('lda_id'))
    value = npappend(value, (self.lda_id))
    distance_id = self.insert_into_database(table, rows, value)

  def add_emails(self, topic_ids):
    '''
    add all emails and email_blobs
    '''
    # loop over emails
    for email in range(0, self.num_emails):  # loop over emails
      em = self.metadata[email]
      dtime_orig = dateparse(em['Date'])
      dtime_utc = dtime_orig.astimezone(pytz.utc)
      values = nparray([em['Subject'], em['From'], em['To'], em['Cc'],
                        em['Bcc'], dtime_orig, dtime_utc])
      values = nparray([value.replace("'", " ") if
                        (value and isinstance(value, str)) else value for value in values])
      rows = nparray(['subject', 'sender', 'receiver', 'cc', 'bcc',
                      'send_time', 'send_time_utc'])
      bool = nparray([True if a else False for a in values])
      self.add_email('email', rows[bool], values[bool])
      for idx2, t_id in enumerate(topic_ids):  # loop over topics
        rows = nparray(['topic_id', 'topic_probability'])
        values = nparray([t_id, self.email_prob[idx2, email]])
        self.add_blob('email_blob', rows, values)

  def add_email(self, table, rows, value):
    '''
    Add email to email table
    '''
    rows = npappend(rows, ('dataset_id'))
    value = npappend(value, (self.dataset_id))
    self.email_id = self.insert_into_database(table, rows, value)

  def add_blob(self, table, rows, value):
    '''
    Add blob to blob table
    '''
    rows = npappend(rows, ('email_id', 'lda_id'))
    value = npappend(value, (self.email_id, self.lda_id))
    blob_id = self.insert_into_database(table, rows, value)


  def add_topic_words(self, topic_ids, word_ids):
    '''
    Fill topicwords table
    '''
    for idx1, topicid in enumerate(topic_ids):
      for idx2, wordid in enumerate(word_ids):
        rows = nparray(['topic_id', 'word_id' , 'probability'])
        values = nparray([topicid, wordid, self.wordprob[idx1, idx2]])
        self.add_topic_word('topic_words', rows, values)

  def add_topic_word(self, table, rows, value):
    '''
    Add topicwords to topicwords table
    '''
    topic_words_id = self.insert_into_database(table, rows, value)

  def add_words(self):
    '''
    Add all words to the dictionary table
    '''
    for word in self.randwords:
      rows = nparray(['word'])
      values = nparray([word])
      try:
        word_ids = npappend(word_ids, self.add_dict('dict', rows, values))
      except NameError:
        word_ids = self.add_dict('dict', rows, values)
    return word_ids

  def add_dict(self, table, rows, value):
    '''
    Add topicwords to topicwords table
    '''
    rows = npappend(rows, ('lda_id'))
    value = npappend(value, (self.lda_id))
    return self.insert_into_database(table, rows, value)


if __name__=="__main__":
  fill_db('../data/testdb.db')
