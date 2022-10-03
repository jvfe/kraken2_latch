## Kraken2

This is a [LatchBio](https://github.com/latchbio/latch) workflow
to run Kraken2.

Kraken 2[^1] is the newest version of Kraken, a taxonomic
classification system using exact k-mer matches to achieve
high accuracy and fast classification speeds. This classifier
matches each k-mer within a query sequence to the lowest common ancestor (LCA)
of all genomes containing the given k-mer. The k-mer assignments inform
the classification algorithm.

[^1]:
    Wood, D.E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2.
    Genome Biol 20, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0
