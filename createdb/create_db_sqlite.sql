CREATE TABLE lda (
  lda_settings_id INT UNSIGNED NOT NULL,
  dataset_id INT UNSIGNED NOT NULL
);

CREATE TABLE lda_settings (
  number_of_topics INT UNSIGNED NOT NULL
);

CREATE TABLE dataset (
  name TEXT
);

CREATE TABLE email (
  subject TXT,
  sender TINYTEXT,
  receiver TINYTEXT,
  cc TINYTEXT,
  bcc TINYTEXT,
  email_txt BLOB,
  send_time TIMESTAMP,
  dataset_id INT UNSIGNED NOT NULL
);

CREATE TABLE email_blob (
  email_id INT UNSIGNED NOT NULL,
  topic_probability FLOAT NOT NULL,
  topic_id INT UNSIGNED NOT NULL,
  lda_id INT UNSIGNED NOT NULL
);

CREATE TABLE distance (
  lda_id UNSIGNED NOT NULL,
  distance FLOAT NOT NULL,
  topic_id1 INT UNSIGNED NOT NULL,
  topic_id2 INT UNSIGNED NOT NULL
);

CREATE TABLE topic (
  lda_id INT UNSIGNED NOT NULL,
  name TINYTEXT
);

CREATE TABLE topic_words (
  topic_id INT UNSIGNED NOT NULL,
  word_id INT UNSIGNED NOT NULL,
  probability INT UNSIGNED NOT NULL
);

CREATE TABLE dict (
  word TINYTEXT,
  lda_id INT UNSIGNED NOT NULL
);
