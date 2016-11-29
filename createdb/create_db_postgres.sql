CREATE TABLE IF NOT EXISTS lda_settings (
  id SERIAL PRIMARY KEY,
  number_of_topics INTEGER
);

CREATE TABLE IF NOT EXISTS dataset (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS lda (
  id SERIAL PRIMARY KEY,
  lda_settings_id INTEGER REFERENCES lda_settings(id),
  dataset_id INTEGER REFERENCES dataset(id)
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
  send_time_utc TIMESTAMP,
  dataset_id INTEGER NOT NULL REFERENCES dataset(id)
);

CREATE TABLE IF NOT EXISTS topic (
  id SERIAL PRIMARY KEY,
  lda_id INTEGER REFERENCES lda(id),
  name TEXT
);

CREATE TABLE IF NOT EXISTS email_blob (
  id SERIAL PRIMARY KEY,
  email_id INTEGER NOT NULL REFERENCES email(id),
  topic_probability REAL NOT NULL,
  topic_id INTEGER REFERENCES topic(id),
  lda_id INTEGER REFERENCES lda(id)
);

CREATE TABLE IF NOT EXISTS distance (
  id SERIAL PRIMARY KEY,
  lda_id SERIAL REFERENCES lda(id),
  distance REAL NOT NULL,
  topic_id1 INTEGER,
  topic_id2 INTEGER
);

CREATE TABLE IF NOT EXISTS dict (
  id SERIAL PRIMARY KEY,
  word TEXT,
  lda_id INTEGER REFERENCES lda(id)
);

CREATE TABLE IF NOT EXISTS topic_words (
  id SERIAL PRIMARY KEY,
  topic_id INTEGER REFERENCES topic(id),
  word_id INTEGER REFERENCES dict(id),
  probability REAL
);
