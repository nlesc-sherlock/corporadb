CREATE VIEW spot_view AS
select
  lda_settings.id as lda_settings_id,
  lda_settings.number_of_topics as lda_settings_ntopics,
  email.subject as subject,
  email.sender as sender,
  email.receiver as receiver,
  email.cc as cc,
  email.bcc as bcc,
  email.send_time as send_time,
  email_blob.topic_probability as email_topic_prob,
  topic.id as topic_id,
  topic.name as topic_name
FROM dataset JOIN lda ON (dataset.id = lda.dataset_id)
             JOIN lda_settings ON (lda.lda_settings_id = lda_settings.id)
             JOIN email ON (dataset.id = email.dataset_id)
             JOIN email_blob ON (email.id = email_blob.email_id)
             JOIN topic ON (email_blob.topic_id=topic.id)
