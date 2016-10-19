CREATE TABLE lda (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  lda_settings_id INT UNSIGNED NOT NULL,
  dataset_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE lda_settings (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  lda_id INT UNSIGNED NOT NULL,
  number_of_words INT UNSIGNED,
  PRIMARY KEY (id)
);

CREATE TABLE dataset (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  name TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE email (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  subject TXT,
  sender TINYTEXT,
  receiver TINYTEXT,
  cc TINYTEXT,
  bcc TINYTEXT,
  email_txt BLOB,
  send_time TIMESTAMP,
  dataset_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE email_blob (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  email_id INT UNSIGNED NOT NULL,
  topic_probability FLOAT NOT NULL,
  topic_id INT UNSIGNED NOT NULL,
  lda_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE distance (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  lda_id UNSIGNED NOT NULL,
  distance FLOAT NOT NULL,
  topic_id1 INT UNSIGNED NOT NULL,
  toppic_id2 INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE topic (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  lda_id INT UNSIGNED,
  PRIMARY KEY (id)
);

CREATE TABLE topic_words (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  PRIMARY KEY (id)
  topic_id INT UNSIGNED NOT NULL,
  word_id INT UNSIGNED NOT NULL,
  probability INT UNSIGNED NOT NULL,
);

CREATE TABLE dict (
  id INT UNSIGNED AUTO_INCREMENT NOT NULL,
  word_id INT UNSIGNED,
  word TINYTEXT,
  lda_id INT UNSIGNED,
  PRIMARY KEY (id)
);
