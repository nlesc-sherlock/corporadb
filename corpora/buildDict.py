import gensim
import argparse
from corpora.utils import loadDocuments

def generateDictionary(inputfolder, outputDict):
    docs = loadDocuments(inputfolder)
    newDic = gensim.corpora.Dictionary.from_documents(docs)
    newDic.save(outputDict)

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tokenize and create dictionary out of given files")
    parser.add_argument('input_folder')
    parser.add_argument('output_dictionary')
    args = parser.parse_args()
    basedir = args.input_folder  # 'enron_mail_clean_tokens'
    savedict = args.output_dictionary  # 'enron_mail_clean.dict'
    generateDictionary(basedir, savedict)
