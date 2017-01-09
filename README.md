# corporadb
db backend corpora

## Installation instructions
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

## Step by step run:

Clean headers
```shell
$ python corpora/cleanHeaders.py data/enron_mail/ data/enron_mail/
```

Create tokens
```shell
$ python corpora/tokenization.py data/enron_mail/ data/enron_mail/
```

Merge tokens into dictionary
```shell
$ python corpora/buildDict.py data/enron_mail/ data/enron_mail.dict
```

Build document matrix
```shell
$ python corpora/buildDocumentMatrix.py data/enron_mail.dict data/enron_mail/ data/enron_mail.mtx
```

RUN:
```
$ SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/
$ SPARK_HOME/spark-submit corpora/trainModel.py data/enron_mail.mtx data/enron_mail.lda.model 5 10
```
