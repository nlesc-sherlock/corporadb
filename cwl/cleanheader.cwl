cwlVersion: v1.0
class: CommandLineTool
label: CLEAN FILE HEADERS
baseCommand: python corpora/cleanHeaders.py
arguments: ["-d", $(runtime.outdir)]
inputs:
  rawfile:
    type: File
    inputBinding:
      position: 1
  cleanedfile:
    type: string
    inputBinding:
      position: 2
outputs:
  cleaned_out:
    type: File
    outputBinding:
      glob: $(inputs.cleanedfile)
