SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/
DATASET_NAME=data/enron_mail_small
N_TOPICS=25

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
$SPARK_HOME/spark-submit corpora/trainModel.py $DOC_MATRIX $LDA_MODEL $N_TOPICS 10

# echo 'RUNNING TEST ================================'
# python test.py
# Start postgres container
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
# connect to it...
docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -U postgres
# Copy/paste create_db_postgres.sql and create_spot_view.sql

# Set dataset name manually
# Set number of tokens manually...
python corporadb/fill_db.py $DATASET_NAME $N_TOPICS
