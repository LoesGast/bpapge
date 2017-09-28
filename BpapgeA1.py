# python 3 on linux

import os
import subprocess
import time



def dw_files():
    """


    :return: Niks
    """
    os.system('mkdir bestanden')
    os.system('mv downloadblast.sh ./bestanden/downloadblast.sh')
    os.system('mv bpapge_seq_a1.txt ./bestanden/bpapge_seq_a1.txt')
    subprocess.run(['bash', 'downloadblast.sh'], cwd='bestanden')
    os.system('mv ./bestanden/downloadblast.sh downloadblast.sh')
    os.system('mv ./bestanden/bpapge_seq_a1.txt bpapge_seq_a1.txt')
    print('Downloading done\nBlast done')


### download functies start
def download_bg_data_list(data_lijst, database_soort):
    os.system('mkdir temp')
    os.system('mkdir temp/{}'.format(database_soort))
    adderes = os.getcwd()+'/temp/{}'.format(database_soort)
    ncbi_addres = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    for naam in data_lijst:
        os.system(
            'wget "{3}db={0}&id={1}&rettype=gb&retmode=text" -O {2}/{1}.txt -q'.format(
                database_soort,  naam, adderes, ncbi_addres))

def allebestanden(path):
    bestandenlijst = os.listdir(path)
    nieuwe_bestandenlijst = []
    for item in bestandenlijst:
        nieuwe_bestandenlijst.append(item)
    return nieuwe_bestandenlijst

def finding_data(data_naam):
    path = os.getcwd() + '/temp/nucleotide/'
    protein_id_list = []
    for item in allebestanden(path):
        with open(path + item, 'r') as file:
            for item in file.readlines():
                if data_naam in item:
                    stripped_item = item.split('"')
                    protein_id_list.append(stripped_item[1])
    return protein_id_list

def download_all_bg_files():
    #dw_files()
    gene_lijst = []
    with open('./bestanden/output_blasten.txt', 'r') as gene_id_file:
        for gene_id in gene_id_file.readlines():
            if gene_id.split('\t')[10] == '0.0':
                gene_lijst += [gene_id.split('\t')[1].split('|')[3]]
    print(len(set(gene_lijst)))
    download_bg_data_list(set(gene_lijst), 'nucleotide')
    protein_lijst = finding_data('/protein_id=')
    download_bg_data_list(protein_lijst, 'protein')
### einde download functies

def finding_data_test(lijst, data):
    for line in lijst:
        if data in line:
            return line.split('"')[1]

def tussen_product_b_nucl():
    data_lijst = []
    nucl = allebestanden('./temp/nucleotide/')
    for i in nucl:
        with open('./temp/nucleotide/'+ i, 'r') as file:
            gene = finding_data_test(file.readlines(), '/gene=')
            naam = i[:-4]
            data_lijst += [(naam + '|' + gene)]
    print_in_file('nucleotide', data_lijst)

def tussen_product_b_prot():
    data_lijst = []
    prot = allebestanden('./temp/protein/')
    for i in prot:
        with open('./temp/protein/'+ i, 'r') as file:
            gene = finding_data_test(file.readlines(), '/product=')
            naam = i[:-4]
            data_lijst += [(naam + '|' + gene.strip().strip(','))]
    print_in_file('protein', data_lijst)



def print_in_file(filenaam, data_in_lijst):
    with open(filenaam, 'w') as write_file:
        for i in data_in_lijst:
            print(i, file=write_file)


def main():
    temp_naam = os.getcwd() + 'temp'
    print('''
Welkom bij het programma voor de opdracht van de hogeschool Leiden van de opleiding Bio-informatica.
met dit programma wordt het project applied genomics in jaar 2 uitgevoerd.
ik hoop dat u het leuk vind.
Met vriendelijke groeten,
Groep A1 (Shirley, Lotta, Hanna, Loes en Nils)\n\n\n\n''')
    time.sleep(5)
    if 'blasten.sh' not in os.listdir() or 'bpapge_seq_a1.txt' not in os.listdir():
        print('''er is een probleem met de files.
blasten.sh of bpapge_seq_a1.txt zijn niet id de map''')
        quit()
    else:
        while True:
            keuze = input('''welkom u kan nu het programma uit te voeren.
1) het uitvoeren van het programmma
2) opties veranderen
3) afsluiten
maak u keuzen:\n''')
            if keuze == '1':
                os.system('mkdir ./bestanden')
                os.system('mkdir ./{}'.format(temp_naam))
                pass
            elif keuze == '2':
                pass
            elif keuze == '3':
                exit()
            else:
                print('wrong input, probeer opnieuw.')

if __name__ == '__main__':
    main()

