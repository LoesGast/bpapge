lass Kegg_info():
    def __init__(self, file_naam):
        self.file = open(file_naam, 'r').readlines()
        self.EC_nummer = self.EC_nummer_info()
        self.reaction = self.reaction_info()
        self.pathway = self.pathway_info()


    def get_EC_nummer(self):
        return self.EC_nummer

    def get_reaction(self):
        return self.reaction

    def get_pathway(self):
        return self.pathway

    def EC_nummer_info(self):
        regel = ''
        for line in self.file:
            if 'ENTRY' in line:
                line = line.split()
                regel = line[1] + ' ' + line[2]
                return regel

    def reaction_info(self):
        regel = ''
        for line in self.file:
            if 'REACTION' in line:
                line = line.split()
                regel = line[1:-1]
                return ' '.join(regel)

    def pathway_info(self):
        file = self.file
        sublijst = []
        for line in file:
            if 'PATHWAY' in line:
                index = file.index(line)
                file =  file[index:]
                for regel in file:
                    lijst_regel = []
                    for x in regel:

                        lijst_regel.append(x)

                #         for y in lijst_regel[0:4]:
                #             if y in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                #                 sublijst.append(y)
                #             len = 0
                #             for q in sublijst:
                #                 len+=1
                #             if len == 4:
                #                 index2 = file.index(regel)
                #                 print(index2)
                #                 een_tellen = 0
                #                 for p in index2:
                #                     if p == 1:
                #                         een_tellen +=1
                #                         file = file[:een_tellen]
                #
                # print(file)









if __name__ == '__main__':
    hoi = Kegg_info('6.1.1.17.txt')
    hoi.pathway_info()


        #file_naam = '6.1.1.17.txt'
        #file = openen(file_naam)



