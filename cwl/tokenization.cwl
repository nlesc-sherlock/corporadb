cwlVersion: v1.0
class: CommandLineTool
label: TOKENIZE MAIL BODIES
baseCommand: tokenization.py
inputs:
  inputdir:
    type: Directory
    inputBinding:
      position: 1
  tokendir:
    type: string
    inputBinding:
      position: 2
  language:
    type: string
    inputBinding:
      position: 3
outputs:
  outputdir:
    type: Directory
    outputBinding:
      glob: $(inputs.tokendir)
