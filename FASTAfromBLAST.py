"""
FASTAfromBLAST.py

---

Get FASTA sequences of sequence regions covered in NCBI BLAST alignments.

Store NCBI alignments as FASTAs with alignment coverage only under a directory (the first argument).
Then have complete genome sequences in FASTA format in a seperate directory.
Ensure file name relating to a given isolate/sample is the same across both directories.

---

Usage:
>>> python FASTAfromBLAST.py [path/to/directory/containing/alignments] [path/to/directory/containing/FASTAs] [output/directory]

"""


import re
from itertools import combinations
from os import listdir, mkdir, path
from sys import argv

from Bio import SeqIO


def getBPrange(fp: str) -> list:
    with open(fp) as a:
        skip = False

        lines = [line for line in a.readlines() if line.startswith(">lcl|")]
        try:
            align_a, *align_b = lines
        except ValueError:
            # print(lines)
            align_a = lines[0]
            skip = True

    first_a, first_b = re.findall(r"[:](\d+)[-]", align_a)[0], re.findall(r"[-](\d+)[\s]", align_a)[0]
    combos = [first_a, first_b]
    if not skip:
        for alignment in align_b:
            end_a, end_b = re.findall(r"[-](\d+)[\s]", alignment)[0], re.findall(r"[:](\d+)[-]", alignment)[0]
            combos += [end_a, end_b]
    values, equation = [], []
    for x, y in combinations(combos, 2):
        equation.append([int(x), int(y)])
        values.append(abs(int(x) - int(y)))

    max_value = max(values)

    for index, value in enumerate(values):
        if value == max_value:
            # print(equation[index], value)
            return equation[index]


def main(align_dir: str, fasta_dir: str, output: str):

    for foo in listdir(align_dir):
        fp = path.join(align_dir, foo)
        equation = getBPrange(fp)

        ID = foo[:-4]
        seq = SeqIO.parse(f"{fasta_dir}/{ID}.fasta", "fasta")

        start, end = equation

        for index, sequence in enumerate(seq):
            if index == 1:
                break
            
            if end > start:
                out_seq = sequence[start:end]
                # print(len(sequence[start:end]))
            else:
                out_seq = sequence[end:start]
                # print(len(sequence[end:start]))

            def write_output():
                with open(f"{output}/{ID}.fasta", 'w') as out:
                    out.write(out_seq.format("fasta"))

            try:
                write_output()
            except FileNotFoundError:
                mkdir(output)
                write_output()


if __name__ == "__main__":
    main(argv[1], argv[2], argv[3])