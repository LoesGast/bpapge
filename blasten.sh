#!/usr/bin/env bash

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/Panthera_tigris_altaica/RNA/rna.fa.gz -O tiger_genoom.fa.gz -q

gunzip *gz


formatdb -i tiger_genoom.fa -p F
blastall -p blastn -d tiger_genoom.fa  -i bpapge_seq_a1.txt -m8 > output_blasten.txt

#cat output_blasten.txt | awk '{if($11 == "0.0"){print $1, $2}}' | sort  | tr '|' ' ' | awk '{print $4}'

# kegg naam :ptg