SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/
DATASET_NAME=data/enron_mail_small

ORIG_DATA=$DATASET_NAME/
CLEAN_DATA=$DATASET_NAME'_clean/'
CLEAN_TOKENS=$DATASET_NAME'_clean_tokens/'
DATA_DICT=$DATASET_NAME'.dict'
DOC_MATRIX=$DATASET_NAME'.mtx'
LDA_MODEL=$DATASET_NAME'_LDA/'

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

# echo 'RUNNING TEST ================================'
# python test.py
