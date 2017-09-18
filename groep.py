import os
os.system('wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt'.format('nucleotide', 'XM_007079698.2'))
