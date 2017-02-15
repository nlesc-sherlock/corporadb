from glob2 import glob
import os
import argparse
from corpora.tokenizer import Tokenizer, filter_email

def saveTokens(filename, tokens):
    with open(filename, 'w') as fout:
        for token in tokens:
            fout.write(token + '\n')

def doTokenization(inputfolder,outputfolder, lang='en'):
    inputdirname = inputfolder.rstrip('/')
    outputdirname = outputfolder.rstrip('/')
    docs = glob(inputdirname + '/**/*.')
    tokenizer = Tokenizer(filters=[filter_email], lang=lang)
    for doc in docs:
        try:
            tokens = tokenizer.tokenize_file(doc)
            baseName=os.path.basename(doc)
            outputdir = os.path.dirname(doc.replace(inputdirname, outputdirname))
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
    parser.add_argument('language')
    args = parser.parse_args()
    basedir = args.input_folder  # 'enron_mail_clean'
    savedir = args.output_folder  # 'enron_mail_clean_tokens'
    doTokenization(basedir,savedir,args.language)
