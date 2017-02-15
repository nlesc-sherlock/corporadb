cwlVersion: v1.0

class: Workflow

inputs:
    inputdir: Directory
    cleandir: string
    tokendir: string
    dictfile: string
    matrixfile: string

outputs:
    dictionary:
        type: File
        outputSource: builddictionary/output
    docmatrix:
        type: File
        outputSource: builddocmatrix/output

steps:
    cleanheaders:
        run: 
            cleanheader.cwl
        in:
            inputdir: inputdir
            cleandir: cleandir
        out: [outputdir]

    tokenization:
        run: 
            tokenization.cwl
        in:
            inputdir: cleanheaders/outputdir
            tokendir: tokendir
        out: [outputdir]

    builddictionary:
        run: 
            builddict.cwl
        in:
            inputdir: tokenization/outputdir
            dictfile: dictfile
        out: [output]

    builddocmatrix:
        run: 
            builddocmatrix.cwl
        in:
            inputdir: tokenization/outputdir
            inputdict: builddictionary/output
            matrixfile: matrixfile
        out: [output]
