import requests

class Protein_gb_info():
    def __init__(self, file_naam):
        self.file = file_naam.readlines()
        self.__lijst_met_variables()
        self._get_all_info()
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

    def _ec_getter(self):
        """

        :return:
        """
        ec_nummers = []
        naam = '%20'.join(self.name.strip('\n').split(' '))
        if len(naam) >= 50:
            naam = naam[:55]
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&protein={}".format(
            naam)
        r = requests.get(requestURL, headers={"Accept": "application/xml"})
        if not r.ok:
            r.raise_for_status()
            self.ec_nummer = ['none']
        else:
            responseBody = r.text.split('<')
            for line in responseBody:
                if 'ecNumber evidence' in line:
                    ec_nummers += [line.split('>')[1]]
            if ec_nummers == []:
                self.ec_nummer = ['none']
            else:
                self.ec_nummer = set(ec_nummers)

    def _get_all_info(self):
        data, is_info = [], ''
        for line in self.file:
            is_info, data = self.region_get(line, data, is_info)
            is_info = self.sequence_getter(line, is_info)

    def region_get(self, line, data, is_region):
        if 'Region' in line:
            is_region = 'Region'
        if 'Region' == is_region:
            data += [line.strip()]
        if '/db_xref' in line and is_region == 'Region':
            area = data.pop(0).split(' ')[-1]
            name = data.pop(0).split('"')[1]
            db_ref = data.pop().split('"')[1]
            self.regions[area] = [name, db_ref, ''.join(data).split('"')[1]]
            data = []
            is_region = ''

        return is_region, data

    def sequence_getter(self, line, is_origin):
        if 'ORIGIN' in line:
            is_origin = 'seq'
        elif is_origin == 'seq':
            for letter in line:
                if letter.isalpha():
                    self.sequence += letter
        return is_origin


    def __str__(self):
        return self.locus


if __name__ == '__main__':
    import os

    name = 'XP_007072912.1'
    os.system('mkdir bestanden')
    os.system(
        'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt -q'.format(
            'protein', name))
    file = open('bestanden/' + name + '.txt', 'r')
    test = Protein_gb_info(file)

    print(test.get_regions())
    print(test.get_sequence())
    print(test.get_ec_nummer())
