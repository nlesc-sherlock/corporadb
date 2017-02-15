cwlVersion: v1.0
class: CommandLineTool
label: BUILD DICTIONARY FROM EMAILS
baseCommand: buildDocumentMatrix.py
inputs:
  inputdir:
    type: Directory
    inputBinding:
      position: 2
  inputdict:
    type: File
    inputBinding:
      position: 1
  matrixfile:
    type: string
    inputBinding:
      position: 3
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.matrixfile)
