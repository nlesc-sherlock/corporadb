from glob2 import glob

def loadDocuments(inputfolder):
    docs = glob(inputfolder + '/**/*.')
    for doc in docs:
        tokens = loadTokens(doc)
        yield tokens

def loadTokens(filename):
    with open(filename, 'r') as fin:
        tokens = [ line.strip() for line in fin ]
    return tokens
