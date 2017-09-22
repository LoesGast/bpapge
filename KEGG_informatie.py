

def positie_pathway(KEGG_bestand):
    pathway_list = []
    for item in KEGG_bestand:
        if 'PATHWAY' in item:
            path_positie = KEGG_bestand.index(item)
            for item in KEGG_bestand[path_positie:]:
                if 'ORTHOLOGY' in item:
                    orth_positie = KEGG_bestand.index(item)
                    pathway_list.append(KEGG_bestand[path_positie:orth_positie])
    return pathway_list

def main():
    KEGG_bestand = open('6.1.1.17.txt', 'r').readlines()
    pathway_list = positie_pathway(KEGG_bestand)
    nieuwe_lijst = pathway_list[0]
    pathway_lijst = []
    for item in nieuwe_lijst:
        print(item)
main()

