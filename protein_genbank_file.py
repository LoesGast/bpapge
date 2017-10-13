import os
import requests


class Protein_gb_info():
    # global variables voor het downloaden van de files
    path_name = 'temp'
    _download_path = os.getcwd() + '/{}/protein/'.format(path_name)

    def __init__(self, protein_code):
        self.locus = protein_code
        self._open_or_download()
        if os.stat(self._download_path + self.locus + '.txt').st_size != 0:
            self.name = self.file[1].split(':')[-1].split('[')[0].strip(' ')
            self.regions = []
            self.site = []
            self.sequence = ''
            self.ec_nummer = []
            self.location = ''
            self.db_info = ''
            self._get_all_info()
            self._ec_getter()


    def get_regions(self):
        """
        returnt de regions die in de genbank file staan.
        :return: de Regions Dict (dict)
        """
        return self.regions

    def get_sequence(self):
        """
        returnt de sequentie die in de genbank file staan.
        :return: de sequentie in de gb_file (str)
        """
        return self.sequence

    def get_sites(self):
        """
        returnt de sites die in de genbank file staan.
        :return: de sites Dict (dict)
        """
        return self.site

    def get_name(self):
        """
        returnt de naam van het eiwit die in de genbank file staan.
        :return: de naam van het eiwit (str)
        """
        return self.name

    def get_location(self):
        """
        returnt de locatie van het eiwit die in de genbank file staan.
        :return: de locatie van het eiwit (str)
        """
        return self.location

    def get_ec_nummer(self):
        """
        returnt de een lijst van alle ec nummers die gevonden zijn bij
        enbl-ebi
        :return: lijst met ec nummers (list)
        """
        return set(self.ec_nummer)

    def get_location(self):
        """
        returnt de lokatie van waar het eiwit te vinden is in een cel
        :return: lokatie van
        """
        return self.location

    def _open_or_download(self):
        """
        probeert eerste de file open te maken met de gegeven naam (locus/ID)
        indien dit niet werkt wordt de file vanaf NCBI gedownload en daarna
        wordt de file als nog geopend en wordt de gelezen file
        in self.file geplaats
        """
        try:
            file = open(self._download_path + self.locus + '.txt', 'r')
        except FileNotFoundError:
            os.system(
                'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O {2}{1}.txt -q'.format(
                    'protein', self.locus, self._download_path ))
            file = open(self._download_path+ + self.locus + '.txt', 'r')
        finally:
            self.file = file.readlines()
            file.close()



    def _ec_getter(self):
        """
        downlaod de Kegg database file van de protein en
         pakt hieruit de EC nummer.
        :return: None
        """
        try:
            file = open(self._download_path + self.db_info + '.txt', 'r')
        except FileNotFoundError:
            os.system(
                'wget "http://rest.kegg.jp/get/ptg:{0}" -O {1}/{0}.txt -q'.format(
                    self.db_info, self._download_path + '/kegg/'))
            file = open(self._download_path + '/kegg/' + self.db_info + '.txt', 'r')
        finally:
            file_kegg = file.readlines()
            file.close()
        for line in file_kegg:
            if 'EC:' in line:
                self.ec_nummer = line.split('EC:')[1].split(']')[0].split(' ')



    def _data_getter(self):
        """
        vraagt in embl-ebi alle info van de protein in xml text. en gaat
        hier veder me werken met de functie: info_getter.

        :return:
        """
        if len(self.name.strip('\n')) > 50:
            naam = self.name[:44]
        else:
            naam = self.name.strip('\n')
        naam = '%20'.join(naam.split('isoform')[0].split(',')[0].split(' '))
        print(naam)
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&protein={}".format(
            naam)
        r = requests.get(requestURL, headers={"Accept": "application/xml"})
        if not r.ok:
            r.raise_for_status()
        else:
            responseBody = r.text.split('<')
            self.info_getter(responseBody)

    def info_getter(self, responsebody_2):
        """
        :param responsebody_2: lijst van de xml uitkomsten van
            data_getter (lijst).
            zoekt in de lijst naar specifieke data.
        :return: None
        """
        for line in responsebody_2:
            if '"C:' in line:
                self.location = line.split('"')[1].split(':')[1]



    def _get_all_info(self):
        """
        Loopt door de genebank file en haalt hier alle nodig informatie uit
        met behulp van functies die als if-statements fungeren.
        :return:
        """
        m_data, is_info = [], ''
        for line in self.file:
            is_info = self._region_get(line, m_data, is_info)
            is_info = self._site_getter(line, m_data, is_info)
            is_info = self._sequence_getter(line, is_info)
            if 'GeneID:' in line:
                self.db_info = line.split('"')[1].split(':')[1]

    def _region_get(self, line, data, is_region):
        """
        :param line: line van de file (str)
        :param data: lijst met alle data indien een functie data
         is aan het sparen (lijst)
        :param is_region: kijkt of de lijn de in de functie komt in
         een regio stuck zit (boolean)

        kijkt of in een line het word "Region" zit en dus data wat moet
         worden gesplit worden. Hierna wordt de data gespaard totdat het eind
         deel van de regio data wordt gededecteerd. als het einde is gekomen
         van de regio wordt dit opgeslagen in een lijst in een lijst. en wordt
         de regio uit gezet tot dat deze weer wordt ontdekt wordt.

        :return: None
        """
        if 'Region' in line:
            is_region = 'Region'
        if 'Region' == is_region:
            data += [line.strip()]
        if '/db_xref' in line and is_region == 'Region':
            area = data.pop(0).split(' ')[-1]
            name = data.pop(0).split('"')[1]
            db_ref = data.pop().split('"')[1]
            self.regions += [[area, name, db_ref, ''.join(data).split('"')[1]]]
            data.clear()
            is_region = ''

        return is_region

    def _sequence_getter(self, line, is_origin):
        """
        :param line: line van de file (str).
        :param is_origin: kijkt of de lijn in de sequentie regio zit (boolean).

        loopt door de lijst en als de line in sequentie regio zit worden alle
         letters toegevoegd aan de sequentie.

        :return: None
        """
        if 'ORIGIN' in line:
            is_origin = 'seq'
        elif is_origin == 'seq':
            for letter in line:
                if letter.isalpha():
                    self.sequence += letter
        return is_origin

    def _site_getter(self, line, data, is_site):
        """
        :param line: line van de file (str)
        :param data: lijst met alle data indien een functie data
            is aan het sparen (lijst)
        :param is_region: kijkt of de lijn de in de functie komt in
            een regio stuck zit (boolean)

        kijkt of in een line het word "Site" zit en dus data wat moet
         worden gesplit worden. Hierna wordt de data gespaard totdat het eind
         deel van de site data wordt gededecteerd. als het einde is gekomen
         van de site-regio wordt dit opgeslagen in een lijst en toegevogd
         aan de lijst van sites. en wordt
         de regio uit gezet tot dat deze weer wordt ontdekt wordt.

        :return: None
        """
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
            self.site += [[dat4, site_type, note, dbref]]
            is_site = ''
            data.clear()
        return is_site

    def __str__(self):
        """
        returnd de naam van het eiwit als deze klas wordt geprint
        :return:
        """
        return self.locus


if __name__ == '__main__':
    name = 'XP_007096051.1'
    test = Protein_gb_info(name)

    print(test.get_regions())
    data = test.get_sites()
    for i in data:
        print(i)
    print(test.get_sequence())
    print(test.get_ec_nummer())
    print(test.get_location())
