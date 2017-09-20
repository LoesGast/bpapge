import os

def allebestanden():
    bestandenlijst = os.listdir()
    nieuwe_bestandenlijst = []
    for item in bestandenlijst:
        if len(item) == 18:
            nieuwe_bestandenlijst.append(item)
    return nieuwe_bestandenlijst


def gen_lijst():
    open_gen_bestand = open('XM_007072850.1.txt', 'r')
    lees_gen_bestand = open_gen_bestand.read().strip().split()
    return lees_gen_bestand

def finding_CDS(m_allebestanden):
    protein_id_list = []
    for item in m_allebestanden:
        open_gen_bestand = open(item, 'r')
        lees_gen_bestand = open_gen_bestand.readlines()
        for item in lees_gen_bestand:
            if '/protein_id=' in item:
                stripped_item = item.split('"')
                    #strip('/protein_id=')
                protein_id_list.append(stripped_item[1])
    print(len(protein_id_list))


def main():
    m_allebestanden = allebestanden()
    #m_gen_lijst = gen_lijst()
    finding_CDS(m_allebestanden)

main()