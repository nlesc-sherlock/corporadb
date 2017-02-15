#!/bin/bash

INPUTDIR=${PWD}/enron_mail
WORKDIR=${PWD}/tmp
LANG=en
NTOPICS=25
NLDAITERS=10

while getopts ":d:o:h:l:n:m:" OPT; do
  case "${OPT}" in

    i) INPUTDIR=${OPTARG};;
    o) WORKDIR=${OPTARG};;
    l) LANG=${OPTARG};;
    n) NTOPICS=${OPTARG};;
    m) NLDAITERS=${OPTARG};;
    *) echo "Usage: ./runAll.sh -i <input data dir> -o <working dir> -l <en|nl> -n <nr of topics> -m <nr of iterations>"
       exit 1;;
  esac
done
shift $((OPTIND-1))

if [[ ! -d ${INPUTDIR} ]]; then
  echo "Input directory ${INPUTDIR} does not exist... aborting" >&2; exit 1
fi
if [[ -d ${WORKDIR} ]]; then
  echo "Working directory ${WORKDIR} already exists, please remove or rename..." >&2; exit 1
fi
if [[ ${LANG} != "en" && ${LANG} != "nl" ]]; then
  echo "Unknown language passed ${LANG}" >&2; exit 1
fi
if [[ ${NTOPICS} =~ '^[0-9]+$' ]]; then
  echo "Invalid number of topics passed: ${NTOPICS}" >&2; exit 1
fi
if [[ ${NLDAITERS} =~ '^[0-9]+$' ]]; then
  echo "Invalid number of LDA iterations passed: ${NLDAITERS}" >&2; exit 1
fi

NAMEROOT=${WORKDIR}/$(basename $INPUTDIR)
ORIG_DATA=${INPUTDIR}
CLEAN_DATA=${NAMEROOT}_clean/
CLEAN_TOKENS=${NAMEROOT}_clean_tokens/
DATA_DICT=${NAMEROOT}.dict
DOC_MATRIX=${NAMEROOT}.mtx
LDA_MODEL=${NAMEROOT}.lda.model

echo "Running corpora pipeline with following settings:"
echo "Input directory: ${INPUTDIR}"
echo "Working directory: ${WORKDIR}"
echo "Language: ${LANG}"
echo "Nr of requested topics: ${NTOPICS}"
echo "Nr of LDA iterations: ${NLDAITERS}"

# INPUTDIR=cwl/enron_mail_translated_en
# INPUTDIR=cwl/enron_mail_translated_nl
# INPUTDIR=cwl/enron_mail_random

# Change to your installation path
# SPARK_HOME=/home/carlosm/Projects/Sherlock/spark-2.0.1/bin/


echo 'CREATING WORKING DIRECTORY =================='
mkdir -p ${WORKDIR}
echo 'RUNNING CLEAN HEADERS ======================='
python corpora/cleanHeaders.py ${ORIG_DATA} ${CLEAN_DATA}
echo 'RUNNING TOKENIZATION ========================'
python corpora/tokenization.py ${CLEAN_DATA} ${CLEAN_TOKENS} ${LANG}
echo 'RUNNING BUILD DICTIONARY ===================='
python corpora/buildDict.py ${CLEAN_TOKENS} ${DATA_DICT}
echo 'RUNNING BUILD MATRIX ========================'
python corpora/buildDocumentMatrix.py ${DATA_DICT} ${CLEAN_TOKENS} ${DOC_MATRIX}

if [[ -z "$SPARK_HOME" ]]; then
  echo "SPARK_HOME environment variable was not set...please set it to your spark folder." >&2; exit 1
fi
if [[ ! -x "${SPARK_HOME}/bin/spark-submit" ]]; then
  echo "spark-submit was not found in ${SPARK_HOME}/bin..." >&2; exit 1
fi

echo 'RUNNING BUILD MODEL ========================='
${SPARK_HOME}/spark-submit corpora/trainModel.py ${DOC_MATRIX} ${LDA_MODEL} ${NTOPICS} ${NLDAITERS}
exit 0
