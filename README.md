# corporadb
db backend corpora

## Step by step run:

Clean headers
```shell
$ python corpora/cleanHeaders.py data/enron_mail_random/ data/enron_mail_random_clean/
```

Create tokens
```shell
$ python corpora/tokenization.py data/enron_mail_random_clean/ data/enron_mail_random_clean_tokens/
```

Merge tokens into dictionary
```shell
$ python corpora/buildDict.py data/enron_mail_random_clean_tokens/ data/enron_mail_random_clean.dict
```

Build document matrix
```shell
$ python corpora/buildDocumentMatrix.py data/enron_mail_random_clean.dict data/enron_mail_random_clean_tokens/ data/enron_mail_random_clean.mtx
```

RUN:
```
$ SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/
$SPARK_HOME/spark-submit corpora/trainModel.py data/enron_mail_random_clean.mtx data/enron_mail_random_clean.lda.model 5 10
```
