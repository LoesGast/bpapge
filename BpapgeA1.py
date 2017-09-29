# python 3 on linux

import os
import subprocess
import time



def dw_files():
    """
    heeft nodig de bash script "downloadblast.sh" en de sequenties
     "bpapge_seq_a1".
    deze worden naar de map bestanden verplaats. en hier worden ze
    uitgevoerd.
    downloadblast download de genoom van de Panthera tigris altaica en
    gebruikt dat als de data base om de bpapge_seq_a1 te blasten.
    en er komt de file output_blasten.txt als uitkomst uit. en de bestanden
    worden weer terug in de main map gezet.
    :return: Niks
    """
    os.system('mv downloadblast.sh ./bestanden/downloadblast.sh')
    os.system('mv bpapge_seq_a1.txt ./bestanden/bpapge_seq_a1.txt')
    subprocess.run(['bash', 'downloadblast.sh'], cwd='bestanden')
    os.system('mv ./bestanden/downloadblast.sh downloadblast.sh')
    os.system('mv ./bestanden/bpapge_seq_a1.txt bpapge_seq_a1.txt')

def get_output_blasten():
    """

    maakt de output van blasten open en pakt alle waardes die een e-value
    van 0.0 heeft. deze worden in een lisjt gezet en aan het einde wordt de
    de lijst uniek gemaakt met set().
    :return: een lijst met unieke gene codes van de output van blasten (list)
    """
    lijst = []
    with open('./bestanden/output_blasten.txt') as file:
        data = file.readlines()
        for x in data:
            z = x.split('\t')
            if z[10] == '0.0':
                lijst += [z[1].split('|')[3]]
        return set(lijst)








def main():
    temp_naam = os.getcwd() + '/temp'
    print('''
Welkom bij het programma voor de opdracht van de hogeschool Leiden van de opleiding Bio-informatica.
met dit programma wordt het project applied genomics in jaar 2 uitgevoerd.
ik hoop dat u het leuk vind.
Met vriendelijke groeten,
Groep A1 (Shirley, Lotta, Hanna, Loes en Nils)\n\n\n\n''')
    time.sleep(5)
    if 'blasten.sh' not in os.listdir() or 'bpapge_seq_a1.txt' not in os.listdir():
        print('''er is een probleem met de files.
blasten.sh of bpapge_seq_a1.txt zijn niet id de map''')
        quit()
    else:
        while True:
            keuze = input('''welkom u kan nu het programma uit te voeren.
1) het uitvoeren van het programmma
2) opties veranderen
3) afsluiten
maak u keuzen:\n''')
            if keuze == '1':
                os.system('mkdir ./bestanden')
                os.system('mkdir {}'.format(temp_naam))
                os.system('mkdir {}/nucleotide'.format(temp_naam))
                os.system('mkdir {}/protein'.format(temp_naam))
                os.system('mkdir {}/pathways'.format(temp_naam))
                genenlijst = get_output_blasten()
                print(genenlijst)
                pass
            elif keuze == '2':
                pass
            elif keuze == '3':
                exit()
            else:
                print('wrong input, probeer opnieuw.')

if __name__ == '__main__':
    main()

