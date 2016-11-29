cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python","-m","corpora.cleanHeaders"]
inputs:
    inputdir:
        type: Directory
        inputBinding: {position: 1}
    outputdir:
        type: string
        inputBinding: {position: 2}
outputs: []
