# python 3 on linux

import os
import subprocess
import time



def dw_files():
    """


    :return: Niks
    """
    os.system('mkdir bestanden')
    os.system('mv downloadblast.sh ./bestanden/downloadblast.sh')
    os.system('mv bpapge_seq_a1.txt ./bestanden/bpapge_seq_a1.txt')
    subprocess.run(['bash', 'downloadblast.sh'], cwd='bestanden')
    os.system('mv ./bestanden/downloadblast.sh downloadblast.sh')
    os.system('mv ./bestanden/bpapge_seq_a1.txt bpapge_seq_a1.txt')
    print('Downloading done\nBlast done')


### download functies start
def allebestanden(path):
    bestandenlijst = os.listdir(path)
    nieuwe_bestandenlijst = []
    for item in bestandenlijst:
        nieuwe_bestandenlijst.append(item)
    return nieuwe_bestandenlijst


def finding_data_test(lijst, data):
    for line in lijst:
        if data in line:
            return line.split('"')[1]


def main():
    temp_naam = os.getcwd() + 'temp'
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
                os.system('mkdir ./{}'.format(temp_naam))
                os.system('mkdir ./{}/nucleotide'.format(temp_naam))
                os.system('mkdir ./{}/protein'.format(temp_naam))
                os.system('mkdir ./{}/pathways'.format(temp_naam))
                pass
            elif keuze == '2':
                pass
            elif keuze == '3':
                exit()
            else:
                print('wrong input, probeer opnieuw.')

if __name__ == '__main__':
    main()

