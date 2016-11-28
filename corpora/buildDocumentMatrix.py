import gensim
import argparse
from corpora.utils import loadTokens
from glob2 import glob
from scipy import sparse
from scipy.io import mmwrite


def buildMatrix(inputDict, inputFolder, outputMatrix):
    wordDict = gensim.corpora.Dictionary.load(inputDict)
    wordDict.filter_extremes()

    # docs = loadDocuments(inputFolder)
    docs = glob(inputFolder + '/**/*.')
    nDocs = len(docs)
    nWords = len(wordDict)

    sp = sparse.dok_matrix((nWords, nDocs))
    for docId,doc in enumerate(docs):
        docTokens = loadTokens(doc)
        for wordIdx,wordCount in wordDict.doc2bow(docTokens):
            sp[wordIdx,docId] = wordCount
    print 'Words,Documents: ',(nWords, nDocs)
    mmwrite(outputMatrix, sp)

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tokenize and create dictionary out of given files")
    parser.add_argument('input_dictionary')
    parser.add_argument('input_folder')
    parser.add_argument('output_matrix')
    args = parser.parse_args()
    inputdict = args.input_dictionary  # 'enron_mail_clean.dict'
    basedir = args.input_folder  # 'enron_mail_clean_tokens'
    savematrix = args.output_matrix  # 'enron_mail_random_clean.mtx'
    buildMatrix(inputdict, basedir, savematrix)
