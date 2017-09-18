class Protein_gb_info():
    def __init__(self, file_naam):
        self.file = open(file_naam, 'r').readlines()
        self.__lijst_met_variables()
        self._split_protein_regions_test()
        self.__get_info()

    def __lijst_met_variables(self):
        self.regions = {}

    def __get_info(self):
        for i in self.regions:
            print(i, self.regions[i])
        pass

    def _split_protein_regions_test(self):
        data, region_dict = [], {}
        region = False
        for line in self.file:
            #print(line)
            if 'Region' in line:
                region = True
            if region:
                data += [line.strip()]
            if '/db_xref' in line and region:
                area, name, db_ref = data.pop(0).split(' ')[-1], data.pop(0).split('"')[1], data.pop().split('"')[1]
                self.regions[area] = [name, db_ref, ''.join(data).split('"')[1]]
                region = False
                data = []



test = Protein_gb_info('temp/protein/XP_007072912.1.txt')