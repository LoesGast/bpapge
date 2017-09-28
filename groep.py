import os
from protein_genbank_file import Protein_gb_info




# os.system('wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt'.format('nucleotide', 'XM_007079698.2'))


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

def finding_CDS(data_soort):
    path = os.getcwd() + '/temp/{}/'.format(data_soort)
    protein_id_list = []
    for item in allebestanden(path):
        with open(path + item, 'r') as file:
            for item in file.readlines():
                if '/protein_id=' in item:
                    stripped_item = item.split('"')
                    protein_id_list.append(stripped_item[1])
    return protein_id_list


def maak_from_dict_list(de_gekoze_dict, positie_in_de_dict):
    atributen_lijst = []
    for i in de_gekoze_dict:
        if type(de_gekoze_dict[i][positie_in_de_dict]) == str:
            atributen_lijst += [de_gekoze_dict[i][positie_in_de_dict]]
    return atributen_lijst


def download_kegg_info(ec_nummer_lijst):
    os.system('mkdir ./temp | mkdir ./temp/pathways')
    for ec_nummer in ec_nummer_lijst:
        os.system(
            'wget "http://rest.kegg.jp/get/{0}" -O ./temp/pathways/{0}.txt -q'.format(
                ec_nummer))


# pathways er uit halen
def get_pathways():
    pathway_dict = {}
    pathway_regio = False
    pathway_lijst = os.listdir('./temp/pathways')
    for x, ec_nummer_file in enumerate(pathway_lijst):
        with open('./temp/pathways/' + ec_nummer_file, 'r') as file:
            for line in file.readlines():
                if 'PATHWAY' in line:
                    pathway_regio = True
                if 'ORTHOLOGY' in line:
                    pathway_regio = False
                elif pathway_regio:
                    data = line.strip('PATHWAY').strip().split('  ')
                    pathway_dict[data[0]] = data[1]
    return pathway_dict


if __name__ == '__main__':
    #print(finding_CDS('nucleotide'))
    #download_bg_data_list(finding_CDS('nucleotide'), 'protein')
    data_lijst = []
    for i in os.listdir('./temp/protein/'):
        print(i)
        if os.stat(os.getcwd() + '/temp/protein/' + i).st_size != 0:
            with open(os.getcwd() + '/temp/protein/' + i) as file:
                data_lijst += [Protein_gb_info(file)]
    for protein in data_lijst:
        print(protein, protein.get_ec_nummer())
        for region in protein.get_regions():
            print(region, protein.get_regions()[region])



    # download_kegg_info(['6.1.1.14'])
    # data = get_pathways()
    # print(len(data))
    # for i in data:
    #     print(data[i], i)
    # os.system(
    #             'wget "http://rest.kegg.jp/get/{0}" -O ./temp/pathways/{0}.txt -q'.format(
    #                 'ec00970'))


