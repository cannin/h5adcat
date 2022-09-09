# Introduction

Basic Information for single-cell RNAseq (scRNAseq) .h5ad Files and Conversion to MTX

# Installation 

```
pipx install git+https://github.com/cannin/h5adcat
```

# Usage
```
usage: h5adcat [-h] [-v] [-m] [-d] file

Basic Information for .h5ad Files and Conversion to MTX

positional arguments:
  file           Input .h5ad File

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -m, --mtx      convert to sparse matrix format (MTX)
  -d, --data     show limited data rows
```

# Run 

```
h5adcat H5AD_FILE
```
