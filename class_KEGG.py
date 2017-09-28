import os


class Kegg_info():

    path_name = 'temp'
    _download_path = os.getcwd() + '/{}/pathways/'.format(path_name)

    def __init__(self, ec_nummer):
        self.ec_nummer = ec_nummer
        self._open_or_download()
        self.reaction = self.reaction_info()
        self.pathways = []
        self._get_pathways()


    def _open_or_download(self):
        try:
            file = open(self._download_path + self.ec_nummer + '.txt', 'r')
        except FileNotFoundError:
            os.system(
                'wget "http://rest.kegg.jp/get/{0}" -O {1}/{0}.txt -q'.format(
                    self.ec_nummer, self._download_path))
            file = open(self._download_path + self.ec_nummer + '.txt', 'r')
        finally:
            self.file = file.readlines()
            file.close()

    def get_EC_nummer(self):
        return self.ec_nummer

    def get_reaction(self):
        return self.reaction

    def get_pathway(self):
        return set(self.pathways)

    def _get_pathways(self):
        pathway_list = []
        for item in self.file:
            if 'PATHWAY' in item:
                path_positie = self.file.index(item)
            if 'ORTHOLOGY' in item:
                orth_positie = self.file.index(item)
                self.pathways += self.file[path_positie:orth_positie]
                break


    def reaction_info(self):
        regel = ''
        for line in self.file:
            if 'REACTION' in line:
                line = line.split()
                regel = line[1:-1]
                return ' '.join(regel)


if __name__ == '__main__':
    os.mkdir('./temp/pathways')
    hoi = Kegg_info('6.1.1.17')
    print(hoi.get_EC_nummer())
    print(hoi.get_reaction())
    print(hoi.get_pathway())








