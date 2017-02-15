cwlVersion: v1.0
class: CommandLineTool
label: BUILD DICTIONARY FROM EMAILS
baseCommand: buildDict.py
inputs:
  inputdir:
    type: Directory
    inputBinding:
      position: 1
  dictfile:
    type: string
    inputBinding:
      position: 2
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.dictfile)
