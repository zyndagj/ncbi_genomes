ncbi_genomes
============

plot_genomes.py downloads a record of all prokaryote, eukaryote, and virus genomes from NCBI genome and plots the number completed by year.

Data is retrieved from ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/

Dependencies
------------

- Numpy
- Matplotlib

Usage
-----

```Shell
plot_genomes.py -o EXT
```

###Options:
```Shell
  -h, --help         show this help message and exit
  -o Ext, --out=Ext  Output figure format [emf, eps, pdf, png, ps, raw, rgba, svg, svgz]
```

Example
-------

```Shell
python plot_genomes -o png
```

Generates: genome_completed.png 
