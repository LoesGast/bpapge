import os


class Nucleotide_gb_info():
    path_name = 'temp'
    _download_path = os.getcwd() + '/{}/nucleotide/'.format(path_name)
    _download_exonnen = os.getcwd() + '/{}/gene/'.format(path_name)

    def __init__(self, accession):
        self.accession = accession
        self.file = self._open_or_download()
        self.line = ""
        self.sequence = ""
        self.gene_name = ""
        self.cds_start = ""
        self.cds_stop = ""
        self.product = ""
        self.protein_id = ""
        self.gene_id = ""
        self.exons = []
        self.file_info()

    def get_accession(self):
        return self.accession

    def get_gene_id(self):
        return self.gene_id

    def get_sequence(self):
        return self.sequence

    def get_gene_name(self):
        return self.gene_name

    def get_cds(self):
        return self.cds_start, self.cds_stop

    def get_product(self):
        return self.product

    def get_protein_id(self):
        return self.protein_id


    def _open_or_download(self):
        """
        probeert eerste de file open te maken met de gegeven naam (locus/ID)
        indien dit niet werkt wordt de file vanaf NCBI gedownload en daarna
        wordt de file als nog geopend en wordt de gelezen file
        in self.file geplaats
        """
        try:
            file = open(self._download_path + self.accession + '.txt', 'r')
        except FileNotFoundError:
            os.system(
                'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gb&retmode=text" -O {2}{1}.txt -q'.format(
                    'nucleotide', self.accession, self._download_path))
            file = open(self._download_path + self.accession + '.txt', 'r')
        finally:
            self.inhoud = file.read().splitlines()
            file.close()

    def file_info(self):
        is_in_line_seq, is_in_line_cds = False, False
        for self.line in self.inhoud:
            is_in_line_seq = self._sequence_getter(is_in_line_seq)
            is_in_line_cds = self._cds_getter(is_in_line_cds)
            self._product_name_getter()
            self._gene_name_getter()
            self._protein_id_getter()
            self._gene_id_getter()
        self.exon_getter()

    def _product_name_getter(self):
        if "/product" in self.line:
            self.product = self.line.split('=')[1].lstrip().replace('"', '')

    def _gene_name_getter(self):
        if "/gene" in self.line:
            self.gene_name = self.line.split('=')[1].lstrip().replace('"', '')

    def _protein_id_getter(self):
        if "/protein_id" in self.line:
            self.protein_id = self.line.split('=')[1].lstrip().replace('"', '')

    def _gene_id_getter(self):
        if '/db_xref="GeneID' in self.line:
            self.gene_id = self.line.split(':')[1].lstrip().replace('"', '')

    def _sequence_getter(self, is_origin):
        if 'ORIGIN' in self.line:
            is_origin = True
        elif is_origin:
            for letter in self.line:
                if letter.isalpha():
                    self.sequence += letter
        return is_origin

    def _cds_getter(self, is_features):
        if 'FEATURES' in self.line:
            is_features = True
        if 'CDS ' in self.line and is_features:
            self.cds_start = self.line.split()[1].split("..")[0]
            self.cds_stop = self.line.split()[1].split("..")[1]
        return is_features

    def exon_getter(self):
        os.system(
            'wget "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={0}&id={1}&rettype=gene_table&retmode=text" -O {2}{1}.txt -q'.format(
                'gene', self.gene_id, self._download_exonnen))
        data, is_data, exon_region = {}, False, False
        with open(self._download_exonnen + self.gene_id + '.txt' , 'r') as genes:
            for line in genes.readlines():
                if self.accession in line:
                    exon_region = True
                if '\n' == line:
                    is_data = False
                    exon_region = False
                if '----' in line:
                    is_data = True
                elif is_data and exon_region:
                    self.exons += [line.split('\t')[0].split('-')]

    def __str__(self):
        return self.accession


if __name__ == '__main__':

    #test = Nucleotide_gb_info('XM_007079698.2')
    #test = Nucleotide_gb_info('XM_015539643.1')
    test = Nucleotide_gb_info('XM_007079093.2')
    test.file_info()
    print('Product: ' + test.get_product())
    print('GeneID: ' + test.get_gene_id())
    print('Seq: ' + test.get_sequence())
    print('Accession: ' + test.get_accession())
    print('Gennaam: ' + test.get_gene_name())
    print('ProteinID: ' + test.get_protein_id())
    print('CDS (start, stop):', test.get_cds())
    for exon in test.exons:
        print(exon)

    # test.product_name_getter()
    # test.gene_name_getter()
    # test.protein_id_getter()
    # test.gene_id_getter()
    # #test.translation_getter()
    # test.cds_getter()
