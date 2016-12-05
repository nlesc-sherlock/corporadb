cwlVersion: v1.0
class: CommandLineTool
label: TOKENIZE MAIL BODIES
baseCommand: python corpora/tokenization.py
inputs:
  inputdir:
    type: Directory
    inputBinding:
      position: 1
  tokendir:
    type: string
    inputBinding:
      position: 2
outputs:
  outputdir:
    type: Directory
    outputBinding:
      glob: $(inputs.tokendir)
