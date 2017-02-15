cwlVersion: v1.0
class: CommandLineTool
label: CLEAN FILE HEADERS
baseCommand: cleanHeaders.py
inputs:
  inputdir:
    type: Directory
    inputBinding:
      position: 1
  cleandir:
    type: string
    inputBinding:
      position: 2
outputs:
  outputdir:
    type: Directory
    outputBinding:
      glob: $(inputs.cleandir)
