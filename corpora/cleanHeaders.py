#!/usr/bin/env python

# Copyright 2015 Netherlands eScience Center <info@esciencecenter.nl>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from glob2 import glob
from email.parser import Parser
import json
import os
import argparse
import re

# Extracts the email text and headers from the input file
def extractEmailBody(filename):
    with open(filename, 'r') as fin:
        mail = fin.readlines()
        mail = ''.join(mail)
        msg = Parser().parsestr(mail)

        metadata = {
            'To': msg['to'],
            'From': msg['from'],
            'Cc': msg['cc'],
            'Bcc': msg['bcc'],
            'Subject': msg['subject'],
            'Date': msg['date'],
            'References': msg['references']
        }
        return msg.get_payload(), metadata

# Removes everything after 'Original Message' or '<somebody> wrote:'
# TODO: Fix this for replies AFTER original messages
def removeOriginalQuote(body):
    match = re.search('.*( wrote:)[\n]+>',body)
    if match:
        body = body[:match.start()]
    match = re.search('-* *(Original Message:) *-*',body,re.I)
    if match:
        body = body[:match.start()]
    match = re.search('-* *(Forwarded by)',body,re.I)
    if match:
        body = body[:match.start()]
    return body.strip()

# Writes the email text to the argument filename
def saveEmailBody(filename, body):
    with open(filename, 'w') as fout:
        fout.write(body)

# Writes the metadata to the argument filename
def saveMetaData(filename, metadata):
    with open(filename, 'w') as fout:
        json.dump(metadata, fout, indent=2, ensure_ascii=False)

def fixMalformedMime(body):
    raise Exception("Not implemented yet")

# Does the full preprocessing of the dataset
def preProcess(inputfolder,outputfolder):
    docs = glob(inputfolder + '/**/*.')
    metaData = []
    for doc in docs:
        try:
            body, emailMeta = extractEmailBody(doc)
            body = removeOriginalQuote(body)
            origName = doc.replace(inputfolder, '')
            if origName.startswith('/'):
                origName = origName[1:]
            saveName = os.path.join(outputfolder, origName)
            saveDir  = os.path.dirname(saveName)
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
            saveEmailBody(saveName, body)
            emailMeta['id'] = origName
            metaData.append(emailMeta)
        except Exception as e:
            print("Error with doc: {0}".format(doc))
            print e
    print "Finished parsing documents..."
    if(metaData):
        # saveMetaData(outputfolder + '/metadata.json', metaData)
        pass

# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Remove headers from emails")
    parser.add_argument('input_folder')
    parser.add_argument('output_folder')
    args = parser.parse_args()
    input_folder = args.input_folder  # 'enron_mail'
    output_folder = args.output_folder  # 'enron_mail_clean'
    preProcess(input_folder,output_folder)
