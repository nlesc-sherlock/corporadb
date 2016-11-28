CREATE TABLE IF NOT EXISTS lda (
  lda_settings_id SERIAL,
  dataset_id SERIAL
);

CREATE TABLE IF NOT EXISTS lda_settings (
  number_of_topics SERIAL
);

CREATE TABLE IF NOT EXISTS dataset (
  name TEXT
);

CREATE TABLE IF NOT EXISTS email (
  subject TEXT,
  sender TEXT,
  receiver TEXT,
  cc TEXT,
  bcc TEXT,
  email_txt TEXT,
  send_time TIMESTAMP [WITHOUT TIME ZONE],
  dataset_id INTEGER NOT NULL REFERENCES dataset
);

CREATE TABLE IF NOT EXISTS email_blob (
  email_id INTEGER NOT NULL REFERENCES email,
  topic_probability REAL NOT NULL,
  topic_id SERIAL REFERENCES topic,
  lda_id SERIAL REFERENCES lda
);

CREATE TABLE IF NOT EXISTS distance (
  lda_id SERIAL REFERENCES lda,
  distance REAL NOT NULL,
  topic_id1 SERIAL,
  topic_id2 SERIAL
);

CREATE TABLE IF NOT EXISTS topic (
  lda_id INT UNSIGNED NOT NULL,
  name TEXT
);

CREATE TABLE IF NOT EXISTS topic_words (
  topic_id SERIAL REFERENCES topic,
  word_id SERIAL,
  probability REAL
);

CREATE TABLE IF NOT EXISTS dict (
  word TEXT,
  lda_id SERIAL REFERENCES lda
);
