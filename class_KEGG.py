import os


class Kegg_info():
    path_name = 'temp'
    _download_path = os.getcwd() + '/{}/pathways/'.format(path_name)

    def __init__(self, ec_nummer):
        self.ec_nummer = ec_nummer
        self._open_or_download()
        self.reaction_info()
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
        return self.pathways

    def _get_pathways(self):
        zone = False
        pathways = []
        for line in self.file:
            if 'PATHWAY' in line:
                zone = True
            if zone and 'ORTHOLOGY' in line:
                self.pathways += pathways
                break
            elif zone:
                data = line.strip('PATHWAY').strip().split()
                path_naam = ' '.join(data[1:])
                pathways += [[data[0], path_naam]]

    def reaction_info(self):
        zone = False
        data = []
        for line in self.file:
            if 'REACTION' in line:
                zone = True
            if zone and 'ALL_REAC' in line:
                self.reaction = '\n'.join(data)
            elif zone:
                data += [
                    (' '.join([line.strip('REACTION').strip()]).split('[')[0])]


if __name__ == '__main__':
    hoi = Kegg_info('2.5.1.17')
    print(hoi.get_EC_nummer())
    print(hoi.get_reaction())
    print(hoi.get_pathway())
