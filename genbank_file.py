import requests #commandline: sudo pip3 install biopython
import sys


class Protein_gb_info():

    def __init__(self, file_naam):
        self.file = open(file_naam, 'r').readlines()
        self.__lijst_met_variables()
        self._split_protein_regions()
        self.__get_info()
        self._ec_getter()

    def __lijst_met_variables(self):
        self.locus = self.file[0].split('      ')[1].strip(' ')
        self.name = self.file[1].split(':')[-1].split('[')[0].strip(' ')
        self.regions = {}
        self.site = {}
        self.sequence = ''
        self.ec_nummer = ''

    def get_regions(self):
        """
        returnt de regions die in de genbank file staan.
        :return: Regions Dict.
        """
        return self.regions

    def get_sequence(self):
        return self.sequence

    def get_sites(self):
        return self.site

    def get_name(self):
        return self.name

    def get_ec_nummer(self):
        return self.ec_nummer

    def __get_info(self):
        """
        hoofd functie, dit voert als hij af is alles uit.
        dus kan je alles uit proberen.
        :return:
        """

    def _ec_getter(self):
        """

        :return:
        """
        ec_nummers = []
        naam = '%20'.join(self.name.split(' '))
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&protein={}".format(naam)
        r = requests.get(requestURL, headers={"Accept": "application/xml"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        responseBody = r.text.split('<')
        for line in responseBody:
            if 'ecNumber evidence' in line:
                ec_nummers += [line.split('>')[1]]
        if ec_nummers == []:
            self.ec_nummer = 'none'
        else:
            self.ec_nummer= set(ec_nummers)

    def _split_protein_regions_t(self):
        """

        :return:
        """
        data = []
        region = False
        for line in self.file:

            if 'Site' in line:
                region = True
            if region:
                data += [line.strip()]
                print(line.strip())
            if '/db_xref' in line and region:
                #area, name, db_ref = data.pop(0).split(' ')[-1], data.pop(0).split('"')[1], data.pop().split('"')[1]
                #self.regions[area] = [name, db_ref, ''.join(data).split('"')[1]]
                region = False
                data = []

    def _split_protein_regions(self):
        """

        :return:
        """
        data = []
        region = False
        for line in self.file:
            # print(line)
            if 'Region' in line:
                region = True
            if region:
                data += [line.strip()]
            if '/db_xref' in line and region:
                area, name, db_ref = data.pop(0).split(' ')[-1], data.pop(0).split('"')[1], data.pop().split('"')[1]
                self.regions[area] = [name, db_ref, ''.join(data).split('"')[1]]
                region = False
                data = []

    def __str__(self):
        return self.locus


if __name__ == '__main__':
    import os
    name = 'XP_007072912.1'
    os.system('mkdir bestanden')
    os.system(
        'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt -q'.format(
            'protein', name))
    test = Protein_gb_info(('bestanden/'+ name + '.txt'))
    print(test)
    print(test.get_name())
    print(test.get_ec_nummer())
    print(test.get_regions())
    print(test)
