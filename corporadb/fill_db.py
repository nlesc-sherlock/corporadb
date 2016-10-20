#!/usr/bin/env python

import random
import string
import datetime
import collections

domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12]

def get_random_domain(domains):
  return random.choice(domains)

def get_random_name(letters, length):
  return ''.join(random.choice(letters) for i in range(length))

def generate_random_emails(nb, length):
  return [get_random_name(letters, length) + '@' + get_random_domain(domains) for i in range(nb)]

def get_random_sentence():
  nouns = ("puppy", "car", "rabbit", "girl", "monkey")
  verbs = ("runs", "hits", "jumps", "drives", "barfs") 
  adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
  adj = ("adorable", "clueless", "dirty", "odd", "stupid")
  l=[nouns,verbs,adj,adv]
  return ' '.join([random.choice(i) for i in l])

def create_dict(lst,keys):
  ddict = collections.defaultdict(dict)
  for num in range(0,len(lst[0])):
    for idx,name in enumerate(keys):
      ddict[num][name] = lst[idx][num]
  return ddict

class fill_db:

  def __init__(self):
    self.create_dummy_metadata_dict(7)
    import pdb; pdb.set_trace()

  def read_avro_files(self):
    pass

  def create_numpy_array(self):
    pass

  def create_dummy_metadata_dict(self, num_emails):
    sender = generate_random_emails(num_emails, random.randint(6,12))
    receiver = generate_random_emails(num_emails, random.randint(6,12))
    cc = generate_random_emails(num_emails, random.randint(6,12))
    bcc = generate_random_emails(num_emails, random.randint(6,12))
    subject = [get_random_sentence() for i in range(num_emails)]
    # generate random email datetime
    start_date = datetime.date.today().replace(day=1, month=1).toordinal()
    end_date = datetime.date.today().toordinal()
    email_time = [datetime.datetime.fromordinal(random.randint(start_date, end_date)) for i in range(num_emails)]
    self.metadict = create_dict([sender, receiver, cc, bcc, subject, 
                                 email_time], ['sender', 'receiver', 'cc',
                                               'bcc', 'subject', 'email_time'])


  def write_to_database(self):
    pass

  def save_database(self):
    pass

  def open_database(self):
    pass
  
if __name__=="__main__":
  fill_db()
