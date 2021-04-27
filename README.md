# FASTAfromBLAST
Extract FASTA sequences of regions of genome assemblies from NCBI BLAST alignments

Store NCBI alignments as FASTAs with alignment coverage only under a directory (the first argument).
Then have complete genome sequences in FASTA format in a seperate directory.
Ensure file name relating to a given isolate/sample is the same across both directories.

---

### How to run:
```
>>> python FASTAfromBLAST.py [path/to/directory/containing/alignments] [path/to/directory/containing/FASTAs] [output/directory]
```