class Protein_gb_info():
    def __init__(self, file_naam):
        self.file = open(file_naam, 'r').readlines()
        self.__lijst_met_variables()
        self._split_protein_regions_test()
        self.__get_info()

    def __lijst_met_variables(self):
        self.regions = {}

    def get_regions(self):
        """
        returnt de regions die in de genbank file staan.
        :return: Regions Dict.
        """
        return self.regions

    def __get_info(self):
        """
        hoofd functie, dit voert als hij af is alles uit.
        dus kan je alles uit proberen.
        :return:
        """
        for i in self.regions:
            print(i, self.regions[i])
        pass

    def _split_protein_regions_test(self):
        """

        :return:
        """
        data, region_dict = [], {}
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


if __name__ == '__main__':
    import os
    os.system('mkdir bestanden')
    os.system(
        'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O ./bestanden/{1}.txt -q'.format(
            'nucleotide', 'XM_007079698.2'))
    test = Protein_gb_info('bestanden/XP_007072912.1.txt')
    test.get_regions()