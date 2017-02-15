# corporadb

For project Sherlock, our team aims to use NLP tools to analyse large collections of documents. The original description of the team's goals are on Sherlock's [repo](https://github.com/nlesc-sherlock/Sherlock/blob/master/topics/analyzing_document_collections/analyzing_large_document_collections.md).

The following sections describes the process for going from a bunch of plain text documents (emails in this case) to a nice visualization of the topics in these documents.

## 1 Installation instructions
Optionally create a virtual python environment in this repo clone.
Then type

```shell
$ pip install -e .
$ python setup.py install
```

The first command may result in missing header messages, which will require you to build or download some additional
libraries. On Debian and Ubuntu systems, you can do

```shell
$ sudo apt-get install python-dev libyaml-dev libssl-dev libffi-dev
```

whereas in Fedora or Red Hat distros type

```shell
$ sudo yum install python-devel libyaml-devel libssl-devel libffi-devel

```

You will also need to download some NLTK data:
```shell
$ python -m nltk.downloader stopwords
```
where you have activated your virtual environment, if you use one.

## 2 Pre-processing:

### 2.1 Preprocessing using step by step Python commands

Clean headers
```shell
$ python corpora/cleanHeaders.py cwl/enron_mail/ cwl/enron_mail_clean/
```

Create tokens
```shell
$ python corpora/tokenization.py cwl/enron_mail_clean/ cwl/enron_mail_clean_tokens/
```

Merge tokens into dictionary
```shell
$ python corpora/buildDict.py cwl/enron_mail_clean_tokens/ cwl/enron_mail.dict
```

Build document matrix
```shell
$ python corpora/buildDocumentMatrix.py cwl/enron_mail.dict cwl/enron_mail_clean_tokens/ cwl/enron_mail.mtx
```

### 2.2 Preprocessing using a CWL workflow

See [this](https://github.com/nlesc-sherlock/corporadb/tree/master/cwl) tutorial

## 3 Train model

Next, the LDA model is trained in Spark. Follow installation instructions from here: https://spark.apache.org/docs/latest/

RUN:
```
$ SPARK_HOME=(path to you Spark installation, e.g. /home/johndoe/spark-2.0.1/bin/)
$ $SPARK_HOME/spark-submit corpora/trainModel.py cwl/enron_mail.mtx cwl/enron_mail.lda.model 5 10
```
## 4 Create and fill database

See [this](https://github.com/nlesc-sherlock/corporadb/tree/master/createdb) tutorial

## 5 Create visualisation

...
