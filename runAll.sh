DATASET=cwl/enron_mail
# DATASET=cwl/enron_mail_translated_en
# DATASET=cwl/enron_mail_translated_nl
# DATASET=cwl/enron_mail_random

# Change to your installation path
SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/

ORIG_DATA=$DATASET
CLEAN_DATA=${DATASET}_clean/
CLEAN_TOKENS=${DATASET}_clean_tokens/
LANGUAGE=en
DATA_DICT=${DATASET}.dict
DOC_MATRIX=${DATASET}.mtx
LDA_MODEL=${DATASET}.lda.model

echo 'RUNNING CLEAN HEADERS ======================='
python corpora/cleanHeaders.py $ORIG_DATA $CLEAN_DATA
echo 'RUNNING TOKENIZATION ========================'
python corpora/tokenization.py $CLEAN_DATA $CLEAN_TOKENS $LANGUAGE
echo 'RUNNING BUILD DICTIONARY ===================='
python corpora/buildDict.py $CLEAN_TOKENS $DATA_DICT
echo 'RUNNING BUILD MATRIX ========================'
python corpora/buildDocumentMatrix.py $DATA_DICT $CLEAN_TOKENS $DOC_MATRIX
echo 'RUNNING BUILD MODEL ========================='
$SPARK_HOME/spark-submit corpora/trainModel.py $DOC_MATRIX $LDA_MODEL 25 10
