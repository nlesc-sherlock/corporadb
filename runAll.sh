SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/
ORIG_DATA=data/enron_mail_translated_en/
CLEAN_DATA=data/enron_mail_translated_en_clean/
CLEAN_TOKENS=data/enron_mail_translated_en_clean_tokens/
DATA_DICT=data/enron_mail_translated_en.dict
DOC_MATRIX=data/enron_mail_translated_en.mtx
LDA_MODEL=data/enron_mail_translated_en.lda.model

echo 'RUNNING CLEAN HEADERS ======================='
python corpora/cleanHeaders.py $ORIG_DATA $CLEAN_DATA
echo 'RUNNING TOKENIZATION ========================'
python corpora/tokenization.py $CLEAN_DATA $CLEAN_TOKENS
echo 'RUNNING BUILD DICTIONARY ===================='
python corpora/buildDict.py $CLEAN_TOKENS $DATA_DICT
echo 'RUNNING BUILD MATRIX ========================'
python corpora/buildDocumentMatrix.py $DATA_DICT $CLEAN_TOKENS $DOC_MATRIX
echo 'RUNNING BUILD MODEL ========================='
$SPARK_HOME/spark-submit corpora/trainModel.py $DOC_MATRIX $LDA_MODEL 25 10
