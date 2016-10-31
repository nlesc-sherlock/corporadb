from glob2 import glob
import os
import argparse
from corpora.tokenizer import Tokenizer, filter_email

def saveTokens(filename, tokens):
    with open(filename, 'w') as fout:
        for token in tokens:
            fout.write(token + '\n')

def doTokenization(inputfolder,outputfolder):
    docs = glob(inputfolder + '/**/*.')
    tokenizer = Tokenizer(filters=[filter_email])
    for doc in docs:
        try:
            tokens = tokenizer.tokenize_file(doc)
            baseName=os.path.basename(doc)
            outputdir = os.path.dirname(doc.replace(inputfolder, outputfolder))
            targetFile = os.path.join(outputdir,baseName)
            if not os.path.exists(outputdir):
                os.makedirs(outputdir)
            saveTokens(targetFile, tokens)
        except:
            print("Error with doc: {0}".format(doc))

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tokenize and create dictionary out of given files")
    parser.add_argument('input_folder')
    parser.add_argument('output_folder')
    args = parser.parse_args()
    basedir = args.input_folder  # 'enron_mail_clean'
    savedir = args.output_folder  # 'enron_mail_clean_tokens'
    doTokenization(basedir,savedir)
