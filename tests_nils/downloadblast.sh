#!/usr/bin/env bash

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/Panthera_tigris_altaica/protein/protein.fa.gz -O tiger_protein.fa.gz -q

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/Panthera_tigris_altaica/RNA/rna.fa.gz -O tiger_genoom.fa.gz -q

gunzip *gz

formatdb -i tiger_protein.fa
formatdb -i tiger_genoom.fa -p F




blastall -p blastx -d tiger_protein.fa -i bpapge_seq_a1 -m8 >raw_eiwitten.txt
cat raw_eiwitten.txt | awk '{if($11 == "0.0"){print $2}}' | sort | uniq | tr '|' ' ' | awk '{print $4}' > gevonden_eiwitten.txt

cat tiger_protein.fa | tr "\n" "@" | sed 's/@>/\n>/g' | egrep -f gevonden_eiwitten.txt | sed 's/@/\n/g' > eiwitten_tiger.fa



blastall -p blastn -d tiger_genoom.fa -i bpapge_seq_a1 -m8 > raw_genen.txt
cat raw_genen.txt | awk '{if($11 == "0.0"){print $2}}' | sort | uniq | tr '|' ' ' | awk '{print $4}' > gevonden_genen.txt

cat tiger_genoom.fa | tr "\n" "@" | sed 's/@>/\n>/g' | egrep -f gevonden_genen.txt | sed 's/@/\n/g'> genen_tiger.fa

echo "kegg naam :ptg"
