import os
import subprocess
#os.system('wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt'.format('nucleotide', 'XM_007079698.2'))




def move_and_excute():
    os.system('mkdir bestanden')
    os.system('mv blasten.sh ./bestanden/blasten.sh')
    os.system('mv bpapge_seq_a1.txt ./bestanden/bpapge_seq_a1.txt')
    subprocess.run(['bash', 'blasten.sh'], cwd='bestanden')
    os.system('mv ./bestanden/blasten.sh blasten.sh')
    os.system('mv ./bestanden/bpapge_seq_a1.txt bpapge_seq_a1.txt')
    print('Downloading done\nBlast done')

def open_get_names():
    lijst = []
    with open('./bestanden/output_blasten.txt', 'r') as blast:
        for line in blast.read().strip().split('\n'):
            data = line.split('\t')
            if data[10] == '0.0':
                lijst += [line.split('\t')[1].split('|')[3]]
        set_lijst = set(lijst)
    return set_lijst

def download_bg_data_list(data_list, database_soort):
    os.system('mkdir temp')
    os.system('mkdir temp/{}'.format(database_soort))
    adderes = os.getcwd()+'/temp/{}'.format(database_soort)
    ncbi_adress = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    for i in data_list:
        os.system(
    'wget "{0}db={1}&id={2}&rettype=gb&retmode=text" -O {3}/{2}.txt'.format(
        ncbi_adress, database_soort, i, adderes))


def main():
    # move_and_excute()
    # download_bg_data_list(open_get_names(), 'nucleotide')


if __name__ == '__main__':
    main()