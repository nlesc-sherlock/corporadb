cwlVersion: v1.0
class: Workflow

inputs:
    inputdir: Directory
    workdir: string

outputs: []

steps:
    run: cleanheader.cwl
    in:
        inputdir: inputdir
        cleandir: workdir
    run: tokenization.cwl
    in:
        inputdir: workdir
        cleandir: workdir
