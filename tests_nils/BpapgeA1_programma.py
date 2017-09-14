import os
import subprocess


def dw_files():
    """


    :return: Niks
    """
    os.system('pwd')
    os.system('mkdir bestanden')
    os.system('mv downloadblast.sh ./bestanden/downloadblast.sh')
    os.system('mv bpapge_seq_a1.txt ./bestanden/bpapge_seq_a1.txt')
    subprocess.run(['bash', 'downloadblast.sh'], cwd='bestanden')
    os.system('mv ./bestanden/downloadblast.sh downloadblast.sh')
    os.system('mv ./bestanden/bpapge_seq_a1.txt bpapge_seq_a1.txt')
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


def download_gb_data_FI(namen_file, database_soort):
    os.system('mkdir temp')
    os.system('mkdir temp/{}'.format(database_soort))
    adderes = os.getcwd()+'/temp/{}'.format(database_soort)
    with open(namen_file, 'r') as namen_bestand:
        namen = namen_bestand.read().strip()
        for naam in namen.split('\n'):
            download_from_NCBI(database_soort, naam, 'temp')


def download_bg_data_dict(data_dict, database_soort):
    os.system('mkdir temp')
    os.system('mkdir temp/{}'.format(database_soort))
    adderes = os.getcwd()+'/temp/{}'.format(database_soort)
    for i in data_dict:
        download_from_NCBI(database_soort, data_dict[i][1], 'temp')

def download_from_NCBI(database, id, temp_naam):
    print('{} wordt gedownload'.format(id))
    subprocess.run(['wget',
        "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text".format(
            database, id), '-O {}.txt'.format(id), '-q'], cwd='{}/{}'.format(temp_naam, database))



def data_splitten(path, data_dict, database):
    ID, gene, product = 'null', 'null', 'null'
    with open(path, 'r') as bg_file:
        for line in bg_file.read().strip().split('\n'):
            if database == 'nucleotide':
                if 'protein_id' in line:
                    ID = line.split('"')[1]
            else:
                if '/coded_by' in line:
                    ID = line.split('"')[1].split('.')[0]
            if '/gene' in line:
                gene = line.split('"')[1]
            if '/product' in line:
                product = line.split('"')[1]
            if 'ORIGIN' in line:
                data_dict[file] = [database, ID, gene, product]


def get_data(database):
    data_dict = {}
    path = os.getcwd() + '/temp/{}'.format(database)
    for file in os.listdir(path):

        ID, gene, product = 'null', 'null', 'null'
        with open(path + '/' + file, 'r') as bg_file:
            for line in bg_file.read().strip().split('\n'):
                if database == 'nucleotide':
                    if 'protein_id' in line:
                        ID = line.split('"')[1]
                else:
                    if '/coded_by' in line:
                        ID = line.split('"')[1].split('.')[0]
                if '/gene' in line:
                    gene = line.split('"')[1]
                if '/product' in line:
                    product = line.split('"')[1]
                if 'ORIGIN' in line:
                    data_dict[file] = [database, ID, gene, product]
    return data_dict


def main():
    dw_files()
    # genen = fill_seq('raw_genen.txt')
    # eiwiten = fill_seq('raw_eiwitten.txt')
    #
    #
    # for x in genen:
    #     print(x, genen[x])
    # print()
    #
    # for i in eiwiten:
    #     print(i, eiwiten[i])
    # test()
    # download_gb_data('./bestanden/gevonden_genen.txt', 'nucleotide')
    # nucl_data = get_data('nucleotide')
    # download_bg_data_dict(nucl_data, 'protein')
    # prot_data = get_data('protein')
    # print(prot_data)
    pass


if __name__ == '__main__':
    main()
