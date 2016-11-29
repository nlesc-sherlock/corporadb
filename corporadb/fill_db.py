#!/usr/bin/env python

import random
import string
import collections
import json
import numpy
from dbase import connectToDB, closeDBConnection, commitToDB
from numpy import array as nparray
from numpy import append as npappend
from dateutil.parser import parse as dateparse
import pytz
from corpora.dataimport import CorporaDataSet

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
  def __init__(self, DB_NAME=None, DB_HOST=None, DB_PORT=None, USER_NAME=None,
               USER_PASSWORD=None):
    self.connection, self.cursor = connectToDB(DB_NAME, USER_NAME,
                                           USER_PASSWORD, DB_HOST, DB_PORT)
    self.dataset = CorporaDataSet('Random')
    self.create_dummy_data()
    self.fill_database()
    commitToDB(self.connection, self.cursor)
    closeDBConnection(self.connection, self.cursor)
    del self.connection, self.cursor

  def create_dummy_data(self):
    self.datasetname = 'sherlock'
    self.read_metadata_json(self.dataset.getMetadata())
    self.worddict, self.lenwords, self.randwords = self.dataset.loadVocabulary()
    self.numtopics = 10

    # normalized probability matrix, words in a topic
    self.wordprob = self.dataset.getWordsInTopicMatrix(self.numtopics, self.lenwords)
    # normalized probability matrix, emails in a topic
    self.num_emails = len(self.metadata)
    self.email_prob = self.dataset.getDocsInTopicMatrix(self.numtopics, self.num_emails)
    # distance matrix between topics
    self.distance_matrix = self.dataset.getTopicDistanceMatrix(self.wordprob)

  def read_metadata_json(self, filename):
    '''
    read metadata from json filename
    '''
    with open(filename, 'r') as f:
      data = f.read()
      self.metadata = json.loads(data.decode('cp1252'))


  def insert_into_database(self, table, rows, value):
    row_sql = ', '.join(map(str, rows))
    parameters = '(' + ','.join(['%s' for i in value]) + ')'
    #value = [x.text if isinstance(
    #         x, lxml.objectify.StringElement) else x for x in value]
    value = nparray(value)
    sql = """INSERT INTO {} ({}) VALUES {} RETURNING id
          """.format(table, row_sql, parameters)
    try:
      self.cursor.execute(sql, tuple(value))
      return self.cursor.fetchone()[0] # return last insert id
    except psycopg2.IntegrityError:
      self.connection.rollback()
    except psycopg2.ProgrammingError:
      self.connection.rollback()

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
    self.cursor.execute('select id as rowid, name from dataset')
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
    self.cursor.execute('select id as rowid, number_of_topics from lda_settings')
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
    self.cursor.execute('select id as rowid, dataset_id, lda_settings_id from lda')
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
  fill_db('sherlock', None, None, 'sherlock', 'sherlock')
