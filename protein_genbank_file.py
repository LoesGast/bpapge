import os
import requests


class Protein_gb_info():
    # global variables
    path_name = 'temp'
    _download_path = os.getcwd() + '/{}/protein/'.format(path_name)

    def __init__(self, protein_code):
        self.locus = protein_code
        self._open_or_download()
        if os.stat(self._download_path + self.locus + '.txt').st_size != 0:
            self.name = self.file[1].split(':')[-1].split('[')[0].strip(' ')
            self.regions = {}
            self.site = {}
            self.sequence = ''
            self.ec_nummer = ''
            self._get_all_info()
            self._ec_getter()

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

    def _open_or_download(self):
        try:
            file = open(self._download_path + self.locus + '.txt', 'r')
        except FileNotFoundError:
            pass
            os.system(
                'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O {2}{1}.txt -q'.format(
                    'protein', self.locus, self._download_path))
            file = open(self._download_path + self.locus + '.txt', 'r')
        finally:
            self.file = file.readlines()
            file.close()

    def _ec_getter(self):
        """

        :return:
        """
        ec_nummers = []
        naam = '%20'.join(self.name.strip('\n').split('isoform')[0].split(' '))
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
        m_data, is_info = [], ''
        for line in self.file:
            is_info = self._region_get(line, m_data, is_info)
            is_info = self._site_getter(line, m_data, is_info)
            is_info = self._sequence_getter(line, is_info)

    def _region_get(self, line, data, is_region):
        if 'Region' in line:
            is_region = 'Region'
        if 'Region' == is_region:
            data += [line.strip()]
        if '/db_xref' in line and is_region == 'Region':
            area = data.pop(0).split(' ')[-1]
            name = data.pop(0).split('"')[1]
            db_ref = data.pop().split('"')[1]
            self.regions[area] = [name, db_ref, ''.join(data).split('"')[1]]
            data.clear()
            is_region = ''

        return is_region

    def _sequence_getter(self, line, is_origin):
        if 'ORIGIN' in line:
            is_origin = 'seq'
        elif is_origin == 'seq':
            for letter in line:
                if letter.isalpha():
                    self.sequence += letter
        return is_origin

    def _site_getter(self, line, data, is_site):
        if 'Site' in line:
            is_site = 'Site'
        if is_site == 'Site':
            data += [line.strip()]
        if '/db_xref' in line and is_site == 'Site':
            dbref = data.pop().split('"')[1]
            if 'note' in data[-1]:
                note = data.pop().split('"')[1]
            else:
                note = ''
            site_type = data.pop().split('"')[1]
            dat4 = ''.join(data).split('(')[-1].strip(')').strip('Site').strip()
            self.site[dat4] = [site_type, note, dbref]
            is_site = ''
            data.clear()
        return is_site

    def __str__(self):
        return self.locus


if __name__ == '__main__':
    name = 'XP_007072912.1'
    test = Protein_gb_info(name)

    print(test.get_regions())
    data = test.get_sites()
    for i in data:
        print(i, data[i])
    print(test.get_sequence())
    print(test.get_ec_nummer())
