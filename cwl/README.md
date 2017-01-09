# corporadb/cwl

Common workflow language scripts and configuration files for corpora analysis. To run the cwl jobs without modifying paths in the yml job files, you should place the email data in a
subdirectory named

# Installation

Install the default cwl-tool implementation:

```shell
$ pip install cwltool
```

or download and install from source (see https://github.com/common-workflow-language/cwltool). Then download and extract the enron email
data in a subfolder named enron\_mail.

# Step-by-step run:

Clean headers
```shell
$ cwltool cleanHeader.cwl cleanHeader-job.yml
```

Create tokens
```shell
$ cwltool tokenization.cwl tokenization-job.yml
```

Build dictionary
```shell
$ cwltool buildDict.cwl buildDict-job.yml
```

Build document matrix
```shell
$ cwltool builddocmatrix.cwl builddocmatrix-job.yml
```
