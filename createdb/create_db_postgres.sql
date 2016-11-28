CREATE TABLE IF NOT EXISTS lda_settings (
  id SERIAL PRIMARY KEY,
  number_of_topics SERIAL
);

CREATE TABLE IF NOT EXISTS dataset (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS lda (
  id SERIAL PRIMARY KEY,
  lda_settings_id SERIAL REFERENCES lda_settings(id),
  dataset_id SERIAL REFERENCES dataset(id)
);

CREATE TABLE IF NOT EXISTS email (
  id SERIAL PRIMARY KEY,
  subject TEXT,
  sender TEXT,
  receiver TEXT,
  cc TEXT,
  bcc TEXT,
  email_txt TEXT,
  send_time TIMESTAMP,
  dataset_id INTEGER NOT NULL REFERENCES dataset(id)
);

CREATE TABLE IF NOT EXISTS topic (
  id SERIAL PRIMARY KEY,
  lda_id SERIAL REFERENCES lda(id),
  name TEXT
);

CREATE TABLE IF NOT EXISTS email_blob (
  email_id INTEGER NOT NULL REFERENCES email(id),
  topic_probability REAL NOT NULL,
  topic_id SERIAL REFERENCES topic(id),
  lda_id SERIAL REFERENCES lda(id)
);

CREATE TABLE IF NOT EXISTS distance (
  lda_id SERIAL REFERENCES lda(id),
  distance REAL NOT NULL,
  topic_id1 SERIAL,
  topic_id2 SERIAL
);

CREATE TABLE IF NOT EXISTS topic_words (
  topic_id SERIAL REFERENCES topic(id),
  word_id SERIAL,
  probability REAL
);

CREATE TABLE IF NOT EXISTS dict (
  word TEXT,
  lda_id SERIAL REFERENCES lda(id)
);
