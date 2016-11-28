CREATE VIEW spot_view AS
select
  ldas.number_of_topics as n_topics,
  da.id as dataset_id,
  da.name as dataset_name,
  email.subject, email.sender, email.receiver, email.cc, email.bcc, send_time,
  topic.name as topicname, topic.id as topic_id, lda.id as lda_id,
  emb.email_id as emailid,
  emb.topic_probability, dis.distance,
  dis.topic_id1 as dist_topic1, dis.topic_id2 as dist_topic2,
  dic.word as word,
  towo.probability as word_probability
FROM lda_settings ldas JOIN lda ON (ldas.id = lda.lda_settings_id)
            JOIN dataset da ON (da.id = lda.dataset_id)
            JOIN email  ON (da.id = email.dataset_id)
            JOIN topic ON (topic.lda_id = lda.id)
            JOIN distance dis ON (dis.lda_id = lda.id)
            JOIN email_blob emb ON (emb.email_id = email.id)
            JOIN dict dic ON (dic.lda_id = topic.id)
            JOIN topic_words towo ON (towo.topic_id = topic.id)
