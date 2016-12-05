cwlVersion: v1.0
class: Workflow

inputs:
    inputdir: Directory
    tempdir: string

outputs: []

steps:
    run: cleanheaders.cwl
    in:
        maildir: inputdir
        cleandir: tempdir
    run: tokenization.cwl
    in:
        inputdir: tempdir
        outputdir: tempdir
