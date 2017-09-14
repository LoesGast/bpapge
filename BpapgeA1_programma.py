import os
import subprocess


def dw_files():
    try:
        os.system('mkdir bestanden')
        os.system('mv opdracht ./bestanden/opdracht')
        os.system('mv bpapge_seq_a1 ./bestanden/bpapge_seq_a1')
    finally:
        subprocess.run(['bash', 'opdracht'], cwd='bestanden')
        os.system('mv ./bestanden/opdracht opdracht')
        os.system('mv ./bestanden/bpapge_seq_a1 bpapge_seq_a1')
        print('Downloading done\nBlast done')


def fill_seq(naam):
    raw = {}
    with open('./bestanden/{}'.format(naam), 'r') as file:
        for line in file.read().strip().split('\n'):
            data = line.split('\t')
            if data[10] == '0.0':
                if data[1].split('|')[3] in raw:
                    raw[data[1].split('|')[3]] = raw[data[1].split('|')[3]] + '|' + data[0]
                else:
                    raw[data[1].split('|')[3]] = data[0]
    return raw


def test():
    with open('test.txt', 'r') as test:
        for line in test.read().strip().split('\n'):
            # print(line.split('\t'))
            print(line)
            # if '/gene' in line:
            #     print(line.strip(' ').split('"')[1])


def download_gb_data(namen_file, database_soort):
    os.system('mkdir temp')
    with open(namen_file, 'r') as namen_bestand:
        namen = namen_bestand.read().strip()
        for naam in namen.split('\n'):
            print('{} wordt gedownload'.format(naam))
            subprocess.run(['wget',
                            "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text".format(
                                database_soort, naam), '-O {}.txt'.format(naam), ' -P temp/'])


def main():
    # dw_files()
    # genen = fill_seq('raw_genen.txt')
    # eiwiten = fill_seq('raw_eiwitten.txt')
    #
    # for x in genen:
    #     print(x, genen[x])
    # print()
    #
    # for i in eiwiten:
    #     print(i, eiwiten[i])
    test()
    #download_gb_data('./bestanden/gevonden_genen.txt', 'nucleotide')

    pass


if __name__ == '__main__':
    main()
