import os, re, slate
from io import StringIO

numbered_lines = "" #string "st.vrstice - 1: vrstica"; zbrisi to na koncu


paths = open('paths_plinska.txt', 'r')
pathInPathOut = paths.readlines()
inPath = pathInPathOut[1][:-1] #pdfs are here
outPath = pathInPathOut[4][:-1] #outputs are here

os.chdir(inPath)
reports = os.listdir(inPath)

#regex:
def re_ka_ph(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za Ka-pH (7.ddd), vrne vrednost, sicer False
    reKa_ph = re.compile(r'(?P<ka_ph>7\.\d\d\d)')
    matchKa_ph = reKa_ph.search(vrstica)
    if matchKa_ph:
        ka_ph = matchKa_ph.group('ka_ph')
        return ka_ph
    return False

def re_ka_pco2(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za pCO2 (d.dd), vrne vrednost, sicer False
    re_ka_Pco2 = re.compile(r'(?P<ka_pco2>\d\.\d\d)')
    match_ka_Pco2 = re_ka_Pco2.search(vrstica)
    if match_ka_Pco2:
        ka_pco2 = match_ka_Pco2.group('ka_pco2')
        return ka_pco2
    return False

def re_ka_presezek_baze(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za presezek baze (d+.d), vrne vrednost, sicer False
    re_ka_presezek_baze = re.compile(r'(?P<ka_presezek_baze>\d+\.\d)')
    match_ka_presezek_baze = re_ka_presezek_baze.search(vrstica)
    if match_ka_presezek_baze:
        ka_presezek_baze = match_ka_presezek_baze.group('ka_presezek_baze')
        return ka_presezek_baze
    return False

for report in reports:
    with open(report, 'rb') as f:
        doc = slate.PDF(f)
    textFromPage1 = doc[0] #string iz pdfja
    strPO = StringIO(textFromPage1) #StringIO object
    #print(StringIO.readlines(strPO))
    list_vrstic = StringIO.readlines(strPO) #StringIO object (strPO), pretvorjen v list_vrstic

    #zacetne vrednosti spremenljivk so "ni podatka"
    output = False #string, iz katerega bo nastal txt file
    id_pacienta = "ni podatka"
    priimek_ime = "ni podatka"
    dodatek_kisika = "ni podatka"
    ka_ph = "ni podatka"
    ka_pco2 = "ni podatka"
    sat_o2 = "ni podatka"
    ka_presezek_baze = "ni podatka"
    ka_standardni_hco3 = "ni podatka"
    sat_o2 = "ni podatka"
    ka_po2 = "ni podatka"

    plinska_prva_vrstica = False
    ka_ph_stevilka_vrstice = False

    counter = 0 #stevilka vrstice

    for vrstica in list_vrstic:
        counter += 1
        #print(counter, ": ", vrstica)
        numbered_lines += str(counter) + ": " + vrstica
        #preveri, kje se začne izvid PAAK v pdfju; plinska_prva_vrstica = vrstica
        if "Plinska analiza arterijske krvi" in vrstica:
            print("kle se začne plinska")
            plinska_prva_vrstica = counter
        #ce najde zacetek paak izvida, 5 - 15 po tem isce, dokler ne najde prve vrednosti, ki ustreza Ka_pH:
        elif ka_ph == "ni podatka" and plinska_prva_vrstica and (15 > (counter - plinska_prva_vrstica) > 5):
                if re_ka_ph(vrstica):
                    ka_ph = re_ka_ph(vrstica)
                    ka_ph_stevilka_vrstice = counter
        #ko najde ka_ph, gleda ostale:
        elif ka_ph_stevilka_vrstice:
            if ka_pco2 == "ni podatka" and re_ka_pco2(vrstica):
                ka_pco2 = re_ka_pco2(vrstica)
            elif ka_presezek_baze == "ni podatka" and re_ka_presezek_baze(vrstica):
                ka_presezek_baze = re_ka_presezek_baze(vrstica)


    #[:-1] - da je string brez newlina
    #id in priimek in ime so (verjetno) vedno 6., 11. vrstica
    id_pacienta = list_vrstic[7][:-1]
    priimek_ime = list_vrstic[12][:-1]
    #plinska:
    dodatek_kisika =list_vrstic[plinska_prva_vrstica + 5][:-1]
    #ka-ph:

    """
    ka_ph = list_vrstic[ka_std_hco3_tekst - 84][:-1]

    ka_pco2 = list_vrstic[ka_std_hco3_tekst - 83][:-1]
    ka_presezek_baze = list_vrstic[ka_std_hco3_tekst - 82][:-1]
    ka_standardni_hco3 = list_vrstic[ka_std_hco3_tekst - 81][:-1]
    sat_o2 = list_vrstic[ka_std_hco3_tekst - 78][:-1]
    ka_po2 = list_vrstic[ka_std_hco3_tekst - 77][:-1]
    """
    print("plinska se začne (counter): ", plinska_prva_vrstica)

    print("id: ", id_pacienta)
    print("priimek in ime: ", priimek_ime)
    print("vdihana količina kisika: ", dodatek_kisika)

    print("Ka-pH: ", ka_ph)
    print("Ka-pCO2: ", ka_pco2)
    print("Ka-presežek baze: ", ka_presezek_baze)
    print("Ka-standardni HCO3: ", ka_standardni_hco3)
    print("Ka-saturacija O2: ", sat_o2)
    print("Ka-pO2: ", ka_po2)


    output = "Priimek in ime: " + priimek_ime + "\n" + \
    "id: " + id_pacienta + "\n" + \
    "Ka-ph: " + ka_ph + "\n" + \
    "Ka-pCO2: " + ka_pco2 + "\n" + \
    "Ka-saturacija O2: " + sat_o2 + "\n"

    #print(output)

    if output:
        outputFileName = priimek_ime + "_" + id_pacienta + ".txt"
        print(outputFileName)
        os.chdir(outPath)
        outputFile = open(outputFileName, 'w')
        #outputFile.write(output)
        outputFile.write(numbered_lines) #txt file oblike: st. vrstice -1: vrstica"
        outputFile.close()
    else:
        print("nekisjeban")


    #to do:
    # - spremenljivke v list al neki drugega?
    # - preveri, ce stevilka vrstice sovpada s tekstom - da ni kaj zamaknjeno
